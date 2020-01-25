## Example

fdisk /dev/vda # And then press n
vgextend VolGroup01 /dev/vda...
lvextend -L +10G /dev/mapper/VolGroup01-root
resize2fs /dev/mapper/VolGroup01-root
xfs_growfs /
