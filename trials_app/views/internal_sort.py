"""Internal webhook endpoints for service-to-service sync from Patents."""

import logging
import hmac

from django.conf import settings
from django.utils import timezone
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from trials_app.models import SortRecord

logger = logging.getLogger(__name__)


class IsInternalWebhookAuthenticated(permissions.BasePermission):
    """Token-based shared-secret auth for internal service-to-service webhooks."""

    message = "Invalid or missing internal webhook token."

    def has_permission(self, request, view) -> bool:
        expected = getattr(settings, "TRIALS_WEBHOOK_TOKEN", "") or ""
        if not expected:
            logger.error("TRIALS_WEBHOOK_TOKEN is not configured; rejecting webhook")
            return False
        header = request.META.get("HTTP_AUTHORIZATION", "")
        prefix = "Token "
        if not header.startswith(prefix):
            return False
        provided = header[len(prefix):].strip()
        return hmac.compare_digest(provided, expected)


class InternalSortUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class InternalSortByPatentIdView(APIView):
    """PATCH /api/internal/sorts/by-patent-id/<patent_sort_id>/ — webhook from Patents."""

    # Disable DRF's default TokenAuthentication: we use a shared-secret header
    # checked by IsInternalWebhookAuthenticated; auth here would only get in the way
    # by trying to resolve the shared secret as a per-user DRF Token.
    authentication_classes = []
    permission_classes = [IsInternalWebhookAuthenticated]

    def patch(self, request, patent_sort_id: int):
        serializer = InternalSortUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_name = serializer.validated_data["name"]

        record = SortRecord.objects.filter(sort_id=patent_sort_id).first()
        if record is None:
            logger.warning(
                "Internal webhook: SortRecord(sort_id=%s) not found; ignoring",
                patent_sort_id,
            )
            return Response(status=status.HTTP_204_NO_CONTENT)

        record.name = new_name
        record.synced_at = timezone.now()
        record.save(update_fields=["name", "synced_at", "updated_at"])
        return Response(
            {"sort_id": patent_sort_id, "name": record.name},
            status=status.HTTP_200_OK,
        )
