from rest_framework import serializers
from .models import Roadmap

class RoadmapSerializer(serializers.ModelSerializer):
    student_username = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Roadmap
        fields = '__all__'
        read_only_fields = ('student', 'content', 'created_at')
