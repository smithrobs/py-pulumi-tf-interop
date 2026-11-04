# A quick module that stands in for a more real resource
# (e.g. a Zscaler application segment). It allocates a stable
# identifier per segment and one policy ID per domain, using only the
# `random` provider so it runs with no cloud account.

terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5.0"
    }
  }
}

# One stable identifier for the segment.
resource "random_id" "segment" {
  byte_length = 6
  keepers = {
    name = var.name
    port = var.port
  }
}

# One "policy" ID per domain, to show the module expanding a list input
# into N resources.
resource "random_id" "policy" {
  for_each    = toset(var.domains)
  byte_length = 4
  keepers = {
    domain = each.value
  }
}
