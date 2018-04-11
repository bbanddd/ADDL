#!/usr/bin/env Rscript

## set a CRAN mirror
local({r <- getOption("repos")
       r["CRAN"] <- "https://mirrors.ustc.edu.cn/CRAN"
       options(repos = r)
})

pkgCheckInstall <- function(x)
{
  if(!require(x, character.only = TRUE)){
    install.packages(x, dep=TRUE)
  }
}

pkgCheckInstall("optparse")