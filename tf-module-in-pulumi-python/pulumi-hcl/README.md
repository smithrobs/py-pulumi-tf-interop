# Same module, via pulumi-hcl

The parent directory consumes `modules/app-segment` with the `terraform-module`
package. This directory consumes the same module with
[pulumi-hcl](https://github.com/pulumi/pulumi-hcl), as a multi-language component (MLC).

## What differs from the parent

| | parent (`terraform-module`) | here (`pulumi-hcl`) |
|---|---|---|
| Module change | none | adds `modules/app-segment/PulumiPlugin.yaml` (`runtime: hcl`) |
| Register SDK | `pulumi package add terraform-module ./modules/app-segment appsegment` | `pulumi package add ./modules/app-segment` |
| Python import | `pulumi_appsegment` | `pulumi_app_segment` (named after the directory) |
| Module executed by | Terraform module provider | pulumi-hcl's HCL interpreter |
| Pulumi state | one `Module` resource | `Module` component with `random:index:Id` children as real resources |

`__main__.py` is otherwise identical.

## Run

    python3 -m venv venv
    pulumi package add ./modules/app-segment   # generates sdks/ (git-ignored)
    pulumi up
