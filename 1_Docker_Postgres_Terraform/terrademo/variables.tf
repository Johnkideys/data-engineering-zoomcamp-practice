variable "project" {
    description = "Project"
    default =  "terraform-demo-484521"
}

variable "region" {
    description = "Region"
    default = "us-central1"
}

variable "location" {
    description = "Project Location"
    default =  "US"
}

variable "bq_dataset_name" {
    description = "My Bigquery dataset name"
    default =  "demo_dataset"
}

variable "gcs_bucket_name" {
    description = "My Bucket storage name"
    default =  "terraform-demo-484521-terrademo-example-bucket"
}

variable "gcs_storage_class" {
    description = "Bucket storage class"
    default =  "STANDARD"
}