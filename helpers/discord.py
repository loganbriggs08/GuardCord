import httpx

from helpers.config import Fetch

httpx_client = httpx.Client(timeout=10)

class Discord:
    def send_code_to_email(password: str) -> str:
        headers = {
            "authorization": Fetch.authorization_token(),
            "content-type": "application/json",
        }
        
        payload = {
            "password": password,
        }
        
        response = httpx_client.post("https://canary.discord.com/api/v9/auth/verify/view-backup-codes-challenge", headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()["nonce"]
        else:
            None
        
    def get_codes(code: str, nonce: str) -> dict:
        headers = {
            "authorization": Fetch.authorization_token(),
            "content-type": "application/json",
        }
        
        payload = {
            "key": code,
            "nonce": nonce,
            "regenerate": False,
        }
        
        response = httpx_client.post("https://canary.discord.com/api/v9/users/@me/mfa/codes-verification", headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            None