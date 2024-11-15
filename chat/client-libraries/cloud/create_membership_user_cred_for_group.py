# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-apps-chat


# [START chat_create_membership_user_cred_for_group]
from authentication_utils import create_client_with_user_credentials
from google.apps import chat_v1 as google_chat

SCOPES = ["https://www.googleapis.com/auth/chat.memberships"]

# This sample shows how to create membership with user credential for a group
def create_membership_with_user_cred_for_group():
    # Create a client
    client = create_client_with_user_credentials(SCOPES)

    # Initialize request argument(s)
    request = google_chat.CreateMembershipRequest(
        # Replace SPACE_NAME here
        parent = "spaces/SPACE_NAME",
        membership = {
            "groupMember": {
                # Replace GROUP_NAME here
                "name": "groups/GROUP_NAME"
            }
        }
    )

    # Make the request
    response = client.create_membership(request)

    # Handle the response
    print(response)

create_membership_with_user_cred_for_group()

# [END chat_create_membership_user_cred_for_group]
