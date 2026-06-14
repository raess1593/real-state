# IAM user to modify S3 bucket

resource "aws_iam_user" "data_bucket_user" {
    name = "${local.name_prefix}-data-bucket-user"
}

resource "aws_iam_user_policy" "data_bucket_user_policy" {
    name = "${local.name_prefix}-data-bucket-user-policy"
    user = aws_iam_user.data_bucket_user.name

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ]
                Resource = [
                    "${aws_s3_bucket.raw_data_bucket.arn}",
                    "${aws_s3_bucket.raw_data_bucket.arn}/*"
                ]
            }
        ]
    })
}