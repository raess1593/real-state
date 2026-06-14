# Raw Data S3 Bucket

resource "aws_s3_bucket" "raw_data_bucket" {
  bucket = var.raw_data_bucket_name

  tags = merge(
    local.tags,
    { Name = "${local.name_prefix}-raw-data" }
  )
}

resource "aws_s3_bucket_versioning" "raw_data_bucket_versioning" {
  bucket = aws_s3_bucket.raw_data_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "raw_data_bucket_encryption" {
  bucket = aws_s3_bucket.raw_data_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "raw_data_bucket_public_access_block" {
  bucket = aws_s3_bucket.raw_data_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}