import httpx

from helpers.config import Fetch
from helpers.random import Random

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
            
    def change_password(code: str, password: str) -> dict[str]:
        new_password: str = Random.string(25)
        
        headers = {
            "authorization": Fetch.authorization_token(),
            "content-type": "application/json",
        }
        
        payload = {
            "password": password,
            "new_password": new_password,
        }
        
        response = httpx_client.patch("https://canary.discord.com/api/v9/users/@me", headers=headers, json=payload)
        
        if response.status_code == 200:
            return {"new_password": new_password, "token": response.json()["token"]}
        
        elif response.status_code == 400:
            if response.json()["message"] == "Invalid two-factor code":
                new_payload = {
                    "code": code,
                    "password": password,
                    "new_password": new_password,
                }
                
                response = httpx_client.patch("https://canary.discord.com/api/v9/users/@me", headers=headers, json=new_payload)
                
                if response.status_code == 200:
                    return {"new_password": new_password, "new_token": response.json()["token"]}
                else:
                    return None
            else:
                return None 
            
        else:
            return None