import os
import json

import requests

from apps.outlook.models import OutlookAccount, Email
from apps.outlook.service.outlook_auth import OutlookAuth


class OutlookMessage():

    def list_of_messages(self, outlook_account: OutlookAccount):
        emails = []
        messages_response = requests.get(
            url='https://graph.microsoft.com/v1.0/me/messages',
            headers={
                'Authorization': f'Bearer {outlook_account.access_token}'
            }
        )

        if messages_response.status_code == 401:
            # TODO send refresh token request and update the tokens
            pass

        for email in messages_response.json()['value']:
            body = email['body']['content']
            preview = email['bodyPreview']
            subject = email['subject']
            id = email['id']
            sender = email['from']['emailAddress']['address']
            receiver = [email_address['emailAddress']['address'] for email_address in email['toRecipients']]
            cc = [email_address['emailAddress']['address'] for email_address in email['ccRecipients']]
            bcc = [email_address['emailAddress']['address'] for email_address in email['bccRecipients']]

            db_email, is_created = Email.objects.get_or_create(outlook_id=id)
            if not is_created:
                db_email.outlook_id = id
                db_email.preview = preview
                db_email.subject = subject
                db_email.body = body
                db_email.sender = sender
                db_email.receiver = receiver
                db_email.cc = cc
                db_email.bcc = bcc
                db_email.save()
            emails.append(db_email)

        return emails

    def send_message(self, outlook_account: OutlookAccount, subject: str, to: str, cc: list, bcc: list, body,
                     attachments=None, avoid_stack_overflow=False):

        send_response = requests.post(
            url=f'https://graph.microsoft.com/v1.0/me/sendMail',
            headers={
                'Authorization': f'Bearer {outlook_account.access_token}',
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "Text",
                        "content": body
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": to
                            }
                        }
                    ],
                    "ccRecipients": [
                        {
                            "emailAddress": {
                                "address": cc_email
                            }
                        } for cc_email in cc
                    ]
                },
                "saveToSentItems": "true"
            })
        )
        if send_response.status_code == 202:
            return True
        if send_response.status_code == 401 and not avoid_stack_overflow:
            access_token, refresh_token = OutlookAuth().send_authorization_token_request(outlook_account.refresh_token,
                                                                                         is_token_expired=True)
            outlook_account.access_token = access_token
            outlook_account.refresh_token = refresh_token
            outlook_account.save()
            self.send_message(outlook_account, subject, to, cc, bcc, body, attachments, avoid_stack_overflow=True)
        else:
            raise Exception(send_response.text)
