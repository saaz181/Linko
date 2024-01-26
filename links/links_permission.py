from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group


class AccessPermissionLinks(BasePermission):
    group_name = 'access_links'

    def has_permission(self, request, view):
        user = request.user
        group_obj = Group.objects.filter(name=self.group_name)
        if group_obj.exists():
            user_group = user.groups.filter(name=self.group_name)
            return len(user_group) == 1

        return False


class CategoryAccess(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        permissions = ['links.can_change_category', 'links.can_view_category', ]

        for perm in permissions:
            if not user.has_perm(perm):
                return False

        return True
