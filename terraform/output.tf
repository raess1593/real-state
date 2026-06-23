output bucket_name {
  value       = aws_s3_bucket.raw_data_bucket.bucket
  sensitive   = true
  description = "The name of the S3 bucket where raw data is stored."
  depends_on  = [aws_s3_bucket.raw_data_bucket]
}   
