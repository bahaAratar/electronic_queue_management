from rest_framework import generics
from rest_framework.response import Response
from .models import Queue, Window
from .serializers import QueueSerializer, WindowSerializer
from ticket.models import Ticket

class QueueListCreateAPIView(generics.ListCreateAPIView):
    queryset = Queue.objects.order_by('created_at').filter(is_served=True)
    serializer_class = QueueSerializer

class WindowListCreateAPIView(generics.ListCreateAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer

class WindowRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer

    def perform_update(self, serializer):
        window = serializer.save()
        if not window.is_available and not window.current_ticket:
            window.current_ticket = self.get_next_ticket(window)
            window.save()

    def get_next_ticket(self, window):
        queue = Queue.objects.filter(operator=window.operator, is_served=False).order_by('created_at').first()
        if queue:
            queue.is_served = True
            queue.save()
            return queue.ticket
        return None

# region 

# class QueueViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queues = Queue.objects.filter(is_served=False)
#         queue_data = []
#         for queue in queues:
#             operator_username = queue.operator.username
#             ticket_data = TicketSerializer(queue.ticket).data
#             queue_data.append({
#                 'ticket_number': ticket_data['number'],
#                 'window_number': operator_username
#             })
#         return Response(queue_data)

#     def create(self, request):
#         ticket_number = request.data.get('ticket_number')
#         operator = request.user
#         ticket = Ticket.objects.get(number=ticket_number)

#         # Проверка, что билет принадлежит текущему пользователю
#         if ticket.owner != request.user:
#             return Response("Недостаточно прав для добавления в очередь", status=403)

#         # Проверка, что билет не был добавлен ранее
#         if Queue.objects.filter(ticket=ticket).exists():
#             return Response("Билет уже добавлен в очередь", status=400)

#         # Добавление в очередь
#         queue = Queue.objects.create(operator=operator, ticket=ticket, is_served=False)
#         return Response("Билет успешно добавлен в очередь", status=201)

#     def destroy(self, request, pk=None):
#         try:
#             queue = Queue.objects.get(id=pk, operator=request.user)
#             queue.delete()
#             return Response("Клиент успешно удален из очереди", status=204)
#         except Queue.DoesNotExist:
#             return Response("Указанный клиент не найден в очереди", status=404)

#endregion