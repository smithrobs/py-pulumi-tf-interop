# Use a Python component from Pulumi HCL

A Pulumi program written in **HCL** (`main.tf`, `runtime: hcl`) that consumes a
Pulumi **component authored in Python** (`appsegments/`). `pulumi package add`
infers a schema from the component's Python type annotations and generates an
HCL SDK, so HCL can call the component like any resource.

The component takes a list of structured "app segments" (`name`, `domains`,
`port`, `protocol`) and expands each into child resources. Config is declarative
in HCL; the main logic is in Python (`appsegments/app_segments.py`).

Only the `random` provider is used; no cloud account is needed.

## How this maps to Terraform
- A Pulumi **stack** ≈ a Terraform workspace.
- The Python **component** ≈ a reusable Terraform module, but authored in a real
  language: the `segments { ... }` blocks in `main.tf` are the module's inputs,
  and `.segment_ids` / `.policy_count` are its outputs.
- A list-of-objects input surfaces in HCL as **repeated nested blocks**.

## Prerequisites
- Pulumi CLI (a recent version e.g. **3.273.0**)
- Python **3.9+** (tested 3.13)

## Run it
```bash
export PULUMI_CONFIG_PASSPHRASE=dev
pulumi login --local

pulumi install        # regenerates sdks/ + the component's appsegments/venv from Pulumi.yaml
pulumi stack init dev
pulumi preview        # 7 resources to create
pulumi up --yes
pulumi stack output   # segment_ids, policy_count
pulumi destroy --yes
```

### NOTE:
> `pulumi install` prints `error: ...exited prematurely...` while it re-extracts
> the component schema. It is cosmetic — the command exits 0 and the SDK is
> generated; `preview`/`up` work normally.

Expected `up` output: `policy_count: 3` and `segment_ids` (map `web`/`api` → hex IDs).

## The component was first added with
```bash
pulumi package add ./appsegments
```
This recorded `packages: { appsegments: ./appsegments }` in `Pulumi.yaml`;
`pulumi install` replays it on a fresh clone.
