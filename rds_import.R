#!/usr/bin/Rscript
library(httr)
suppressPackageStartupMessages(library(Matrix))

# benchmark 100 rows:
# chunk_size 10, threads = 4, entries = 4032674
# 303712 in 89.992 sec    300m in 24.7 hours
# 359332 in 119.429 sec   300m in 27.7 hours
# 348826 in 125.492 sec   300m in 29.9 hours
# 823793 in 187.611 sec   300m in 18.6 hours
# 


start.time <- proc.time()[[3]]

args = commandArgs(trailingOnly=TRUE)
threads = as.integer(args[2])
current_thread = as.integer(args[3])

cat("Thread", current_thread, "importing",args[1],"\n")
mat <- readRDS(args[1])
cat("Thread", current_thread, "read rds file\n")

chunk_size <- 5
rows <- 40 #nrow(mat)
chunk_data <- list()

start <- floor(rows * ((current_thread - 1) / threads)) + 1
end <- floor(rows * (current_thread / threads))
total_data_size <- 0

for (i in seq(start, end, chunk_size)) {
	seq_size <- chunk_size
	data_size <- 0
	if ((i + seq_size) > end) seq_size <- end - i + 1

	cat("Thread",current_thread,": building request data\n")
	for (j in seq(1, seq_size)) {
		row <- j + i - 1
		temp_df <- as.data.frame(as.matrix(mat[row,]))
		colnames(temp_df) <- c("expression")
		temp_df$cell <- rownames(temp_df)
		temp_df <- temp_df[temp_df$expression > 0,]
		if (nrow(temp_df) == 0) next
		gene_data <- do.call("mapply", c(list, temp_df, SIMPLIFY = FALSE, USE.NAMES=FALSE))
		gene_name <- rownames(mat)[row]
		chunk_data[[gene_name]] <- gene_data

		data_size <- data_size + length(gene_data)
	}
	total_data_size <- total_data_size + data_size
	# TODO: add filter_column and filter_data arguments to request body
	body <- list(data=chunk_data)

	api.start.time <- proc.time()[[3]]

	POST("localhost:8000/genes", body = body, encode = "json")

	api.end.time <- proc.time()[[3]]
	api.time.taken <- api.end.time - api.start.time
	cat("Thread",current_thread,": chunk",(((i-start)/chunk_size)+1),"/",
		ceiling((end-start+1)/chunk_size), "(size:", data_size, 
		"entries) sent to api in",api.time.taken,"sec\n")
	
}

end.time <- proc.time()[[3]] 
time.taken <- end.time - start.time
cat("Thread",current_thread,": total data sent:", total_data_size, "in",
	time.taken, "seconds; thats", (time.taken/total_data_size * 300000000 / 60
								   / 60),"hours for 300m!**********\n")
