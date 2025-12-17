# Google Device Auth for Python

A lightweight Python client for the **Google OAuth 2.0 Device Authorization Flow**. 

This library is designed for **limited-input devices** (IoT, Raspberry Pi, Smart TVs) or **CLI tools** where a browser redirect is not possible. It handles the full flow: requesting codes, polling for user authorization, and saving credentials locally.

## Features
- **Headless Authentication:** No local browser required.
- **Automatic Polling:** Handles Google's polling intervals and rate limits (slow_down).
- **Session Persistence:** Saves Refresh Tokens, Client ID, and Secret to a JSON file for easy reuse.

## Prerequisites

```bash
pip install requests

## Example Usage

import google_auth

# 1. Setup your credentials and scope
client_id = "YOUR_GOOGLE_CLIENT_ID"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
scopes = ["[https://www.googleapis.com/auth/drive.metadata.readonly](https://www.googleapis.com/auth/drive.metadata.readonly)"]

# 2. Initialize the auth client
# You can optionally pass a custom path for the token file
auth = google_auth.GoogleDeviceAuth(client_id, client_secret, scopes, token_file="my_tokens.json")

# 3. Start the authentication flow
# This will print the URL and User Code to the console
auth.authenticate()
