from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user_id` attribute.
    """

    def has_object_permission(self, request, view, obj):

        # Instance must have an attribute named `created_by_id`.
        return obj.created_by_id == request.user.id