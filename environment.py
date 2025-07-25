from __future__ import annotations

class Environment:

    def __init__(self, enclosing: Environment|None = None):
        self.__enclosing: Environment|None = enclosing
        self.__map = {}

    def define(self, name: str, value: object) -> None:
        self.__map[name] = value

    def get(self, name: str) -> object:
        if name in self.__map:
            return self.__map[name]

        if self.__enclosing is not None:
            return self.__enclosing.get(name)

        raise RuntimeError(f"Undefined variable {name}. Lock tf in bruh")

    def assign(self, name: str, value: object) -> None:
        if name in self.__map:
            self.__map[name] = value
            return

        if self.__enclosing is not None:
            self.__enclosing.assign(name, value)
            return

        raise RuntimeError(f"ts undefined: {name}.")
