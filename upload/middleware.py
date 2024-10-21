from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile
class CheckUploadStatusMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            request.has_uploaded_book = user_profile.has_uploaded_book