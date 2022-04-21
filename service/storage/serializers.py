from rest_framework import serializers
from .models import UploadToken, Resource


class UploadTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadToken
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('unique', 'bucket', 'filename', 'url', 'publish')
