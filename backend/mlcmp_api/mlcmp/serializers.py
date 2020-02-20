from rest_framework.serializers import ModelSerializer
from .models import Mlcmp


class MlcmpSerializer(ModelSerializer):
    class Meta:
        model = Mlcmp
        fields = '__all__'
