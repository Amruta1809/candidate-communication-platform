from django.test import TestCase
from rest_framework.test import APIClient
from .models import Candidate, Message

class MessagingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.good = Candidate.objects.create(name="Riya", phone="+919876543210", email="riya@example.com")
        self.bad = Candidate.objects.create(name="Bad number", phone="not-a-phone", email="bad@example.com")

    def test_bulk_send_isolated_and_reports_each_result(self):
        response = self.client.post("/api/messages/send/", {"candidate_ids": [self.good.id, self.bad.id], "body": "Interview reminder"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data), 2)
        self.assertEqual({m.status for m in Message.objects.all()}, {"read", "failed"})

    def test_create_candidate_returns_json(self):
        response = self.client.post("/api/candidates/", {"name": "New candidate", "phone": "+919123456789", "email": "new@example.com"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "New candidate")

    def test_duplicate_provider_callback_is_safe(self):
        message = Message.objects.create(candidate=self.good, body="Hello", status="delivered")
        payload = {"external_id": str(message.external_id), "status": "sent"}
        self.client.post("/api/provider/status/", payload, format="json")
        self.client.post("/api/provider/status/", payload, format="json")
        message.refresh_from_db()
        self.assertEqual(message.status, "delivered")
