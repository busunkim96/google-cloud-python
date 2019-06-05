# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate Grafeas GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "grafeas", "v1", config_path="/grafeas/artman_grafeas_v1.yaml", include_protos=True
)

excludes = ["README.rst", "nox.py", "setup.py", "docs/index.rst"]

# Make 'grafeas' a namespace
s.move(library / "grafeas", excludes=["__init__.py"])
s.move(library / "docs", excludes=["conf.py", "index.rst"])
s.move(
    library / "google/cloud/grafeas_v1/proto",
    "grafeas/grafeas_v1/proto",
    excludes=excludes,
)
s.move(library / "tests")


# Fix proto imports
s.replace(
    ["grafeas/**/*.py", "tests/**/*.py"],
    "from grafeas\.v1( import \w*_pb2)",
    "from grafeas.grafeas_v1.proto\g<1>",
)
s.replace(
    "grafeas/**/*_pb2.py",
    "from grafeas_v1\.proto( import \w*_pb2)",
    "from grafeas.grafeas_v1.proto\g<1>",
)
s.replace(
    "grafeas/**/grafeas_pb2_grpc.py",
    "from grafeas_v1\.proto",
    "from grafeas.grafeas_v1.proto",
)

# Make package name 'grafeas'
s.replace(
    "grafeas/grafeas_v1/gapic/grafeas_client.py", "google-cloud-grafeas", "grafeas"
)

# Fix docstrings with no summary lines
s.replace(
    "grafeas/grafeas_v1/proto/vulnerability_pb2.py",
    r"""(\s+)__doc__ = \"\"\"Attributes:""",
    """\g<1>__doc__=\"\"\"
    Attributes:""",
)

# Replace mentions of 'Container Analysis' with 'Grafeas' in the docs
s.replace("docs/**/v*/*.rst", "Container Analysis", "Grafeas")


# # ----------------------------------------------------------------------------
# # Remove google-specific portions of library
# # ----------------------------------------------------------------------------
# # Remove default endpoint (service address).
# s.replace(
#     "grafeas/**/grafeas_client.py",
#     r"""    SERVICE_ADDRESS = 'containeranalysis\.googleapis\.com:443'
#     \"\"\"The default address of the service\.\"\"\"""",
#     "",
# )

# # Don't set a default service address in the transport
# s.replace(
#     "grafeas/**/grafeas_grpc_transport.py",
#     """    def __init__\(self, channel=None, credentials=None,
#                  address='containeranalysis.googleapis.com:443'\):""",
#     "    def __init__(self, address, channel=None, credentials=None):",
# )
# s.replace(
#     "grafeas/**/grafeas_grpc_transport.py",
#     r"""    def create_channel\(
#                 cls,
#                 address='containeranalysis\.googleapis\.com:443',
#                 credentials=None\):""",
#     """    def create_channel(
#                 cls,
#                 address,
#                 credentials=None):""",
# )

# # Make transport required, since we aren't providing default credentials
# # or endpoint.
# s.replace("grafeas/**/grafeas_client.py", "transport=None,", "transport,")
# s.replace(
#     "grafeas/**/grafeas_client.py",
#     r"""        if transport:
#             if callable\(transport\):
#                 self\.transport = transport\(
#                     credentials=credentials,
#                     default_class=grafeas_grpc_transport.GrafeasGrpcTransport,
#                 \)
#             else:
#                 if credentials:
#                     raise ValueError\(
#                         'Received both a transport instance and '
#                         'credentials; these are mutually exclusive\.'
#                     \)
#                 self\.transport = transport
#         else:
#             self\.transport = grafeas_grpc_transport.GrafeasGrpcTransport\(
#                 address=self\.SERVICE_ADDRESS,
#                 channel=channel,
#                 credentials=credentials,
#             \)""",
#     """        if callable(transport):
#             self.transport = transport(
#                 credentials=credentials,
#                 default_class=grafeas_grpc_transport.GrafeasGrpcTransport,
#             )
#         else:
#             if credentials:
#                 raise ValueError(
#                     "Received both a transport instance and "
#                     "credentials; these are mutually exclusive."
#                 )
#             self.transport = transport""",
# )



# # Remove OAuth Scope from Transport
# s.replace(
#     "grafeas/**/grafeas_grpc_transport.py",
#     """    # The scopes needed to make gRPC calls to all of the methods defined
#     # in this service.
#     _OAUTH_SCOPES = \(
#         'https://www.googleapis.com/auth/cloud-platform',
#     \)""",
#     "    _OAUTH_SCOPES = ()",
# )


# # TODO: Fix client instanatiation in tests

# # Fix snippets showing client initialization.

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=78, cov_level=78)
s.move(templated_files, excludes=["noxfile.py"])

# s.shell.run(["nox", "-s", "blacken"], hide_output=False)
