from django.contrib import admin
from django.urls import path, include, re_path
from .views import serve_react

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/students/', include('students.urls')),
    # path('api/v1/curriculum/', include('curriculum.urls')), # Commenting out until verified
    path('api/v1/coaching/', include('coaching.urls')),
    
    # Catch-all for React Frontend
    # Matches any URL that doesn't start with api/, admin/, or static/
    re_path(r'^(?!api|admin|static).*$', serve_react),
]
