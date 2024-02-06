import requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import HandlerSerializer, OrderContactSerializer, ContactSerializer
from .models import Deal


class HandlerView(APIView):
    """A view for viewing and creating Deal objects, meant for requests from bitrix24"""

    def post(self, request):
        # The original format is hard to serialize so we simplify it for easier use
        data = self.reformat_call_data(request)
        serializer = HandlerSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        dealid = serializer.validated_data['order_id']
        response = requests.get(
            'https://b24-5fc7z1.bitrix24.ru/rest/1/s6i97ofh6yo71kn4/crm.deal.contact.items.get.json', {'ID': dealid})

        if response.status_code == 200:
            serializer = OrderContactSerializer(data=response.json())
            if not serializer.is_valid():
                raise ValueError(
                    f"An error occured while verifying order data: {serializer.errors}")

            contactid = serializer.validated_data['result'][0]['CONTACT_ID']
            response = requests.get(
                'https://b24-5fc7z1.bitrix24.ru/rest/1/bumi8etmuefxzikf/crm.contact.get.json', {'ID': contactid})

            if response.status_code == 200:
                serializer = ContactSerializer(data=response.json())
                if not serializer.is_valid():
                    raise ValueError(
                        f"An error occured while verifying contact data: {serializer.errors}")

                full_name = serializer.validated_data['result']['NAME'] + \
                    serializer.validated_data['result']['SECOND_NAME'] + \
                    serializer.validated_data['result']['LAST_NAME']
                phone_number = serializer.validated_data['result']['PHONE'][0]['VALUE']
                comment = serializer.validated_data['result']['COMMENTS']

                Deal.objects.create(full_name=full_name,
                                    phone_number=phone_number, comment=comment)
                # TODO: Send to google sheets handler

            else:
                raise ValueError(str(response.status_code) +
                                 ': ' + str(request.json()))

        else:
            raise ValueError(str(response.status_code) +
                             ': ' + str(request.json()))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def reformat_call_data(self, request):
        """Reformats the QueryDict data by the API call for better handling in serializers"""

        data = request.data
        auth_token = data['auth[application_token]']
        order_id = str(data['data[FIELDS][ID]'])

        return {'order_id': order_id, 'auth_token': auth_token}
