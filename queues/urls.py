from django.urls import path
from .views import QueueListCreateAPIView, WindowListCreteAPIView, WindowRetrieveUpdateDestroyAPIView, WindowToggleAPIView

urlpatterns = [
    path('', QueueListCreateAPIView.as_view()),
    
    path('window/', WindowListCreteAPIView.as_view()),
    path('window/<int:pk>/', WindowRetrieveUpdateDestroyAPIView.as_view()),
    path('window/<int:pk>/toggle/', WindowToggleAPIView.as_view()),
]
