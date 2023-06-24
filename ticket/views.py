from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Ticket, City, Department, Area, Region
from .serializers import TicketSerializer, CitySerializer, DepartmentSerializer, AreaSerializer, RegionSerializer, ActivateTicketSerializer
from queues.models import Queue, Window 

class TicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # permission_classes = [IsAuthenticated]

class TicketRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        queue = Queue.objects.filter(ticket=instance).first()
        if queue:
            queue.delete()
        instance.delete()

class TicketActivationAPIView(APIView):
    serializer_class = ActivateTicketSerializer

    def post(self, request):
        activation_code = request.data.get('activation_code', None)

        #activate and deactivate
        if activation_code is not None:
            try:
                ticket = Ticket.objects.get(activation_code=activation_code)
                if ticket.status == 'active':
                    ticket.status = 'not_active'
                    queue = Queue.objects.filter(ticket=ticket).first()
                    if queue:
                        queue.delete()
                else:
                    ticket.status = 'active'
                    Queue.objects.create(ticket=ticket)
                ticket.save()
                serializer = self.serializer_class(ticket)
                return Response(serializer.data)
            except Ticket.DoesNotExist:
                return Response({'error': 'Билет не найден'}, status=400)
        else:
            return Response({'error': 'Отсутствует активационный код'}, status=400)
        
        #only activate
    #     if activation_code is not None:
    #         try:
    #             ticket = Ticket.objects.get(activation_code=activation_code)
    #             if ticket.status == 'active':
    #                 return Response({'error': 'Билет уже активирован'}, status=400)
    #             ticket.status = 'active'
    #             ticket.save()
    #             Queue.objects.filter(ticket=ticket, ticket__status='not_active').delete()
    #             queue_entry = Queue.objects.filter(ticket=ticket).first()
    #             if not queue_entry:
    #                 Queue.objects.create(ticket=ticket)
    #             serializer = self.serializer_class(ticket)
    #             return Response(serializer.data)
    #         except Ticket.DoesNotExist:
    #             return Response({'error': 'Билет не найден'}, status=400)
    #     else:
    #         return Response({'error': 'Отсутствует активационный код'}, status=400)
        

        
class RegionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAdminUser]

class RegionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAdminUser]

class AreaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAdminUser]

class AreaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsAdminUser]

class CityListCreateAPIView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]

class CityRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]

class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]

class DepartmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]
