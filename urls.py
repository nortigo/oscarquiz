from django.urls import path, include
from django.contrib import admin


admin.site.site_header = "Oscar Quiz Admin"
admin.site.site_title = "Oscar Quiz Admin Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_urls', namespace='api')),
]
