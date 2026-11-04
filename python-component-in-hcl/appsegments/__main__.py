"""Entry point for the component plugin.

`pulumi package add ./appsegments` runs this to infer the schema from the
component's type annotations, then generates an SDK in the consumer's language.
"""

from pulumi.provider.experimental import component_provider_host

from app_segments import AppSegmentGroup

if __name__ == "__main__":
    component_provider_host(components=[AppSegmentGroup], name="appsegments")
