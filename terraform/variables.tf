locals {
    data_lake_bucket = "data_lake_ny_taxi"
}

variable "project" {
    description = "Project ID"
    default = "ny-taxi-data-project-386814"
    type = string
}

variable "region" {
    description = "Region for GCP resources"
    default = "southamerica-east1"
    type = string
}

variable "zone" {
    description = "Zone"
    default = "southamerica-east1-b"
    type = string
}

variable "storage_class" {
    description = "Storage class type for your bucket"
    default = "STANDARD"
}

variable "vm_name" {
    description = "Name for VM instance"
    default = "ny-taxi-data-instance"
    type = string
}

variable "machine_type" {
    description = "Machine type for VM instance"
    default = "e2-standard-4"
    type = string
}

variable "vm_image" {
  description = "Image for VM instance"
  default = "ubuntu-2004-lts"
  type = string
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset"
  type = string
  default = "nytaxi_bq"
}