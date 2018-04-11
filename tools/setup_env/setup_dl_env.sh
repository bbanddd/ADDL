#!/usr/bin/env bash

function setup_dl_env_variables()
{
  # CUDA suits
  if ! grep "cuda/bin" $HOME/.bashrc > /dev/null ; then
    echo "export PATH=\"/usr/local/cuda/bin:\$PATH\"" >> $HOME/.bashrc
  fi
  if ! grep "cuda/lib64" $HOME/.bashrc > /dev/null ; then
    echo "export LD_LIBRARY_PATH=\"/usr/local/cuda/lib64:\$LD_LIBRARY_PATH\"" \
    >> $HOME/.bashrc
  fi
  if ! grep "CUDA_HOME" $HOME/.bashrc > /dev/null ; then
    echo "export CUDA_HOME=\"/usr/local/cuda\"" >> $HOME/.bashrc
  fi
  # Anaconda2
  if ! grep "anaconda2/bin" $HOME/.bashrc > /dev/null ; then
    echo "export PATH=\"$HOME/anaconda2/bin:\$PATH\"" >> $HOME/.bashrc
    source $HOME/.bashrc
  fi
  source $HOME/.bashrc
}

function conda_install()
{
  if ! [ -e $HOME/anaconda2/bin/conda ] ; then
    bash pkg/Anaconda2-5.1.0-Linux-x86_64.sh -b
  fi
}

function conda_update_repo_mirror()
{
  conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  conda config --set show_channel_urls yes
}

function setup_dl_env()
{
  setup_dl_env_variables
  conda_install
  conda_update_repo_mirror
  conda upgrade -y --all
  if ! pip list | grep tensorflow-gpu > /dev/null ; then
    pip install pkg/tensorflow_gpu-1.6.0-cp27-none-linux_x86_64.whl
  fi
  if ! pip list | grep tflearn > /dev/null ; then
    pip install tflearn
  fi
  if ! pip list | grep nibabel > /dev/null ; then
      pip install nibabel
  fi
  if ! pip list | grep opencv-python > /dev/null ; then
      pip install opencv-python
  fi
}

setup_dl_env