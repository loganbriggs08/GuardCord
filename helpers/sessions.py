import httpx

from typing import Union
from helpers.config import Fetch
from helpers.useragent import UserAgent

httpx_client = httpx.Client(timeout=10)

class Sessions:
    def get() -> Union[None, dict[str]]:
        headers = {
            "authorization": Fetch.authorization_token(),
            "user-agent": UserAgent.get_random(),
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJjYW5hcnkiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC42MCIsIm9zX3ZlcnNpb24iOiIxMC4wLjIyNjIxIiwib3NfYXJjaCI6Ing2NCIsInN5c3RlbV9sb2NhbGUiOiJlbi1HQiIsImNsaWVudF9idWlsZF9udW1iZXIiOjE5NjE0MiwibmF0aXZlX2J1aWxkX251bWJlciI6MzIzNDIsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0=",
        }
        
        sessions_response: object = httpx_client.get("https://canary.discord.com/api/v9/auth/sessions", headers=headers)
        
        if sessions_response.status_code == 200:
            return sessions_response.json()
        else:
            None