from rest_framework import serializers
from .models import Queue, Window
# from ticket.serializers import TicketSerializer


class WindowSerializer(serializers.ModelSerializer):
    operator = serializers.StringRelatedField(read_only=True)
    ticket = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Window
        fields = '__all__'

class QueueSerializer(serializers.ModelSerializer):
    ticket = serializers.StringRelatedField()

    class Meta:
        model = Queue
        fields = '__all__'