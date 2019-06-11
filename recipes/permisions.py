from django.core.exceptions import PermissionDenied


class SameUserOnlyPermission(object):
    def has_permissions(self):
        return self.get_object().author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied('You do not have permission.')
        return super(SameUserOnlyPermission, self).dispatch(
            request, *args, **kwargs)
