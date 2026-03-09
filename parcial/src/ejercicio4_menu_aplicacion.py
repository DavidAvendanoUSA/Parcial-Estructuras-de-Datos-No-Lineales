from __future__ import annotations
from typing import Dict, Optional, Generator
from collections import deque


class MenuNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.subopciones: Dict[str, MenuNode] = {}

    def agregar_subopcion(self, nodo: MenuNode) -> None:
        self.subopciones[nodo.nombre] = nodo

    def buscar(self, nombre: str) -> Optional[MenuNode]:
        if self.nombre == nombre:
            return self
        for sub in self.subopciones.values():
            resultado = sub.buscar(nombre)
            if resultado:
                return resultado
        return None

    def recorrido_por_niveles(self) -> Generator[str, None, None]:
        cola = deque([self])
        while cola:
            actual = cola.popleft()
            yield actual.nombre
            for sub in actual.subopciones.values():
                cola.append(sub)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.recorrido_por_niveles()
