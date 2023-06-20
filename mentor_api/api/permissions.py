from rest_framework.permissions import BasePermission


class IsMentorUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_mentor)


class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_student)

