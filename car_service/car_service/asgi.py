import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from CarCompany.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_service.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),  # Regular HTTP requests
        'websocket': URLRouter(websocket_urlpatterns),  # WebSocket connections
    }
)