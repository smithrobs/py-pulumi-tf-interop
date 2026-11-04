# Pulumi program written in HCL (Pulumi.yaml specifies runtime: hcl)
#
# `pulumi package add ./appsegments` generated a local SDK for the Python
# component and recorded it in Pulumi.yaml. The component's resource token
# appsegments:index:AppSegmentGroup is referenced in HCL as the resource type
# `appsegments_app_segment_group`.
#
# As an end user, you only need to run `pulumi install` once.

terraform {
  required_providers {
    appsegments = {
      source = "pulumi/appsegments"
    }
  }
}

# Config is simple, declarative HCL. All the expansion logic lives in Python.
# A list-of-objects input surfaces in HCL as repeated nested blocks.
resource "appsegments_app_segment_group" "main" {
  segments {
    name     = "web"
    domains  = ["app.example.com", "www.example.com"]
    port     = 443
    protocol = "HTTPS"
  }
  segments {
    name     = "api"
    domains  = ["api.example.com"]
    port     = 8443
    protocol = "HTTPS"
  }
}

# Read the component's outputs back out.
output "segment_ids" {
  value = appsegments_app_segment_group.main.segment_ids
}

output "policy_count" {
  value = appsegments_app_segment_group.main.policy_count
}
