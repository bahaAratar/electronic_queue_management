from django.urls import path
from .views import QueueListCreateAPIView, WindowListCreateAPIView, WindowRetrieveUpdateDestroyAPIView

app_name = 'queues'

urlpatterns = [
    path('', QueueListCreateAPIView.as_view(), name='queue-list-create'),
    path('window/', WindowListCreateAPIView.as_view(), name='window-list-create'),
    path('window/<int:pk>/', WindowRetrieveUpdateDestroyAPIView.as_view(), name='window-retrieve-update-destroy'),
]
