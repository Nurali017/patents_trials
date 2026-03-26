#!/bin/sh
set -eu

: "${MINIO_ROOT_USER:?MINIO_ROOT_USER is required}"
: "${MINIO_ROOT_PASSWORD:?MINIO_ROOT_PASSWORD is required}"
: "${MINIO_BUCKET:?MINIO_BUCKET is required}"
: "${MINIO_ACCESS_KEY:?MINIO_ACCESS_KEY is required}"
: "${MINIO_SECRET_KEY:?MINIO_SECRET_KEY is required}"

until mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null 2>&1; do
  echo "Waiting for MinIO..."
  sleep 2
done

mc mb --ignore-existing "local/${MINIO_BUCKET}"
mc version enable "local/${MINIO_BUCKET}"

if ! mc admin user info local "$MINIO_ACCESS_KEY" >/dev/null 2>&1; then
  mc admin user add local "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"
fi

cat > /tmp/trials-media-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads"
      ],
      "Resource": [
        "arn:aws:s3:::${MINIO_BUCKET}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": [
        "arn:aws:s3:::${MINIO_BUCKET}/*"
      ]
    }
  ]
}
EOF

if ! mc admin policy info local trials-media-rw >/dev/null 2>&1; then
  mc admin policy create local trials-media-rw /tmp/trials-media-policy.json
fi

mc admin policy attach local trials-media-rw --user "$MINIO_ACCESS_KEY" >/dev/null

echo "MinIO initialized for bucket ${MINIO_BUCKET}"
