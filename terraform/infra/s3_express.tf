data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_s3_directory_bucket" "iceberg_warehouse" {
  bucket = "cjmm-mds-lake-iceberg--${data.aws_availability_zones.available.zone_ids[0]}--x-s3"

  location {
    name = data.aws_availability_zones.available.zone_ids[0]
    type = "AvailabilityZone"
  }
}

output "s3_express_bucket_name" {
  value       = aws_s3_directory_bucket.iceberg_warehouse.bucket
  description = "S3 Express One Zone bucket name"
}

output "s3_express_warehouse_path" {
  value       = "s3://${aws_s3_directory_bucket.iceberg_warehouse.bucket}/warehouse/"
  description = "S3 Express warehouse path for Iceberg"
}
