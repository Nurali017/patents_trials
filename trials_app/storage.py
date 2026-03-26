import mimetypes
import os
from urllib.parse import urlencode, urljoin

from django.conf import settings
from django.core import signing
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import FileResponse
from django.utils._os import safe_join
from django.utils.encoding import filepath_to_uri

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:  # pragma: no cover - exercised only when optional deps are missing locally
    BotoCoreError = None
    ClientError = None

try:
    from storages.backends.s3boto3 import S3Boto3Storage
except ImportError:  # pragma: no cover - exercised only when optional deps are missing locally
    S3Boto3Storage = None


class MinioMediaStorage(S3Boto3Storage if S3Boto3Storage is not None else FileSystemStorage):
    file_overwrite = False
    default_acl = None
    custom_domain = None
    querystring_auth = False

    def __init__(self, *args, **kwargs):
        if S3Boto3Storage is None:
            raise RuntimeError('django-storages and boto3 must be installed for MEDIA_BACKEND=minio')

        kwargs.setdefault('bucket_name', settings.MINIO_BUCKET)
        kwargs.setdefault('access_key', settings.MINIO_ACCESS_KEY)
        kwargs.setdefault('secret_key', settings.MINIO_SECRET_KEY)
        kwargs.setdefault('endpoint_url', settings.MINIO_ENDPOINT)
        kwargs.setdefault('region_name', settings.MINIO_REGION)
        kwargs.setdefault('addressing_style', 'path')
        kwargs.setdefault('signature_version', 's3v4')
        kwargs.setdefault('file_overwrite', False)
        kwargs.setdefault('default_acl', None)
        kwargs.setdefault('querystring_auth', False)
        kwargs.setdefault('custom_domain', None)
        super().__init__(*args, **kwargs)


DOWNLOAD_SIGNER_SALT = 'document-download'


def uses_minio_storage():
    return getattr(settings, 'MEDIA_BACKEND', 'filesystem') == 'minio'


def is_storage_error(exc):
    current = exc
    while current is not None:
        if isinstance(current, (OSError, PermissionError)):
            return True
        if BotoCoreError is not None and isinstance(current, BotoCoreError):
            return True
        if ClientError is not None and isinstance(current, ClientError):
            return True
        current = current.__cause__ or current.__context__
    return False


def get_document_file_name(document):
    if not getattr(document, 'file', None):
        return ''
    return document.file.name or ''


def primary_file_exists(file_name):
    if not file_name:
        return False
    return default_storage.exists(file_name)


def get_legacy_file_path(file_name):
    if not file_name:
        return None
    try:
        return safe_join(settings.LEGACY_MEDIA_ROOT, file_name)
    except Exception:
        return None


def legacy_file_exists(file_name):
    file_path = get_legacy_file_path(file_name)
    return bool(file_path and os.path.exists(file_path))


def document_file_exists(document):
    file_name = get_document_file_name(document)
    return primary_file_exists(file_name) or legacy_file_exists(file_name)


def build_media_url(file_name, request=None):
    relative_url = urljoin(settings.MEDIA_URL, filepath_to_uri(file_name))
    if request is None:
        return relative_url
    return request.build_absolute_uri(relative_url)


def build_signed_download_url(document, request=None):
    token = signing.dumps(
        {
            'document_id': document.id,
            'file_name': get_document_file_name(document),
        },
        salt=DOWNLOAD_SIGNER_SALT,
    )
    relative_url = f'/api/documents/{document.id}/signed-download/?{urlencode({"token": token})}'
    if request is None:
        return relative_url
    return request.build_absolute_uri(relative_url)


def validate_signed_download_token(document, token):
    if not token:
        return False

    try:
        payload = signing.loads(
            token,
            salt=DOWNLOAD_SIGNER_SALT,
            max_age=settings.MINIO_PRESIGNED_URL_EXPIRY_SECONDS,
        )
    except signing.SignatureExpired:
        return False
    except signing.BadSignature:
        return False

    return (
        payload.get('document_id') == document.id
        and payload.get('file_name') == get_document_file_name(document)
    )


def get_document_file_url(document, request=None):
    file_name = get_document_file_name(document)
    if not file_name:
        return None

    try:
        if primary_file_exists(file_name):
            if uses_minio_storage():
                return build_signed_download_url(document, request=request)
            return build_media_url(file_name, request=request)
    except Exception as exc:
        if not is_storage_error(exc):
            raise

    if legacy_file_exists(file_name):
        return build_media_url(file_name, request=request)

    return None


def stream_primary_file(document):
    file_name = get_document_file_name(document)
    file_obj = default_storage.open(file_name, 'rb')
    content_type = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
    return FileResponse(
        file_obj,
        as_attachment=True,
        filename=os.path.basename(file_name),
        content_type=content_type,
    )


def stream_legacy_file(document):
    file_name = get_document_file_name(document)
    file_path = get_legacy_file_path(file_name)
    content_type = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=os.path.basename(file_name),
        content_type=content_type,
    )
