#!/usr/bin/env Rscript

library(optparse)

option_list <- list(
  make_option(c("-r", "--repo"), action="store",
              default="https://mirrors.ustc.edu.cn/CRAN",
              help="The CRAN mirror address.[default: %default]"),
  make_option(c("-n", "--ncpu"), action="store", type="integer",default=1,
              help="The number of parallel threads for source package install.[default: %default]")
)

opt <- parse_args(OptionParser(option_list=option_list))

pkgCheckInstall <- function(x)
{
  if(!require(x, character.only = TRUE)){
    install.packages(x, repos = opt$r, dependencies = TRUE, Ncpus = opt$n)
  }
}

pkgCheckInstall("bitops")
pkgCheckInstall("abind")
pkgCheckInstall("neurobase")
pkgCheckInstall("matrixStats")
pkgCheckInstall("R.utils")
pkgCheckInstall("rgl")
pkgCheckInstall("R.matlab")
pkgCheckInstall("neuroim")
pkgCheckInstall("magic")
pkgCheckInstall("psych")
pkgCheckInstall("rsvd")
pkgCheckInstall("RcppEigen")
pkgCheckInstall("WhiteStripe")
pkgCheckInstall("fslr")
pkgCheckInstall("oro.nifti")