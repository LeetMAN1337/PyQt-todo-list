from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: Optional[int]
    time: str
    text: str
    created_at: str

    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time,
            'text': self.text,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            time=data['time'],
            text=data['text'],
            created_at=data['created_at']
        )