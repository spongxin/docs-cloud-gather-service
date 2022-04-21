from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from gather.serializers import PackageSerializer
from rest_framework import viewsets
from gather.models import Package


class PackageViewSet(viewsets.ModelViewSet):
    # permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    queryset = Package.objects.all().order_by('-publish')
    serializer_class = PackageSerializer

