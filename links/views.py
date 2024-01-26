from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import *
from .models import *
from .links_permission import AccessPermissionLinks, CategoryAccess
from .admin_serializers import CryptoSerializer
from django.contrib.auth.models import Group


from shop.models import OrderItems
from payment.views import USERINFO_CREATE_PERM


# class that user can see basic models & icons to choose from
class OpenGui(APIView):
    permission_classes = [IsAuthenticated, AccessPermissionLinks]
    serializer_class = BlankSerializer

    def get(self, request):
        front_views = Blank.objects.all()
        return Response(self.serializer_class(front_views, many=True).data, status=status.HTTP_200_OK)


class AdminControl(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CryptoSerializer

    def get(self, request):
        crypto_wallets = CryptoWalletAddress.objects.filter(user=None)

        return Response(self.serializer_class(crypto_wallets, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            crypto_obj = CryptoWalletAddress.objects.create(**serializer.validated_data)
            return Response(self.serializer_class(crypto_obj).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


def get_user(request):
    return request.user


class Category(APIView):
    permission_classes = [IsAuthenticated, CategoryAccess]
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        return Response(self.serializer_class(categories).data, status=status.HTTP_200_OK)

    def patch(self, request):
        # TODO: make changes in order to change the title of category
        pass


class GeneralView(APIView):
    permission_classes = [IsAuthenticated, AccessPermissionLinks]
    serializer_class = AbstractDataSerializer
    model = AbstractData

    def get(self, request):
        user = get_user(request)
        obj = self.model.objects.filter(user=user)

        if obj.exists():
            return Response(self.serializer_class(obj, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

        return Response({'message': 'No Item Found!'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            obj = self.model.objects.create(user=user, **serializer.validated_data)

            return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            obj = self.model.objects.filter(user=user, id=pk)

            if obj.exists():
                obj.update(**serializer.validated_data)
                return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)

            return Response({'message': 'Not Found!'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = get_user(request)

        obj = self.model.objects.filter(user=user, id=pk)

        if obj.exists():
            obj.delete()
            return Response({'message': 'Item deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CryptoWalletAddressView(GeneralView):
    serializer_class = CryptoWalletAddressSerializer
    model = CryptoWalletAddress

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.crypto_wallet_address.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SocialMediaView(GeneralView):
    serializer_class = SocialMediaSerializer
    model = SocialMedia

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.services.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ContactInfoView(GeneralView):
    serializer_class = ContactInfoSerializer
    model = ContactInfo

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.contact_info.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class BannerAndImageView(GeneralView):
    serializer_class = BannerAndImageSerializer
    model = BannerAndImage

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.images.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class VideoView(GeneralView):
    serializer_class = VideoSerializer
    model = Video

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.video_links.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class LinksView(GeneralView):
    serializer_class = LinksSerializer
    model = Links

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.links.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class NavigationView(GeneralView):
    serializer_class = NavigationsSerializer
    model = Navigations

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.navigation_info.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class FAQView(GeneralView):
    serializer_class = FAQSerializer
    model = FAQ

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.faq.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class BankAccountView(GeneralView):
    serializer_class = BankAccountsSerializer
    model = BankAccounts

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.bank_account.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CounterView(GeneralView):
    serializer_class = CounterSerializer
    model = Counter

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.counter.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class FreeTextView(GeneralView):
    serializer_class = FreeTextSerializer
    model = FreeText

    def post(self, request, pk=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = get_user(request)
            user_info = UserInfo.objects.filter(user=user, id=pk)

            if user_info.exists():
                obj = self.model.objects.create(user=user, **serializer.validated_data)
                user_info = user_info.first()
                user_info.free_texts.add(obj)

                return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

            return Response({'message': 'Not Valid'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated, AccessPermissionLinks]

    def get(self, request, page_name=None):
        user = get_user(request)

        if page_name is not None:
            user_page = UserInfo.objects.filter(user=user, page_name=page_name)
            if user_page.exists():
                return Response(UserInfoSerializer(user_page, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

            return Response({'message': 'Page Not Found!'}, status=status.HTTP_404_NOT_FOUND)

        user_pages = UserInfo.objects.filter(user=user)
        if user_pages.count() == 0:
            return Response({'message': 'You have not created any pages yet!'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserInfoSerializer(user_pages, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    def post(self, request):
        user = get_user(request)
        if user.has_perm(USERINFO_CREATE_PERM):

            user_card_orders = OrderItems.objects.filter(user=user, ordered=True, created_card=False)
            if user_card_orders.exists():
                for order in user_card_orders:
                    cards = order.orders.all()
                    for item in cards:
                        for _ in range(item.quantity):
                            UserInfo.objects.create(selected_product=item.product,
                                                    selected_product_opt=item.selected_product,
                                                    user=user)

                    order.created_card = True
                    order.save()

                group_obj = Group.objects.get(name=USERINFO_CREATE_PERM)
                group_obj.user_set.remove(user)
                # user.user_permissions.remove(USERINFO_CREATE_PERM)

                return Response(status=status.HTTP_201_CREATED)

            return Response({'message': 'You don\'t have any order!'}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": 'You do NOT have permission to perform this action'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        serializer = UserInfoPatchSerializer(data=request.data)

        if serializer.is_valid():
            page_name = serializer.validated_data.get('page_name')
            page_name_id = serializer.validated_data.get('user_info_id')
            user = get_user(request)

            page = UserInfo.objects.filter(id=page_name_id, user=user)
            if page.exists():

                is_page_name_unique = UserInfo.objects.filter(page_name=page_name)

                if is_page_name_unique.count() == 0:
                    page.update(page_name=page_name)
                    return Response(status=status.HTTP_201_CREATED)

                return Response({'message': f'The name {page_name} Already Exists'}, status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)



def page_name_unqiue_check(request):
    pass


class PublicViewUserInfo(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserInfoForPublic

    def get(self, request, page_name=None):
        if page_name is not None:
            page_name = page_name.strip()
            page = UserInfo.objects.filter(page_name=page_name)

            if page.exists():
                return Response(self.serializer_class(page, context={'request': request}).data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)
