import os
import json

import requests

from apps.outlook.models import OutlookAccount, Email


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
