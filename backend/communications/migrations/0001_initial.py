import django.db.models.deletion
import uuid
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Candidate", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=120)), ("phone", models.CharField(max_length=30, unique=True)), ("email", models.EmailField(blank=True, max_length=254)), ("created_at", models.DateTimeField(auto_now_add=True))], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Template", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=80, unique=True)), ("body", models.TextField(max_length=1000)), ("created_at", models.DateTimeField(auto_now_add=True))]),
        migrations.CreateModel(name="Message", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("body", models.TextField(max_length=1000)), ("status", models.CharField(choices=[("queued", "Queued"), ("sent", "Sent"), ("delivered", "Delivered"), ("read", "Read"), ("failed", "Failed")], default="queued", max_length=12)), ("external_id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)), ("failure_reason", models.CharField(blank=True, max_length=255)), ("retryable", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="communications.candidate"))], options={"ordering": ["-created_at"]}),
    ]
