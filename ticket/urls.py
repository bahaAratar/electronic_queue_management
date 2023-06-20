from django.urls import path
from .views import (
    TicketListCreateAPIView,
    TicketRetrieveUpdateDestroyAPIView,
    RegionListCreateAPIView,
    RegionRetrieveUpdateDestroyAPIView,
    AreaListCreateAPIView,
    AreaRetrieveUpdateDestroyAPIView,
    CityListCreateAPIView,
    CityRetrieveUpdateDestroyAPIView,
    DepartmentListCreateAPIView,
    DepartmentRetrieveUpdateDestroyAPIView,
    TicketActivationAPIView,
)

app_name = 'ticket'

urlpatterns = [
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-retrieve-update-destroy'),
    path('regions/', RegionListCreateAPIView.as_view(), name='region-list-create'),
    path('regions/<int:pk>/', RegionRetrieveUpdateDestroyAPIView.as_view(), name='region-retrieve-update-destroy'),
    path('areas/', AreaListCreateAPIView.as_view(), name='area-list-create'),
    path('areas/<int:pk>/', AreaRetrieveUpdateDestroyAPIView.as_view(), name='area-retrieve-update-destroy'),
    path('cities/', CityListCreateAPIView.as_view(), name='city-list-create'),
    path('cities/<int:pk>/', CityRetrieveUpdateDestroyAPIView.as_view(), name='city-retrieve-update-destroy'),
    path('departments/', DepartmentListCreateAPIView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyAPIView.as_view(), name='department-retrieve-update-destroy'),
    path('tickets/activate/', TicketActivationAPIView.as_view(), name='ticket-activation'),
]


# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('', TicketAPIView.as_view()),
#     path('region/', RegionAPIView.as_view()),
#     path('city/', CityAPIView.as_view()),
#     path('department/', DepartmentAPIView.as_view()),
#     path('area/', AreaAPIView.as_view()),
#     path('activate/', TicketActivationView.as_view()),
# ]