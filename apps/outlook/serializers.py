from rest_framework.serializers import ModelSerializer

from apps.outlook.models import Email


class EmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = ('__all__')
