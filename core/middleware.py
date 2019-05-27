from django.utils import timezone

from core.models import ActionHistory


class HistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time = timezone.now()

        response = self.get_response(request)
        ActionHistory.objects.create(
            user=self.get_user(request),
            created_at=time,
            ip=request.META.get('REMOTE_ADDR')
        )
        return response

    def get_user(self, request):
        if request.user.is_anonymous:
            user = None
        else:
            user = request.user
        return user
