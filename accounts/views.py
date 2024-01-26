from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import AddressSerializer
from .models import Address, User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class AddressView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AddressSerializer

    @swagger_auto_schema(
        operation_description="Get User Address",
        responses={200: "OK", 404: "No Address Found!"},
    )
    def get(self, request):
        user = request.user

        addresses = Address.objects.filter(user_addr=user)
        if addresses.exists():
            return Response(self.serializer_class(addresses, many=True).data, status=status.HTTP_200_OK)

        return Response({'message': 'No Address Found!'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            address = Address.objects.create(**serializer.validated_data, user_addr=user)
            return Response(self.serializer_class(address).data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({'message': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and pk is not None:
            user = request.user
            address = Address.objects.filter(id=pk, user_addr=user)

            if address.exists():
                address.update(**serializer.validated_data)
                return Response(self.serializer_class(address).data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            user = request.user
            address = Address.objects.filter(id=pk, user_addr=user)
            if address.exists():
                address.delete()
                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)



