#!/usr/bin/Rscript
library(httr)
suppressPackageStartupMessages(library(Matrix))

args = commandArgs(trailingOnly=TRUE)

print(paste("importing",args[1]))
mat <- readRDS(args[1])
print("read rds file")


# df <- data.frame(gene=rownames(mat)[df$i], cell=colnames(mat)[df$j], expression=df$x)
# print("built data frame")


chunk_size <- 10000
rows <- 40000 # nrow(df)

for (i in seq(1, rows, chunk_size)) {
	seq_size <- chunk_size
	if ((i + seq_size) > rows) seq_size <- rows - i + 1

	chunk_data <- list()

	for (j in seq(1, seq_size)) {
		row <- j + i
		temp_df <- as.data.frame(as.matrix(mat[row,]))
		gene_data <- do.call("mapply", c(list, temp_df[temp_df$expression > 0,], SIMPLIFY = FALSE, USE.NAMES=FALSE))
		gene_name <- rownames(mat)[row]
		chunk_data[[gene_name]] <- gene_data
	}

	# 45 sec per 10000
	# 375 hour per 300,000,000
	#POST("localhost:5000/cell_gene", body = temp_df, encode = "json")
}

