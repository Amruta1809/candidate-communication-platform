import uuid
from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

class Message(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        SENT = "sent", "Sent"
        DELIVERED = "delivered", "Delivered"
        READ = "read", "Read"
        FAILED = "failed", "Failed"
    candidate = models.ForeignKey(Candidate, related_name="messages", on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.QUEUED)
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    failure_reason = models.CharField(max_length=255, blank=True)
    retryable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

class Template(models.Model):
    name = models.CharField(max_length=80, unique=True)
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
