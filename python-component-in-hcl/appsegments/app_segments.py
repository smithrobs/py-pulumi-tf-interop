"""A Pulumi component, written in Python, that an HCL program consumes.

The component takes a list of "app segment" definitions (the kind of structured
config you'd keep as JSON or HCL) and expands each one into child resources. All
the reshaping logic lives here in Python; the caller only supplies data.

Only the credential-free `random` provider is used, so this runs with no cloud
account. Swap `random` for a real provider (e.g. Zscaler) and the shape is the
same: data in, resources out, typed outputs back.
"""

from typing import Mapping, Optional, Sequence, TypedDict

import pulumi
import pulumi_random as random


class AppSegment(TypedDict):
    """One application segment definition."""

    name: pulumi.Input[str]
    """Logical name of the segment."""
    domains: pulumi.Input[Sequence[pulumi.Input[str]]]
    """FQDNs that belong to this segment."""
    port: pulumi.Input[int]
    """Port the segment listens on."""
    protocol: Optional[pulumi.Input[str]]
    """Protocol label (defaults to "HTTPS")."""


class AppSegmentGroupArgs(TypedDict):
    """Inputs for the component: just the list of segments."""

    segments: pulumi.Input[Sequence[pulumi.Input[AppSegment]]]


class AppSegmentGroup(pulumi.ComponentResource):
    """Expands a list of app segments into per-segment and per-domain resources."""

    segment_ids: pulumi.Output[Mapping[str, str]]
    """Map of segment name -> allocated segment ID."""
    policy_count: pulumi.Output[int]
    """Total number of per-domain policy resources created."""

    def __init__(self, name: str, args: AppSegmentGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("appsegments:index:AppSegmentGroup", name, {}, opts)

        child_opts = pulumi.ResourceOptions(parent=self)
        segment_ids: dict[str, pulumi.Output[str]] = {}
        policy_count = 0

        # The "heavy lifting": iterate the structured config and create resources.
        for segment in args["segments"]:
            seg_name = segment["name"]

            # One stable identifier per segment.
            seg_id = random.RandomId(
                f"{name}-{seg_name}-id",
                byte_length=6,
                keepers={"port": str(segment["port"])},
                opts=child_opts,
            )
            segment_ids[seg_name] = seg_id.hex

            # One "policy" resource per domain, showing the list expanding into
            # N child resources.
            for domain in segment["domains"]:
                random.RandomPet(
                    f"{name}-{seg_name}-{domain}-policy",
                    keepers={"domain": domain},
                    opts=child_opts,
                )
                policy_count += 1

        self.segment_ids = pulumi.Output.all(**segment_ids)
        self.policy_count = pulumi.Output.from_input(policy_count)
        self.register_outputs({
            "segment_ids": self.segment_ids,
            "policy_count": self.policy_count,
        })
