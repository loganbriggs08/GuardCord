import httpx

from typing import Union
from helpers.config import Fetch
from helpers.encoding import Encoding
from helpers.useragent import UserAgent

httpx_client = httpx.Client(timeout=10)

x_super_properties: dict[str] = {"os":"Windows", "browser":"Discord Client", "release_channel":"canary", "client_version":"1.0.60", "os_version":"10.0.22621", "os_arch":"x64", "system_locale":"en-GB", "client_build_number":196142, "native_build_number":32342, "client_event_source": None, "design_id":0}

class Sessions:
    def get() -> Union[None, dict[str]]:
        headers = {
            "authorization": Fetch.authorization_token(),
            "user-agent": UserAgent.get_random(),
            "x-super-properties": Encoding.string(str(x_super_properties)),
        }
        
        sessions_response: object = httpx_client.get("https://canary.discord.com/api/v9/auth/sessions", headers=headers)
        
        if sessions_response.status_code == 200:
            return sessions_response.json()
        else:
            None