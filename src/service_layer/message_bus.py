from typing import Callable, Dict, List, Any

class MessageBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, event: Any):
        for handler in self._handlers.get(event_type, []):
            handler(event)
