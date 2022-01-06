#!/usr/bin/env python
# coding=utf-8
# =================================================================================================================================================
# This script obtains data on jobs (name and specific attributes like topology, storage backend, etc.) and updates google spreadsheet with the data
# =================================================================================================================================================
import datetime
import gspread
from gspread.models import Cell
from elasticsearch import Elasticsearch
from oauth2client.service_account import ServiceAccountCredentials
import yaml


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/google_creds.json", scope)
client = gspread.authorize(creds)
general_sheet = client.open("jenkins jobs").sheet1
data = general_sheet.get_all_records()

fields = ["network_backend", "dvr", "overcloud_ssl", "storage_backend", "topology", "ip_version", "ovn", "ovs"]

body={
    "query": {
        "bool": {
            "must_not": {
                    "range": {"@timestamp": {"lte": "now-14d/d"}},
            },
            "should": [{"exists": {"field": field}} for field in fields]
        }
    },
    "_source": fields + ["job_name"]
}

all_jobs_body = {
    "size": 0,
    "aggs" : {
        "jobs" : {
            "terms" : { "field" : "job_name.keyword",  "size" : 4000 }
        }
    }
}

with open(r'/etc/arie.yaml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

es = Elasticsearch(data['elk']['es_url'])

# Get all jobs
result = es.search(index="logstash", body=all_jobs_body)
jobs = {}
for job in result["aggregations"]["jobs"]["buckets"]:
    jobs[job['key']] = {}

results = es.search(index="logstash", body=body, size=2000)
for res in results['hits']['hits']:
    for k,v in res['_source'].items():
        jobs[res['_source']['job_name']][k] = v

cells_li = []
cells_li.append(Cell(row=1, col=1 , value="This spreadsheet is auto-generated based on data from ELK from the past 14 days. PLEASE DON'T EDIT MANUALLY :)"))
cells_li.append(Cell(row=2, col=1 , value="Last update: {} (Israel Time)".format(str(datetime.datetime.now()))))
i = 4
for job, values in jobs.items():
    cells_li.append(Cell(row=i, col=1, value=job))
    field_i = 2
    for field in fields:
        cells_li.append(Cell(row=3, col=field_i , value=field))
        if field in values:
            cells_li.append(Cell(row=i, col=field_i, value=values[field]))
        else:
            cells_li.append(Cell(row=i, col=field_i, value="-"))
        field_i += 1

    i += 1
general_sheet.update_cells(cells_li)
