from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # path('', views.home, name='home'),
    # path('overview/', views.overview, name='overview'),

    path('sentry-debug/', trigger_error),

    path('', views.MyView.as_view(), name='home'),
    path('', views.MyView.as_view(), name='overview'),

    path('', include('bookings.urls')),
    path('', include('services.urls')),
    path('', include('customers.urls')),
    path('', include('equipment.urls')),
    path('', include('staff.urls')),
    path('', include('schedule.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
