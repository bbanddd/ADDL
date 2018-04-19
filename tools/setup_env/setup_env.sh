#!/usr/bin/env bash

pkg_fsl=fslinstaller.py
pkg_fsl_archived=fsl-5.0.10-centos7_64.tar.gz
pkg_itkr=ITKR_0.4.12_R_x86_64-pc-linux-gnu.tar.gz
pkg_antsr=ANTsR_0.6.1_R_x86_64-pc-linux-gnu.tar.gz
pkg_antsrcore=ANTsRCore_0.4.2.1_R_x86_64-pc-linux-gnu.tar.gz


function rpm_pkg_check_yum_install()
{
  #############################################################################
  # $1: package name                                                          #
  #############################################################################
  echo "# $0 INFO: rpm_pkg_check_yum_install $1 start."
  if ! [ $# -eq 1 ] ; then
    echo "# $0 ERROR: rpm_pkg_check_yum_install expect one argument."
    exit 1
  fi
  if yum info $1 | grep ^Error > /dev/null ; then
    echo "# $0 ERROR: rpm_pkg_check_yum_install no match package for $1."
    exit 1
  fi
  _tmp_v=$(yum info $1 | grep -m 1 ^Version | cut -d : -f 2 | cut -d " " -f 2)
  if echo $1 | grep $_tmp_v 2>&1 /dev/null ; then
    # $1 contains version info, which means user hint.
    if ! rpm -qa | grep ^$1 > /dev/null ; then
      yum install -y $1 > /dev/null
    fi
  else
    # $1 does not contain version info, need version appending package name.
    if ! rpm -qa | grep ^$1-$_tmp_v > /dev/null ; then
      yum install -y $1 > /dev/null
    fi
  fi
  echo "# $0 INFO: rpm_pkg_check_yum_install $1 end."
  echo
}

function firewall_port_check_enable()
{
  #############################################################################
  # $1: port of firewall, e.g. 8800/tcp                                       #
  #############################################################################
  echo "# $0 INFO: firewall_port_check_enable $1 start."
  if ! [ $# -eq 1 ] ; then
    echo "# $0 ERROR: firewall_port_check_enable expect one argument."
    exit 1
  fi
  if ! firewall-cmd --query-port=$1 | grep yes > /dev/null ; then
    firewall-cmd --zone=public --add-port=$1 --permanent > /dev/null
    firewall-cmd --reload > /dev/null
  fi
  echo "# $0 INFO: firewall_port_check_enable $1 end."
  echo
}

function check_install_centos7_mini_pending_suits()
{
  rpm_pkg_check_yum_install tree
  rpm_pkg_check_yum_install emacs-nox
  rpm_pkg_check_yum_install subversion
  rpm_pkg_check_yum_install wget
  rpm_pkg_check_yum_install git
  rpm_pkg_check_yum_install bzip2
  rpm_pkg_check_yum_install screen
  rpm_pkg_check_yum_install kernel-devel-$(uname -r)
  rpm_pkg_check_yum_install kernel-headers-$(uname -r)
  rpm_pkg_check_yum_install libXmu-devel
  rpm_pkg_check_yum_install libXi-devel
  rpm_pkg_check_yum_install libcurl-devel
  rpm_pkg_check_yum_install openssl-devel
  rpm_pkg_check_yum_install libpng-devel
  rpm_pkg_check_yum_install libX11-devel
  rpm_pkg_check_yum_install mesa-libGL-devel
  rpm_pkg_check_yum_install mesa-libGLU-devel
  rpm_pkg_check_yum_install ImageMagick-c++-devel
  rpm_pkg_check_yum_install gcc
  rpm_pkg_check_yum_install gcc-c++
  rpm_pkg_check_yum_install epel-release
  rpm_pkg_check_yum_install R
}

function disable_nouveau()
{
  touch /etc/modprobe.d/blacklist-nouveau.conf
  echo "
blacklist nouveau
options nouveau modeset=0" > /etc/modprobe.d/blacklist-nouveau.conf
  mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
  dracut -v /boot/initramfs-$(uname -r).img $(uname -r)
}

function check_and_disable_nouveau()
{
  if lsmod | grep nouveau > /dev/null ; then
    echo "Detected the Nouveau kernel driver, goto following step:"
    echo "  1) Remove Nouveau kernel driver."
    echo "  2) Reboot system."
    echo
    disable_nouveau
    reboot
  fi
}

function check_install_nvidia_driver()
{
  echo "# $0 INFO: Check and install NVIDIA driver."
  if rpm -qa | grep nvidia > /dev/null ; then
    yum -y remove nvidia*
  fi
  if ! lsmod | grep nvidia > /dev/null ; then
    check_and_disable_nouveau

    bash pkg/NVIDIA-Linux-x86_64-390.25.run --silent
  fi
  echo
}

function check_install_cuda()
{
  echo "# $0 INFO: Check and install CUDA 9.0."
  if ! [ -e /usr/local/cuda/version.txt ] ; then
    bash pkg/cuda_9.0.176_384.81_linux.run --silent
  fi
  echo

  echo "# $0 INFO: Install CUDA 9.0 patch 1."
  bash pkg/cuda_9.0.176.1_linux.run --silent --installdir=/usr/local/cuda      \
                                    --accept-eula > /dev/null
  echo

  echo "# $0 INFO: Install CUDA 9.0 patch 2."
  bash pkg/cuda_9.0.176.2_linux.run --silent --installdir=/usr/local/cuda      \
                                    --accept-eula > /dev/null
  echo
}

function check_install_cudnn()
{
  echo "# $0 INFO: Check and install cuDNN."
  if ! [ -e /usr/local/cuda/lib/libcudnn.so ] ; then
    tar xzvf pkg/cudnn-9.0-linux-x64-v7.tgz -C /usr/local > /dev/null
  fi
  echo
}

function check_install_nvidia_suits()
{
  check_install_nvidia_driver
  check_install_cuda
  check_install_cudnn
}

function check_install_dl_framework_suits()
{
  echo "# $0 INFO: Check and install anaconda2."
  if ! [ -e $HOME/anaconda2/bin/conda ] ; then
    su -s /bin/bash -c "bash setup_dl_env.sh" python2
  fi
  echo
}

function check_install_fsl_antsr_suits()
{

  echo "Check and install FSL."
  if ! [ -e /usr/local/fsl/bin/fsl ] ; then
    python pkg/$pkg_fsl -f pkg/$pkg_fsl_archived -M -d /usr/local/fsl -q
  fi
  echo

  echo "Check and install a pending R library for following scripts."
  Rscript install_optparse.r > /dev/null
  echo

  echo "Check and install pending R libraries for ANTsR."
  Rscript install_tools.r -n $(nproc --all) > /dev/null
  echo

  echo "Check and install ITKR."
  if ! R CMD Rscript -e 'installed.packages()[,c(0)]' | grep ITKR ; then
    R CMD INSTALL pkg/$pkg_itkr > /dev/null
  fi
  echo 

  echo "Check and install ANTsRCore."
  if ! R CMD Rscript -e 'installed.packages()[,c(0)]' | grep ANTsRCore ; then
    R CMD INSTALL pkg/$pkg_antsrcore > /dev/null
  fi
  echo

  echo "Check and install ANTsR."
  if ! R CMD Rscript -e 'installed.packages()[,c(0)]' | grep "ANTsR " ; then
    R CMD INSTALL pkg/$pkg_antsr > /dev/null
  fi
  echo

  echo "Check and install extrantsr."
  if ! R CMD Rscript -e 'installed.packages()[,c(0)]' | grep extrantsr ; then
    Rscript install_extrantsr.r
  fi
  echo
}

function post_config()
{
  # Enable firewall 6006 port for TensorBoard
  firewall_port_check_enable 6006/tcp
}

function main()
{
  check_install_centos7_mini_pending_suits
  check_install_nvidia_suits
  check_install_dl_framework_suits
  check_install_fsl_antsr_suits
  post_config
}

if [ "root" = $(whoami) ] ; then
  main
else
  echo "Please launch this script with root permission.[sudo]"
fi