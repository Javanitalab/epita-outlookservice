import os
import json

import requests

from apps.outlook.models import OutlookAccount, Email


class OutlookAuth():

    def create_authorization_url(self):
        client_secret_path = os.path.join('.', 'data', 'microsoft', 'entra_config.json')
        data = dict()
        with open(client_secret_path, 'r') as file:
            data = json.load(file)

        url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize/?client_id={data['client_id']}&response_type=code&redirect_uri={data['redirect_uri']}&scope={data['scope']}"

        return url

    def send_authorization_token_request(self, code: str, is_token_expired: bool):
        client_secret_path = os.path.join('.', 'data', 'microsoft', 'entra_config.json')
        data = dict()
        with open(client_secret_path, 'r') as file:
            data = json.load(file)

        response = requests.post(
            url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'client_id': data['client_id'],
                'scope': data['scope'],
                'code': code,
                'redirect_uri': data['redirect_uri'],
                'grant_type': 'refresh_token' if is_token_expired else 'authorization_code',
                'client_secret': data['secret_key']
            }
        )

        print(response.status_code)
        print(response.text)

        if response.status_code != 200:
            raise Exception(response.text)
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']

        return access_token, refresh_token

    def create_outlook_account(self, access_token: str, refresh_token: str):
        profile_response = requests.get(
            url='https://graph.microsoft.com/beta/me/profile',
            headers={
                'Authorization': access_token
            }
        )

        email = profile_response.json()['emails'][0]['address']
        account, is_created = OutlookAccount.objects.get_or_create(email_address=email)

        account.access_token = access_token
        account.refresh_token = refresh_token
        account.save()
        return account


