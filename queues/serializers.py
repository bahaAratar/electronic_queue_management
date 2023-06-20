from rest_framework import serializers
from .models import Queue, Window

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = '__all__'

class WindowSerializer(serializers.ModelSerializer):
    queue = QueueSerializer(read_only=True)

    class Meta:
        model = Window
        fields = '__all__'