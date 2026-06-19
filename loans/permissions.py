from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Profile


def get_request_profile(request):
    user = request.user
    if not user or not user.is_authenticated:
        return None
    return getattr(user, 'profile', None)


def is_admin(request):
    profile = get_request_profile(request)
    return bool(profile and profile.role == Profile.ROLE_ADMIN)


class HasProfileRole(BasePermission):
    def has_permission(self, request, view):
        return get_request_profile(request) is not None


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request)


class IsAdminOrSelfProfile(BasePermission):
    def has_permission(self, request, view):
        return get_request_profile(request) is not None

    def has_object_permission(self, request, view, obj):
        if is_admin(request):
            return True
        return isinstance(obj, Profile) and obj.user_id == request.user.id


class IsAdminOrOwnObject(BasePermission):
    def has_permission(self, request, view):
        return get_request_profile(request) is not None

    def has_object_permission(self, request, view, obj):
        if is_admin(request):
            return True

        profile = get_request_profile(request)
        if not profile:
            return False

        if isinstance(obj, Profile):
            return obj.id == profile.id

        if hasattr(obj, 'profile_id'):
            return obj.profile_id == profile.id

        if hasattr(obj, 'applicant_id'):
            return obj.applicant_id == profile.id

        return False


class CanViewOwnApplicationOrAdminUpdate(BasePermission):
    def has_permission(self, request, view):
        if get_request_profile(request) is None:
            return False
        if request.method in SAFE_METHODS:
            return True
        return is_admin(request)

    def has_object_permission(self, request, view, obj):
        if is_admin(request):
            return True
        if request.method not in SAFE_METHODS:
            return False

        profile = get_request_profile(request)
        return bool(profile and obj.applicant_id == profile.id)
