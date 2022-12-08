from collections.abc import Callable

class CustomEvent():
    def __init__(self) -> None:
        self._bound_functions:list[Callable[[],None]]=[]

    def bind(self, func:Callable[[],None]) -> None:
        self._bound_functions.append(func)

    def __call__(self) -> None:
        for func in self._bound_functions:
            func()

