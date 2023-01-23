"""Contains a class with an event class.
"""
import logging
from collections.abc import Callable

from .logger import Logger

log:logging.Logger = Logger(__name__).get_logger()

class CustomEvent():
    """Created to call multiple functions.
    Calling the object calls all bound functions.
    """
    def __init__(self, name:str) -> None:
        self._bound_functions:list[Callable[[],None]]=[]
        
        try:
            assert name is not None
        except AssertionError:
            log.exception("An event with no name was created. An empty constructor is considered deprecated.")
            name="<Unnamed>"
        # remove newlines to parse it to packets
        filtered_name=name.replace("\n"," ")
        self.bind(lambda: log.info("%s called", filtered_name))
        self.name:str=filtered_name

    def bind(self, func:Callable[[],None]) -> None:
        """Binds `func` to the event,
        `func` will be called when calling this event.
        """
        self._bound_functions.append(func)

    def __call__(self) -> None:
        for func in self._bound_functions:
            func()
