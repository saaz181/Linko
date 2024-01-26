from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group


class UploadAccess(BasePermission):
    group_name = 'customization'

    def has_permission(self, request, view):
        user = request.user
        group_obj = Group.objects.filter(name=self.group_name)
        if group_obj.exists():
            user_group = user.groups.filter(name=self.group_name)
            return len(user_group) == 1

        return False
