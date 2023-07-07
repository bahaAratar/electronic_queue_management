from rest_framework import serializers
from .models import Queue, Window, Operathor
from account.serializers import ProfileSerializer
from ticket.serializers import TicketSerializer


class WindowSerializer(serializers.ModelSerializer):
    # operator = ProfileSerializer()
    # ticket = TicketSerializer()

    class Meta:
        model = Window
        fields = '__all__'

class QueueSerializer(serializers.ModelSerializer):
    ticket = serializers.StringRelatedField()

    class Meta:
        model = Queue
        fields = '__all__'

class OperathorSerializer(serializers.ModelSerializer):
    window = WindowSerializer()
    client = QueueSerializer(many=True)

    class Meta:
        model = Operathor
        fields = '__all__'