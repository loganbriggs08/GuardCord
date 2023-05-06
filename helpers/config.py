import json

class Fetch:
    def authorization_token() -> str: 
        """Fetch the authorization token from the config.json file.

        Returns:
            str: Returns the authorization token.
        """
        config = open("./config.json"); data = json.load(config)
        authorization = data["account"]["authorization_token"]
        
        config.close(); return authorization