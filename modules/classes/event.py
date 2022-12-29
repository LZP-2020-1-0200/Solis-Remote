"""Contains a class with an event class.
"""
from collections.abc import Callable

class CustomEvent():
    """Created to call multiple functions.
    Calling the object calls all bound functions.
    """
    def __init__(self) -> None:
        self._bound_functions:list[Callable[[],None]]=[]

    def bind(self, func:Callable[[],None]) -> None:
        """Binds `func` to the event,
        `func` will be called when calling this event.
        """
        self._bound_functions.append(func)

    def __call__(self) -> None:
        for func in self._bound_functions:
            func()
