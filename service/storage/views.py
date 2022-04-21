from storage.serializers import UploadTokenSerializer, ResourceSerializer
from storage.models import UploadToken, Resource
from rest_framework import viewsets


class UploadTokenViewSet(viewsets.ModelViewSet):
    queryset = UploadToken.objects.all().order_by('-publish')
    serializer_class = UploadTokenSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all().order_by('-publish')
    serializer_class = ResourceSerializer
