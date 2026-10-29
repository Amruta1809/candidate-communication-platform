from rest_framework import serializers
from .models import Candidate, Message, Template

class CandidateSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Candidate
        fields = ["id", "name", "phone", "email", "created_at", "message_count"]

class MessageSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source="candidate.name", read_only=True)
    class Meta:
        model = Message
        fields = ["id", "candidate", "candidate_name", "body", "status", "external_id", "failure_reason", "retryable", "created_at", "updated_at"]

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ["id", "name", "body", "created_at"]
