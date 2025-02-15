# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
from unittest.mock import patch

import pytest
from interface_tester import InterfaceTester
from ops.pebble import Layer
from scenario.state import Container, State

from charm import TempoCharm


# Interface tests are centrally hosted at https://github.com/canonical/charm-relation-interfaces.
# this fixture is used by the test runner of charm-relation-interfaces to test traefik's compliance
# with the interface specifications.
# DO NOT MOVE OR RENAME THIS FIXTURE! If you need to, you'll need to open a PR on
# https://github.com/canonical/charm-relation-interfaces and change traefik's test configuration
# to include the new identifier/location.
@pytest.fixture
def interface_tester(interface_tester: InterfaceTester):
    with patch("charm.KubernetesServicePatch"):
        interface_tester.configure(
            charm_type=TempoCharm,
            state_template=State(
                leader=True,
                containers=[
                    # unless the traefik service reports active, the
                    # charm won't publish the ingress url.
                    Container(
                        name="tempo",
                        can_connect=True,
                        layers={
                            "foo": Layer(
                                {
                                    "summary": "foo",
                                    "description": "bar",
                                    "services": {
                                        "tempo": {
                                            "startup": "enabled",
                                            "current": "active",
                                            "name": "tempo",
                                        }
                                    },
                                    "checks": {},
                                }
                            )
                        },
                    )
                ],
            ),
        )
        yield interface_tester
