"""A provider adapter; replace SimulatedProvider with a real vendor implementation."""
import re
from dataclasses import dataclass
from .models import Message

@dataclass
class ProviderResult:
    status: str
    reason: str = ""
    retryable: bool = False

class SimulatedProvider:
    def send(self, message: Message) -> ProviderResult:
        recipient = message.candidate.phone
        text = message.body.lower()
        if not re.fullmatch(r"\+?[0-9][0-9 -]{7,}", recipient) or "invalid" in text:
            return ProviderResult("failed", "The recipient address is invalid.", False)
        if "temporary" in text and not message.failure_reason:
            return ProviderResult("failed", "The communication service is temporarily unavailable. Try again shortly.", True)
        return ProviderResult("read")

provider = SimulatedProvider()

STATUS_RANK = {"queued": 0, "sent": 1, "delivered": 2, "read": 3, "failed": 4}

def apply_provider_update(message: Message, result: ProviderResult):
    # Duplicate callbacks and stale callbacks are safely ignored.
    if message.status == "failed" and result.status != "failed":
        return message
    if result.status != "failed" and STATUS_RANK[result.status] < STATUS_RANK.get(message.status, 0):
        return message
    message.status = result.status
    message.failure_reason = result.reason
    message.retryable = result.retryable
    message.save(update_fields=["status", "failure_reason", "retryable", "updated_at"])
    return message
