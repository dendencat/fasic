from __future__ import annotations

from typing import Any

from .config import get_settings


def get_s3_client() -> Any | None:
    """Return a boto3 S3 client if boto3 is available; otherwise None.

    This keeps T1 lightweight while providing a future hook.
    """
    try:
        import boto3  # type: ignore
    except Exception:
        return None

    s = get_settings()
    session = boto3.session.Session()
    return session.client(
        "s3",
        endpoint_url=s.s3_endpoint,
        aws_access_key_id=s.s3_access_key,
        aws_secret_access_key=s.s3_secret_key,
        region_name=s.s3_region,
    )

