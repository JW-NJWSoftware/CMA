import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "resilienceai-cma"
AWS_S3_ENDPOINT_URL="https://fra1.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION="https://resilienceai-cma.fra1.digitaloceanspaces.com"

DEFAULT_FILE_STORAGE = "ResilienceAI.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "ResilienceAI.cdn.backends.StaticRootS3Boto3Storage"