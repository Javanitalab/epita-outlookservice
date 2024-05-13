from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.outlook.service.outlook_auth import OutlookAuth


# Create your views here.


class OutlookAuthViewSet(ViewSet):

    @action(methods=['get'], detail=False)
    def get_authorization_url(self,request,*args):
        url = OutlookAuth().create_authorization_url()

        return Response(data={
            "url": url
        }, status=200)
