import requests
import time
import json
import os
from typing import Optional, List

class GoogleDeviceAuth:
    """
    Handles the Google OAuth 2.0 Device Authorization Flow.
    Reference: https://developers.google.com/identity/protocols/oauth2/limited-input-device
    """
    
    DEVICE_CODE_URL = "https://oauth2.googleapis.com/device/code"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    
    def __init__(self, client_id: str, client_secret: str, scopes: List[str], token_file: str = "auth_tokens.json"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = " ".join(scopes) if isinstance(scopes, list) else scopes
        self.token_file = token_file

    def request_codes(self) -> dict:
        """Step 1: Request device and user codes."""
        data = {'client_id': self.client_id, 'scope': self.scopes}
        try:
            response = requests.post(self.DEVICE_CODE_URL, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error requesting codes: {e}")
            return None

    def poll_for_tokens(self, device_code: str, interval: int) -> dict:
        """Step 3: Poll until user authorizes."""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        }

        print(f"Polling every {interval} seconds...")
        
        while True:
            time.sleep(interval)
            try:
                response = requests.post(self.TOKEN_URL, data=data)
                tokens = response.json()

                if response.status_code == 200:
                    return tokens

                error = tokens.get('error')
                if error == 'authorization_pending':
                    continue
                elif error == 'slow_down':
                    interval += 5
                    print(f"Slow down requested. New interval: {interval}s")
                elif error in ('access_denied', 'expired_token'):
                    print(f"Authorization failed: {error}")
                    return None
                else:
                    print(f"Unexpected error: {tokens}")
                    return None
            except requests.Exception as e:
                print(f"Polling error: {e}")
                return None

    def authenticate(self):
        """Orchestrates the full flow."""
        # 1. Get Codes
        codes = self.request_codes()
        if not codes:
            return

        # 2. User Interaction
        print("\n" + "="*40)
        print(f"Go to: {codes['verification_url']}")
        print(f"Enter Code: {codes['user_code']}")
        print("="*40 + "\n")

        # 3. Poll
        tokens = self.poll_for_tokens(codes['device_code'], codes['interval'])
        
        if tokens:
            self.save_tokens(tokens)
            print("✅ Authentication successful!")
            return tokens

    def save_tokens(self, tokens: dict):
        tokens["client_id"] = self.client_id
        tokens["client_secret"] = self.client_secret
        with open(self.token_file, 'w') as f:
            json.dump(tokens, f, indent=4)
        print(f"Tokens saved to {self.token_file}")

# --- Usage Example ---
if __name__ == '__main__':
    # load these from environment variables for security
    CLIENT_ID = "YOUR_CLIENT_ID"
    CLIENT_SECRET = "YOUR_CLIENT_SECRET"
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

    if CLIENT_ID == "YOUR_CLIENT_ID":
        print("Please configure your Client ID and Secret in the script.")
    else:
        auth = GoogleDeviceAuth(CLIENT_ID, CLIENT_SECRET, SCOPES)
        auth.authenticate()
