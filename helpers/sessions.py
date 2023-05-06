import httpx

from helpers.encoding import Encoding
from helpers.useragent import UserAgent

httpx_client = httpx.Client(timeout=10)

x_super_properties: dict[str] = {"os":"Windows", "browser":"Discord Client", "release_channel":"canary", "client_version":"1.0.60", "os_version":"10.0.22621", "os_arch":"x64", "system_locale":"en-GB", "client_build_number":196142, "native_build_number":32342, "client_event_source": None, "design_id":0}

class Sessions:
    def get() -> dict[str]:
        headers = {
            "authorization": "MTA1Mjk4MjcyMTU5ODczODUyMg.GSVGIr.gnN1CD1XomyeALkhlG3HaJ7tUiOVvkRF6L0rmc",
            "user-agent": UserAgent.get_random(),
            "x-super-properties": Encoding.string(str(x_super_properties)),
        }