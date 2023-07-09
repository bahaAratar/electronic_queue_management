from django.urls import path
from .views import *

app_name = 'ticket'

urlpatterns = [
    path('', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('<int:pk>/', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-retrieve-update-destroy'),
    path('me/', TicketListAPIView.as_view()),
    
    path('regions/', RegionListCreateAPIView.as_view(), name='region-list-create'),
    path('regions/<int:pk>/', RegionRetrieveUpdateDestroyAPIView.as_view(), name='region-retrieve-update-destroy'),
    
    path('areas/', AreaListCreateAPIView.as_view(), name='area-list-create'),
    path('areas/<int:pk>/', AreaRetrieveUpdateDestroyAPIView.as_view(), name='area-retrieve-update-destroy'),
    
    path('cities/', CityListCreateAPIView.as_view(), name='city-list-create'),
    path('cities/<int:pk>/', CityRetrieveUpdateDestroyAPIView.as_view(), name='city-retrieve-update-destroy'),
    
    path('departments/', DepartmentListCreateAPIView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyAPIView.as_view(), name='department-retrieve-update-destroy'),
    
    path('activate/', TicketActivationAPIView.as_view(), name='ticket-activation'),

]
