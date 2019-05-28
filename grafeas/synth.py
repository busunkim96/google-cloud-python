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
# Generate grafeas GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "grafeas",
    "v1",
    config_path="/grafeas/artman_grafeas_v1.yaml",
    include_protos=True,
)

#excludes = ["README.rst", "nox.py", "setup.py", "docs/index.rst"]
s.move(library / "docs", excludes=None)
s.move(library / "grafeas_v1", "grafeas/grafeas_v1", excludes=None)
s.move(library / "grafeas.py", "grafeas")
s.move(library / "google/cloud/grafeas_v1/proto", "grafeas/grafeas_v1/proto", excludes=None)
s.move(library / "tests", excludes=None)
s.move(library / "README.rst")

# Replacements to fix namespace

s.replace(["grafeas/**/*.py","tests/**/*.py"], "(import|from) (grafeas\.v1|grafeas_v1)", "\g<1> grafeas.grafeas_v1")
s.replace(["grafeas/**/*.py", "tests/**/*.py"], "from grafeas\.grafeas_v1 (import .*_pb2)", "from grafeas.grafeas_v1.proto \g<1>")
# s.replace("grafeas/**/*/*_pb2.py", "((name|package)=(\"|\'))grafeas(\.|_)v1", "\g<1>grafeas.grafeas_v1")
s.replace("docs/**/*.rst", "grafeas_v1", "grafeas.grafeas_v1")

# change package name
s.replace("grafeas/**/grafeas_client.py", "google-cloud-grafeas", "grafeas")

# Missing summary line error
s.replace("grafeas/**/*.py", "__doc__ = \"\"\"Attributes:", "__doc__ = \"\"\"\nAttributes:")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files, excludes=["noxfile.py"])

# s.shell.run(["nox", "-s", "blacken"], hide_output=False)