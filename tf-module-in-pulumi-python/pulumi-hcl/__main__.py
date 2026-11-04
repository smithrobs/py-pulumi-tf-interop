"""Consume a local HCL module from Pulumi Python via pulumi-hcl.

Same program as ../__main__.py, but the module is a pulumi-hcl multi-language
component (it has a PulumiPlugin.yaml with `runtime: hcl`) instead of a plain
Terraform module wrapped by the terraform-module provider.

`pulumi package add ./modules/app-segment` generated the typed
`pulumi_app_segment` SDK below.
"""

import pulumi
import pulumi_app_segment as app_segment

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

# Each Module(...) is a ComponentResource whose children (the random_id
# resources) are registered in Pulumi state by the HCL interpreter.
modules = {
    seg_name: app_segment.Module(
        seg_name,
        name=seg_name,
        domains=cfg["domains"],
        port=cfg["port"],
    )
    for seg_name, cfg in segments.items()
}

pulumi.export(
    "segment_ids",
    {name: mod.segment_id for name, mod in modules.items()},
)
pulumi.export("web_policy_ids", modules["web"].domain_policy_ids)
pulumi.export("web_listen_port", modules["web"].listen_port)
