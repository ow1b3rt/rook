from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class Evidence(BaseModel):
    platform: str
    external_id: str
    kind: Literal["article", "post", "comment", "listing", "video"]
    url: HttpUrl
    text_original: str
    title: str | None = None
    parent_external_id: str | None = None
    published_at: datetime | None = None
    collected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    location: str | None = None
    location_basis: Literal["confirmed", "inferred", "unknown"] = "unknown"
    metrics: dict[str, Any] = Field(default_factory=dict)
    extractor: str
    extra: dict[str, Any] = Field(default_factory=dict)
