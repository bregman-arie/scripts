#!/bin/bash

echo "Updating the system...this might take a while"""
sudo dnf -y update

echo "Install packages"
sudo dnf install -y xchat-gnome NetworkManager-openvpn NetworkManager-openvpn-gnome smartctl git git-review virtualenv redhat-rpm-config python-pip python-devel libffi-devel openssl-devel gcc-c++ libtool

echo "Install oh-my-zsh"
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

# CI packages
while true; do
    read -p "Do you wish to install CI/CD packages? [Yy/Nn]" ci_install
    case $ci_install in
        [Yy]* ) sudo dnf install -y groovy python-jenkins-jobs-builder; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Web development
while true; do
    read -p "Do you wish to install web development packages? [Yy/Nn]" web_install
    case $web_install in
        [Yy]* ) sudo npm install -g bower; sudo npm install -g grunt-cli break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Web development

echo "VIM time!"
sudo dnf install vim ctags
wget https://raw.githubusercontent.com/tao12345666333/vim/master/vimrc -O $HOME/.vimrc
echo "Plugin 'andviro/flake8-vim'" >> $HOME/.vimrc
vim -E -u $HOME/.vimrc +qall

# Extend zsh
echo "setopt extended_glob" >> ~/.zshrc

echo "System going to reboot in 5 seconds..."
sleep 5
reboot
