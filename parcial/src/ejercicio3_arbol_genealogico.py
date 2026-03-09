from __future__ import annotations
from typing import Dict, Optional, List, Generator
from collections import deque


class PersonaNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.hijos: Dict[str, PersonaNode] = {}
        self.padre: Optional[PersonaNode] = None

    def agregar_hijo(self, hijo: PersonaNode) -> None:
        hijo.padre = self
        self.hijos[hijo.nombre] = hijo

    def buscar(self, nombre: str) -> Optional[PersonaNode]:
        if self.nombre == nombre:
            return self
        for hijo in self.hijos.values():
            resultado = hijo.buscar(nombre)
            if resultado:
                return resultado
        return None

    def ancestros(self) -> Generator[str, None, None]:
        actual = self.padre
        while actual:
            yield actual.nombre
            actual = actual.padre

    def generaciones(self, nivel: int = 0) -> int:
        if not self.hijos:
            return nivel
        return max(hijo.generaciones(nivel + 1) for hijo in self.hijos.values())

    def recorrido(self) -> Generator[str, None, None]:
        cola = deque([self])
        while cola:
            actual = cola.popleft()
            yield actual.nombre
            for hijo in actual.hijos.values():
                cola.append(hijo)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.recorrido()
