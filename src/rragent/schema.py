from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class TraceEvent:
    step: str
    agent: str
    status: str
    summary: str
    details: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
