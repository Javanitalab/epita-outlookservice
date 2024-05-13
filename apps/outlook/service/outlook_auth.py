import os
import json


class OutlookAuth():

    def create_authorization_url(self):
        client_secret_path = os.path.join('.', 'data', 'microsoft', 'entra_config.json')
        data = dict()
        with open(client_secret_path, 'r') as file:
            data = json.load(file)

        url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize/?client_id={data['client_id']}&response_type=code&redirect_uri={data['redirect_uri']}&scope={data['scope']}"

        return url
