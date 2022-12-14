from typing import Optional
from pydantic import BaseModel


class Config(BaseModel):
    vk_token: str
    tg_token: str
    notified: list[int]
    rules: dict[str, str]


class Event(BaseModel):
    event_type: str
    event_url: str
    text: str
    tags: list[str]
    event_type: str


class WsEvent(BaseModel):
    code: int
    event: Optional[Event]


class Credentials(BaseModel):
    endpoint: str
    key: str


class Rule(BaseModel):
    value: str
    tag: str
