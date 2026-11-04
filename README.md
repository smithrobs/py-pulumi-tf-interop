# Pulumi ⇄ Terraform interop (two-way)

Small POCs showing Pulumi and Terraform/HCL code reusing each
other's building blocks. Both use only the `random` provider, so no cloud
account is needed.

| Directory | Direction | Summary |
|---|---|---|
| [`tf-module-in-pulumi-python/`](tf-module-in-pulumi-python/) | Terraform → Pulumi | A Pulumi **Python** program consumes a local **Terraform module** through a generated, typed SDK (`pulumi package add terraform-module`). Also includes a `pulumi-hcl` variant. |
| [`python-component-in-hcl/`](python-component-in-hcl/) | Pulumi → Terraform | A Pulumi program written in **HCL** consumes a Pulumi **component authored in Python**, which is exposed to HCL as a generated SDK. |

Each directory has its own README with prerequisites and run instructions.
