#!/bin/bash
# Title: Install Marian
# Description: Commands taken from https://groups.google.com/g/marian-nmt/c/uQC6q1PIf3k/m/JGP_4B5NBwAJ?utm_medium=email&utm_source=footer

apt update
apt-get install -y git cmake build-essential libboost-all-dev libprotobuf10 protobuf-compiler libprotobuf-dev openssl libssl-dev libgoogle-perftools-dev doxygen
sudo apt remove cmake
sudo apt purge --auto-remove cmake
wget https://cmake.org/files/v3.12/cmake-3.12.3-Linux-x86_64.sh
sudo mkdir /opt/cmake
sudo sh cmake-3.12.3-Linux-x86_64.sh --prefix=/opt/cmake --skip-license
rm /usr/local/bin/cmake
sudo ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake
cmake --version
git clone https://github.com/marian-nmt/marian
cd marian && git rev-parse --short HEAD
rm -rf marian/build
mkdir -p marian/build
pwd
ldconfig
cd marian/build && cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_STATIC_LIBS=on
pwd
make -j1 -C marian/build