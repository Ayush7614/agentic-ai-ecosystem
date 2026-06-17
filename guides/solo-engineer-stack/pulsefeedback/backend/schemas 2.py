from typing import Literal

from pydantic import BaseModel, Field

FeedbackStatus = Literal["new", "triaged", "done"]


class FeedbackCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=5000)
    email: str | None = Field(default=None, max_length=320)


class FeedbackUpdate(BaseModel):
    status: FeedbackStatus


class FeedbackOut(BaseModel):
    id: int
    title: str
    body: str
    email: str | None
    status: FeedbackStatus
    created_at: str


class AnalyticsEvent(BaseModel):
    event: str = Field(min_length=1, max_length=100)
    properties: dict | None = None


class CSATWebhook(BaseModel):
    score: float = Field(ge=1, le=5)
    comment: str | None = None


class StackToolStatus(BaseModel):
    id: int
    name: str
    role: str
    artifact: str
    demo_url: str | None = None
    live: bool
