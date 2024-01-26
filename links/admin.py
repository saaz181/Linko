from django.contrib import admin
from .models import *

"""
Category
FrontData
AbstractData
Seperator
SocialMedia
ContactInfo
BannerAndImage
Video
Links
Navigations
FAQ
FreeText
Counter
UserInfo
Blank
"""

#
admin.site.register(Category)
# admin.site.register(FrontData)
# admin.site.register(AbstractData)
admin.site.register(SocialMedia)
admin.site.register(ContactInfo)
admin.site.register(BannerAndImage)
admin.site.register(Video)
admin.site.register(Links)
admin.site.register(Navigations)
admin.site.register(FAQ)
admin.site.register(FreeText)
admin.site.register(Counter)
admin.site.register(UserInfo)
admin.site.register(Blank)
admin.site.register(BankAccounts)
admin.site.register(CryptoWalletAddress)