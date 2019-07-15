#!/bin/bash

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -eo pipefail

cd github/google-cloud-python

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Debug: show build environment
env | grep KOKORO

# Setup firestore account credentials
export FIRESTORE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/firebase-credentials.json

# Setup service account credentials.
export GOOGLE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/service-account.json

# Setup project id.
export PROJECT_ID=$(cat "${KOKORO_GFILE_DIR}/project-id.json")

# Setup API Key for Videointelligence VPC SC tests
gcloud kms decrypt \
  --location=global \
  --keyring=kokoro \
  --key=kokoro-environment \
  --ciphertext-file=${KOKORO_GFILE_DIR}/videointelligence_vpcsc_outside_perimeter_project_api_key.enc \
  --plaintext-file=videointelligence_vpcsc_outside_perimeter_project_api_key.dec
export VIDEOINTELLIGENCE_VPCSC_OUTSIDE_PERIMETER_PROJECT_API_KEY=$(cat videointelligence_vpcsc_outside_perimeter_project_api_key.dec)

# GitHub token (this token has no scopes and is read-only)
gcloud kms decrypt \
  --location=global \
  --keyring=kokoro \
  --key=kokoro-environment \
  --ciphertext-file=${KOKORO_GFILE_DIR}/diff_checker_github_key.enc \
  --plaintext-file=diff_checker_github_key.dec
export TARGET_PACKAGES_GITHUB_TOKEN=$(cat diff_checker_github_key.dec)

# Find out if this package was modified.
python3.6 test_utils/scripts/get_target_packages_kokoro.py > ~/target_packages
cat ~/target_packages

if [[ ! -n $(grep -x "$PACKAGE" ~/target_packages) ]]; then
    echo "$PACKAGE was not modified, returning."
    exit;
fi

cd "$PACKAGE"

# Remove old nox
python3.6 -m pip uninstall --yes --quiet nox-automation

# Install nox
python3.6 -m pip install --upgrade --quiet nox
python3.6 -m nox --version

python3.6 -m nox
