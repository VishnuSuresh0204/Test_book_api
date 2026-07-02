from rest_framework.response import Response
from functools import wraps
from django.conf import settings

def api_key_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        api_key = request.headers.get("x-api-key")

        if api_key != settings.API_KEY:
            return Response(
                {"error": "Invalid API Key"},
                status=401
            )

        return view_func(request, *args, **kwargs)

    return wrapper