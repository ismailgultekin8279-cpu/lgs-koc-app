from django.http import HttpResponse
from django.conf import settings
import os

def serve_react(request, resource=''):
    try:
        # In production, index.html is located in STATIC_ROOT (collected from frontend build)
        path = os.path.join(settings.STATIC_ROOT, 'index.html')
        with open(path) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        return HttpResponse(
            """
            <h1>Frontend Not Found</h1>
            <p>Please ensure React is built and collected into staticfiles.</p>
            """,
            status=501,
        )
