from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class UrlObject:
    name: str
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
