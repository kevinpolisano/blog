args <- commandArgs(trailingOnly = TRUE)
file <- args[1]

if (requireNamespace("rstudioapi", quietly = TRUE)) {
  rstudioapi::viewer(file)
} else {
  message("Le package 'rstudioapi' n'est pas installé.")
}

