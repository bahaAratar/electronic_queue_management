from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from .models import Queue, Window, Operathor
from .serializers import QueueSerializer, WindowSerializer, OperathorSerializer
from django.core.exceptions import ObjectDoesNotExist

class QueueListCreateAPIView(generics.ListCreateAPIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

class QueueRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    permission_classes = [IsAdminUser]

class WindowListCreteAPIView(generics.ListCreateAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer
    permission_classes = [IsAdminUser]

class WindowRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_works:
            return Response('окно выключено', status=400)
        
        try:
            next_queue = Queue.objects.filter(ticket__status='active').order_by('id').first() # для брони просто order_by пот времени сделать
        except ObjectDoesNotExist:
            next_queue = None
        
        operathor = Operathor.objects.filter(operathor=request.user).latest('id')

        # Проверка, что окно включено и имеет билет
        if instance.ticket == None:
            instance.is_available = False
            instance.ticket = next_queue.ticket
            instance.save()

            # Обновление статуса билета из очереди
            next_queue.ticket.status = 'no_active'
            next_queue.ticket.save()
            next_queue.window = instance
            next_queue.is_served = True
            next_queue.service_start = timezone.now()
            next_queue.save()

            return Response(f'Билет {instance.ticket.number} успешно привязан к окну {instance.id}', status=200)

        # Получение следующего билета из очереди и привязка его к окну
        if next_queue:
            # Удаление текущего билета из очереди
            old_ticket = instance.ticket
            instance.ticket = None
            instance.is_available = True
            instance.save()

            # Обновление статуса билета из очереди
            next_queue.ticket.status = 'not_active'
            next_queue.ticket.save()
            next_queue.window = instance
            next_queue.is_served = True
            next_queue.service_end = timezone.now()
            next_queue.save()

            # Привязка следующего билета из очереди к окну\
            instance.is_available = False
            instance.ticket = next_queue.ticket
            instance.save()

            next_queue.service_start= timezone.now()
            next_queue.save()
            
            # Оператор
            operathor.client.add(next_queue)
            operathor.save()

            return Response(f'Билет {old_ticket.number} успешно удален из окна и привязан следующий билет {instance.ticket.number} из очереди.', status=200)
        else:
            return Response('Нет следующего билета в очереди.', status=400)

class WindowToggleAPIView(generics.UpdateAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        queue = Queue.objects.filter(ticket__status='active').order_by('id').first()

        # Выключение окна
        if instance.is_works:
            instance.is_works = False
            instance.operator = None
            instance.is_available = True
            instance.ticket = None
            instance.save()

            if queue:
                queue.service_end = timezone.now()
                queue.save()
            
            operathor = Operathor.objects.filter(window=instance).first()
            if operathor:
                operathor.word_end = timezone.now()
                operathor.save()

            return Response('Окно успешно выключено.', status=200)
        
        if queue == None:
            return Response('В очереди нет билетов со статусом "active".', status=400)
            
        # Включение окна
        if instance.is_works == False:
            
            instance.is_available = False
            instance.is_works = True
            instance.operator = request.user
            instance.ticket = queue.ticket
            instance.save()

            # Обновление статуса билета из очереди
            queue.ticket.status = 'not_active'
            queue.ticket.save()
            queue.window = instance
            queue.service_start = timezone.now()
            queue.is_served = True
            queue.save()

            # Добавление информации об операторе 
            operathor = Operathor.objects.create(
                operathor=request.user,
                window=instance,
                word_start=timezone.now(),
                word_end = None
            )
            operathor.client.add(queue)
            operathor.save()

            return Response('Окно успешно включено.', status=200)

        return Response('Некорректный запрос.', status=400)
    
class OperathorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Operathor.objects.all()
    serializer_class = OperathorSerializer
    permission_classes = [IsAdminUser]