from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Deal
from .serializers import DealSerializer


class DealViewset(viewsets.ModelViewSet):
    """A view for viewing and creating Deal objects, meant for requests from bitrix24"""

    queryset = Deal.objects.all()
    serializer_class = DealSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
