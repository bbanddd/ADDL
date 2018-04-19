#!/usr/bin/env Rscript

local({r <- getOption("repos")
       r["CRAN"] <- "https://mirrors.ustc.edu.cn/CRAN"
       options(repos = r)
})

source("https://neuroconductor.org/neurocLite.R")
neuroc_install("extrantsr")
