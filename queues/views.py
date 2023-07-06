from rest_framework import generics, viewsets
from rest_framework.response import Response
from .models import Queue, Window
from .serializers import QueueSerializer, WindowSerializer
from ticket.models import Ticket
from datetime import datetime, timedelta, time

import tkinter as tk

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

class PrintTicket(viewsets.ViewSet):
    def get_ticket(self, request, pk=None): # Начало и конец рабочего дня
        science_time = datetime.now().time()
        start_time = time(9, 0)
        end_time = time(17, 59)

        if not (start_time <= science_time <= end_time):
            return Response({'error': 'Печать талонов недоступна в данный момент'}, status=403)

        try:
            customer = Queue.objects.get(ticket_number=pk)  # номер талона
        except Queue.DoesNotExist:
            return Response({'error': 'Талон с указанным номером не найден'},
                            status=404)

        def get_timeout(queue, customer):
            customers = Queue.objects.filter(queue=queue, is_served=False,
                                                      ticket_number__lt=customer.ticket_number)
            average_waiting_time = queue.average_waiting_time or 0  # время ожидания

            total_waiting_time = customers.count() * average_waiting_time  # время ожидания для всех талонов
            estimated_wait_time = datetime.now() + timedelta(
                minutes=total_waiting_time)  # времени ожидания для указанного талона
            time_remaining = estimated_wait_time - datetime.now()  # Вычисление оставшегося времени ожидания

            minutes = time_remaining.seconds // 60
            seconds = time_remaining.seconds % 60

            time_remaining_str = f"{minutes} минут, {seconds} секунд"

            return time_remaining_str

        ticket_data = {
            'Номер талона': customer.ticket_number,
            'Выдано': customer.created_at,
            'Имя посетителя': customer.user.username,
            'Наименование организации': 'RSK',
            'Очередь': customer.queue.name,
            'Номер окна': customer.queue.window_number,
            'Количество посетителей в очереди': Queue.objects.filter(queue=customer.queue, is_served=False,
                                                                        number__lt=customer.ticket_number).count(),
            'Примерное время ожидания': get_timeout(customer.queue, customer),
        }
        return Response(ticket_data)


# #модуль центрального табло
#
# #Создания главного окна
# root = tk.Tk()
# root.title('Центральное табло и аудио оповещение')
#
# #Обновление информации на табло
# def update_display():
#     display.delete('1.0', tk.END)
#     #номер талонов
#     display.insert(tk.END, 'Номер талона: ')
#     display.insert(tk.END, 'Окно оператора: ')
#
#     #отображение блоков информации
#     display.insert(tk.END, 'Логотип компании')

