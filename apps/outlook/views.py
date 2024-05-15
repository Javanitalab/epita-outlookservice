from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.outlook.service.outlook_auth import OutlookAuth


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

        url = OutlookAuth().send_authorization_token_request(code, is_token_expired=False)

        return Response(status=200)
