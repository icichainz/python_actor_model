import sys
from typing import Any
import pykka

GetMessages = object()

class PlainActor(pykka.ThreadingActor):
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        super().__init__(*_args, **_kwargs)
        self.stored_messages = []
    
    def on_receive(self, message: Any) -> Any:
        if message is GetMessages:
            return self.stored_messages
        self.stored_messages.append(message)
        return None
    
if __name__ == "__main__":
    actor = PlainActor.start()
    i = 0
    while i < 1000:
        actor.tell({"no":"Norway","se":"Sweden"})
        actor.tell({"a":3,"b":4,"c":5})
        print(actor.ask(GetMessages))
        i =i + 1
    actor.stop
    