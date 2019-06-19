# from rest_framework import permissions
#
#
# class IsOwnerOrIsAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_staff:
#             return True
#         return obj.pk == request.user.pk
#
#
# class IsOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.pk == request.user.pk
