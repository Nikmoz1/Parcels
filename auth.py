import json

import requests

from config import Config


class AuthFedex:

    @staticmethod
    def getting_a_token():
        config = Config.auth_conf()
        # print(config["client_id"])
        # print(config["client_secret"])
        url = "https://apis-sandbox.fedex.com/oauth/token"
        payload = f'grant_type=client_credentials&client_id={config["client_id"]}&' \
                  f'client_secret={config["client_secret"]} '
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        token = json.loads(response.text)["access_token"]
        config['Authorization']['access_token'] = token
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)


# AuthFedex.getting_a_token()
