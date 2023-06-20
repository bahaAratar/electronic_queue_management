from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Ticket, City, Department, Area, Region
from .serializers import TicketSerializer, CitySerializer, DepartmentSerializer, AreaSerializer, RegionSerializer, ActivateTicketSerializer
from queues.models import Queue, Window 

class TicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ticket = serializer.save(owner=self.request.user)
        window = self.get_available_window()
        if window:
            queue = Queue.objects.create(ticket=ticket, window=window)

    def get_available_window(self):
        return Window.objects.filter(is_available=True).order_by('queue__timestamp').first()

class TicketRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        queue = Queue.objects.filter(ticket=instance).first()
        if queue:
            queue.delete()
        instance.delete()

class TicketActivationAPIView(APIView):
    serializer_class = ActivateTicketSerializer

    def post(self, request):
        activation_code = request.data.get('activation_code', None)

        if activation_code is not None:
            try:
                ticket = Ticket.objects.get(activation_code=activation_code)
                if ticket.status == 'active':
                    ticket.status = 'not_active'
                else:
                    ticket.status = 'active'
                ticket.save()
                serializer = self.serializer_class(ticket)
                return Response(serializer.data)
            except Ticket.DoesNotExist:
                return Response({'error': 'Билет не найден'}, status=400)
        else:
            return Response({'error': 'Отсутствует активационный код'}, status=400)
        
    
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



#region до обновления очереди

# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from .models import Ticket, City, Department, Area, Region
# from .serializers import TicketSerializer, CitySerializer, DepartmentSerializer, AreaSerializer, RegionSerializer, ActivateTicketSerializer
# from queues.models import Queue, Window 

# class TicketAPIView(generics.ListCreateAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         ticket = serializer.save(owner=self.request.user)
#         window = self.get_available_window()
#         if window:
#             queue = Queue.objects.create(ticket=ticket, window=window)

#     def get_available_window(self):
#         return Window.objects.filter(is_available=True).order_by('queue__timestamp').first()

# class TicketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     # permission_classes = [IsAuthenticated]

#     def perform_destroy(self, instance):
#         queue = Queue.objects.filter(ticket=instance).first()
#         if queue:
#             queue.delete()
#         instance.delete()

# class RegionAPIView(generics.ListCreateAPIView):
#     queryset = Region.objects.all()
#     serializer_class = RegionSerializer
#     permission_classes = [IsAdminUser]

# class RegionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Region.objects.all()
#     serializer_class = RegionSerializer
#     permission_classes = [IsAdminUser]

# class AreaAPIView(generics.ListCreateAPIView):
#     queryset = Area.objects.all()
#     serializer_class = AreaSerializer
#     permission_classes = [IsAdminUser]

# class AreaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Area.objects.all()
#     serializer_class = AreaSerializer
#     permission_classes = [IsAdminUser]

# class CityAPIView(generics.ListCreateAPIView):
#     queryset = City.objects.all()
#     serializer_class = CitySerializer
#     permission_classes = [IsAdminUser]

# class CityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = City.objects.all()
#     serializer_class = CitySerializer
#     permission_classes = [IsAdminUser]

# class DepartmentAPIView(generics.ListCreateAPIView):
#     queryset = Department.objects.all()
#     serializer_class = DepartmentSerializer
#     permission_classes = [IsAdminUser]

# class DepartmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Department.objects.all()
#     serializer_class = DepartmentSerializer
#     permission_classes = [IsAdminUser]

# class TicketActivationView(generics.GenericAPIView):
#     serializer_class = ActivateTicketSerializer

#     def post(self, request):
#         activation_code = request.data.get('activation_code', None)

#         if activation_code is not None:
#             try:
#                 ticket = Ticket.objects.get(activation_code=activation_code)
#                 if ticket.status == 'active':
#                     ticket.status = 'not_active'
#                 else:
#                     ticket.status = 'active'
#                 ticket.save()
#                 serializer = self.get_serializer(ticket)
#                 return Response(serializer.data)
#             except Ticket.DoesNotExist:
#                 return Response({'error': 'Билет не найден'}, status=400)
#         else:
#             return Response({'error': 'Отсутствует активационный код'}, status=400)

# #region всё что выше только на APIView

# # class TicketAPIView(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def get(self, request):
# #         ticket = Ticket.objects.filter(owner=request.user)
# #         serializer = TicketSerializer(ticket, many=True)
# #         return Response(serializer.data)

