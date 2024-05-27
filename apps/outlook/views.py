from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.outlook.models import OutlookAccount, Email
from apps.outlook.serializers import EmailSerializer
from apps.outlook.service.outlook_auth import OutlookAuth
from apps.outlook.service.outlook_message import OutlookMessage


# Create your views here.


class OutlookAuthViewSet(ViewSet):

    @action(methods=['get'], detail=False)
    def get_authorization_url(self, request, *args):
        url = OutlookAuth().create_authorization_url()

        return Response(data={
            "url": url
        }, status=200)

    @action(methods=['get'], detail=False)
    def get_authorization_token(self, request, *args):
        code = self.request.query_params.get('code', None)

        if code is None:
            return Response(status=400, data={'message': 'code is missing in query params'})
        outlook_account = OutlookAuth()
        access_token, refresh_token = outlook_account.send_authorization_token_request(code, is_token_expired=False)
        outlook_account.create_outlook_account(access_token, refresh_token)

        return Response(status=200)


class OutlookMessageViewSet(ViewSet):

    @action(methods=['get'], detail=False)
    def list_of_messages(self, request, *args):
        try:
            outlook_account = OutlookAccount.objects.get(email_address=self.request.query_params.get('email_address'))
        except OutlookAccount.DoesNotExist:
            return Response(status=400, data='outlook account with this email does not exists!')
        except OutlookAccount.MultipleObjectsReturned:
            return Response(status=500, data='multiple accounts with this email exists!')

        emails = OutlookMessage().list_of_messages(outlook_account)

        return Response(status=200, data=EmailSerializer(instance=emails, many=True).data)

    @action(methods=['post'], detail=False)
    def send_message(self, request, *args):
        outlook_account_id = self.request.data.get('outlook_account_id', None)
        subject = self.request.data.get('subject', None)
        body = self.request.data.get('body', None)
        to = self.request.data.get('to', None)
        cc = self.request.data.get('cc', None)
        bcc = self.request.data.get('bcc', None)

        try:
            outlook_account = OutlookAccount.objects.get(id=outlook_account_id)
        except OutlookAccount.DoesNotExist:
            return Response(status=400, data='outlook account with this email does not exists!')
        except OutlookAccount.MultipleObjectsReturned:
            return Response(status=500, data='multiple accounts with this email exists!')

        OutlookMessage().send_message(outlook_account, subject=subject, to=to, cc=cc, bcc=bcc, body=body)

        return Response(status=202)
