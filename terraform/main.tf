terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

# Provider block
provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

# Resource block
# VM
resource "google_compute_instance" "vm_instance" {
  provider     = google
  name         = var.vm_name
  machine_type = var.machine_type

  boot_disk {
    initialize_params {
      image = var.vm_image
    }
  }
  network_interface {
    network = "default"
    access_config {
    }
  }
}

# GCS
resource "google_storage_bucket" "data-lake-bucket" {
  name     = "${local.data_lake_bucket}_${var.project}"
  location = var.region

  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}

# DWH
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET[0]
  project    = var.project
  location   = var.region
}

resource "google_bigquery_dataset" "dataset_stag" {
  dataset_id = var.BQ_DATASET[1]
  project    = var.project
  location   = var.region
}

resource "google_bigquery_dataset" "dataset_prod" {
  dataset_id = var.BQ_DATASET[2]
  project    = var.project
  location   = var.region
}

# Artifact
resource "google_artifact_registry_repository" "ny-taxi-container-registry" {
  location      = var.region
  repository_id = var.registry_id
  format        = "DOCKER"
}