# #     def post(self, request):
# #         serializer = TicketSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save(owner=request.user)
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)
    
# #     def put(self, request):
# #         ticket_id = request.data.get('id')
# #         try:
# #             ticket = Ticket.objects.get(id=ticket_id, owner=request.user)
# #         except Ticket.DoesNotExist:
# #             return Response({'error': 'Билет не найден'}, status=404)

# #         serializer = TicketSerializer(ticket, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=400)
    
# #     def delete(self, request, pk):
# #         try:
# #             ticket = Ticket.objects.get(pk=pk, owner=request.user)
# #         except Ticket.DoesNotExist:
# #             return Response({'error': 'Билет не найден'}, status=404)

# #         ticket.delete()
# #         return Response(status=204)
    
# # class RegionAPIView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def get(self, request):
# #         area = Area.objects.all()
# #         serializer = RegionSerializer(area, many=True)
# #         return Response(serializer.data)

# #     def post(self, request):
# #         serializer = RegionSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)
    
# #     def put(self, request, pk):
# #         try:
# #             regions = Region.objects.get(pk=pk)
# #         except Region.DoesNotExist:
# #             return Response({'error': 'Область не найдена'}, status=404)

# #         serializer = RegionSerializer(region, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=400)
    
# #     def delete(self, request, pk):
# #         try:
# #             regions = Region.objects.get(pk=pk)
# #         except Region.DoesNotExist:
# #             return Response({'error': 'Область не найдена'}, status=404)

# #         regions.delete()
# #         return Response(status=204)

# # class AreaAPIView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def get(self, request):
# #         area = Area.objects.all()
# #         serializer = AreaSerializer(area, many=True)
# #         return Response(serializer.data)

# #     def post(self, request):
# #         serializer = AreaSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)
    
# #     def put(self, request, pk):
# #         try:
# #             area = Area.objects.get(pk=pk)
# #         except Area.DoesNotExist:
# #             return Response({'error': 'Район не найден'}, status=404)

# #         serializer = AreaSerializer(area, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=400)
    
# #     def delete(self, request, pk):
# #         try:
# #             area = Area.objects.get(pk=pk)
# #         except Area.DoesNotExist:
# #             return Response({'error': 'Район не найден'}, status=404)

# #         area.delete()
# #         return Response(status=204)

# # class CityAPIView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def get(self, request):
# #         city = City.objects.all()
# #         serializer = CitySerializer(city, many=True)
# #         return Response(serializer.data)

# #     def post(self, request):
# #         serializer = CitySerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)
    
# #     def put(self, request, pk):
# #         try:
# #             city = City.objects.get(pk=pk)
# #         except City.DoesNotExist:
# #             return Response({'error': 'Город не найден'}, status=404)

# #         serializer = CitySerializer(city, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=400)
    
# #     def delete(self, request, pk):
# #         try:
# #             city = City.objects.get(pk=pk)
# #         except City.DoesNotExist:
# #             return Response({'error': 'Город не найден'}, status=404)

# #         city.delete()
# #         return Response(status=204)
    
# # class DepartmentAPIView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def get(self, request):
# #         department = Department.objects.all()
# #         serializer = DepartmentSerializer(department, many=True)
# #         return Response(serializer.data)
    
# #     def post(self, request):
# #         serializer = DepartmentSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)
    
# #     def put(self, request, pk):
# #         try:
# #             department = Department.objects.get(pk=pk)
# #         except Department.DoesNotExist:
# #             return Response({'error': 'Отделение не найдено'}, status=404)

# #         serializer = DepartmentSerializer(department, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=400)
    
# #     def delete(self, request, pk):
# #         try:
# #             department = Department.objects.get(pk=pk)
# #         except Department.DoesNotExist:
# #             return Response({'error': 'Отделение не найдено'}, status=404)

# #         department.delete()
# #         return Response(status=204)

# # class ActivateTicketAPIView(APIView):
    
# #     def post(self, request):
# #         serializer = ActivateTicketSerializer(data=request.data)
# #         if serializer.is_valid():
# #             number = serializer.validated_data['number']
# #             try:
# #                 ticket = Ticket.objects.get(number=number)
# #                 ticket.activation_code = 'Active'
# #                 ticket.save()
# #                 return Response({'message': 'Статус билета обновлен.'})
# #             except Ticket.DoesNotExist:
# #                 return Response({'message': 'Билет с указанным номером не найден.'})
# #         else:
# #             return Response(serializer.errors, status=400)

# #endregion

#endregion