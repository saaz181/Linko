from django.urls import path
from .views import *


urlpatterns = [
    path('front', OpenGui.as_view(), name='open-gui'),

    # crypto wallet address
    path('crypto-wallet', CryptoWalletAddressView.as_view(), name='crypto-wallet'),
    path('crypto-wallet/<int:pk>', CryptoWalletAddressView.as_view(), name='crypto-wallet'),

    # social media
    path('social-media', SocialMediaView.as_view(), name='social-media'),
    path('social-media/<int:pk>', SocialMediaView.as_view(), name='social-media'),

    # contact info
    path('contact-info', ContactInfoView.as_view(), name='contact-info'),
    path('contact-info/<int:pk>', ContactInfoView.as_view(), name='contact-info'),

    # banner & image
    path('banner', BannerAndImageView.as_view(), name='banner-and-image'),
    path('banner/<int:pk>', BannerAndImageView.as_view(), name='banner-and-image'),

    # video link
    path('video', VideoView.as_view(), name='video'),
    path('video/<int:pk>', VideoView.as_view(), name='video'),

    # Links
    path('link', LinksView.as_view(), name='link'),
    path('link/<int:pk>', LinksView.as_view(), name='link'),

    # navigation
    path('navigation', NavigationView.as_view(), name='navigation'),
    path('navigation/<int:pk>', NavigationView.as_view(), name='navigation'),

    # FAQs
    path('faq', FAQView.as_view(), name='faq'),
    path('faq/<int:pk>', FAQView.as_view(), name='faq'),

    # bank account
    path('bank-account', BankAccountView.as_view(), name='bank-account'),
    path('bank-account/<int:pk>', BankAccountView.as_view(), name='bank-account'),

    # counter
    path('counter', CounterView.as_view(), name='counter'),
    path('counter/<int:pk>', CounterView.as_view(), name='counter'),

    # user info
    path('page', UserInfoView.as_view(), name='page'),
    path('page/<str:page_name>', UserInfoView.as_view(), name='page'),

    # admin controls
    path('admin/crypto', AdminControl.as_view(), name='crypto'),

    # public view
    path('public/<str:page_name>', PublicViewUserInfo.as_view(), name='public-view')
]
