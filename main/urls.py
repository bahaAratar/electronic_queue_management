from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
    title='Pets hackathon',
    default_version='v1',
    description='pets'
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('ticket/', include('ticket.urls')),
    path('queue/', include('queues.urls')),

    path('swagger/', schema_view.with_ui('swagger')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
