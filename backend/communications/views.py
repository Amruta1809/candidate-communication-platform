from django.db.models import Count, Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Candidate, Message, Template
from .provider import ProviderResult, apply_provider_update, provider
from .serializers import CandidateSerializer, MessageSerializer, TemplateSerializer

@api_view(["GET", "POST"])
def candidates(request):
    if request.method == "POST":
        serializer = CandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    query = request.query_params.get("search", "").strip()
    items = Candidate.objects.annotate(message_count=Count("messages"))
    if query:
        items = items.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
    return Response(CandidateSerializer(items, many=True).data)

@api_view(["GET"])
def candidate_detail(request, candidate_id):
    try: candidate = Candidate.objects.get(pk=candidate_id)
    except Candidate.DoesNotExist: return Response({"detail": "Candidate not found."}, status=404)
    return Response({"candidate": CandidateSerializer(candidate).data, "messages": MessageSerializer(candidate.messages.all(), many=True).data})

def dispatch(message):
    result = provider.send(message)
    return apply_provider_update(message, result)

@api_view(["POST"])
def send_messages(request):
    ids = request.data.get("candidate_ids", [])
    body = str(request.data.get("body", "")).strip()
    if not ids: return Response({"detail": "Select at least one candidate."}, status=400)
    if not body: return Response({"detail": "A message cannot be empty."}, status=400)
    if len(body) > 1000: return Response({"detail": "Keep messages under 1,000 characters."}, status=400)
    people = list(Candidate.objects.filter(id__in=ids))
    found = {p.id for p in people}
    if len(found) != len(set(ids)): return Response({"detail": "One or more selected candidates no longer exist."}, status=400)
    results = []
    for person in people:
        message = Message.objects.create(candidate=person, body=body.replace("{{name}}", person.name))
        results.append(dispatch(message))
    return Response(MessageSerializer(results, many=True).data, status=201)

@api_view(["POST"])
def retry(request, message_id):
    try: message = Message.objects.select_related("candidate").get(pk=message_id)
    except Message.DoesNotExist: return Response({"detail": "Message not found."}, status=404)
    if message.status != "failed" or not message.retryable:
        return Response({"detail": "This message cannot be retried."}, status=400)
    message.failure_reason = ""
    message.retryable = False
    message.status = "queued"
    message.save()
    return Response(MessageSerializer(dispatch(message)).data)

@api_view(["POST"])
def provider_webhook(request):
    try: message = Message.objects.get(external_id=request.data["external_id"])
    except (Message.DoesNotExist, KeyError): return Response({"detail": "Unknown message reference."}, status=404)
    value = request.data.get("status")
    if value not in dict(Message.Status.choices): return Response({"detail": "Unsupported status."}, status=400)
    updated = apply_provider_update(message, ProviderResult(value, request.data.get("reason", ""), bool(request.data.get("retryable"))))
    return Response(MessageSerializer(updated).data)

@api_view(["GET", "POST"])
def templates(request):
    if request.method == "POST":
        s = TemplateSerializer(data=request.data); s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data, status=201)
    return Response(TemplateSerializer(Template.objects.all(), many=True).data)

@api_view(["GET"])
def health(request):
    messages = Message.objects.all()
    return Response({"status": "operational", "sent": messages.exclude(status="queued").count(), "delivered": messages.filter(status__in=["delivered", "read"]).count(), "failed": messages.filter(status="failed").count()})
