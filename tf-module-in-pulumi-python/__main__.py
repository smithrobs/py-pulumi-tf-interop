"""Consume a local Terraform module from Pulumi Python.

`pulumi package add terraform-module ./modules/app-segment appsegment` generated
the typed `pulumi_appsegment` SDK below. From Pulumi's point of view the module
is just another resource: we pass typed inputs in, and read its outputs back.
"""

import pulumi
import pulumi_appsegment as appsegment

# ---- Config stays plain data, the way a JSON/HCL config file would -----------
# In a real migration this might be read from a JSON file; the shape is the only
# thing that matters. The Python SDK gives IDE autocomplete on every field here.
segments = {
    "web": {
        "domains": ["app.example.com", "www.example.com"],
        "port": 443,
    },
    "api": {
        "domains": ["api.example.com"],
        "port": 8443,
    },
}

# ---- The Terraform handoff ---------------------------------------------------
# Each `appsegment.Module(...)` call runs the local Terraform module once, with
# the typed inputs declared in modules/app-segment/variables.tf. Pulumi manages
# the module's resources in its own state — no `terraform apply`, no tfstate.
modules = {
    seg_name: appsegment.Module(
        seg_name,
        name=seg_name,
        domains=cfg["domains"],
        port=cfg["port"],
    )
    for seg_name, cfg in segments.items()
}

# ---- Read the module's outputs back ------------------------------------------
# These are the outputs declared in modules/app-segment/outputs.tf, surfaced as
# strongly-typed Pulumi Outputs on the generated resource.
pulumi.export(
    "segment_ids",
    {name: mod.segment_id for name, mod in modules.items()},
)
pulumi.export(
    "web_policy_ids",
    modules["web"].domain_policy_ids,
)
pulumi.export(
    "web_listen_port",
    modules["web"].listen_port,
)
