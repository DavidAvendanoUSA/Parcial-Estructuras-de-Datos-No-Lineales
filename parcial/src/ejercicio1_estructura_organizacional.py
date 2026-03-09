from __future__ import annotations
from typing import Dict, Optional, Generator
from collections import deque


class OrganizacionNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.hijos: Dict[str, OrganizacionNode] = {}

    def agregar_hijo(self, hijo: OrganizacionNode) -> None:
        self.hijos[hijo.nombre] = hijo

    def buscar(self, nombre: str) -> Optional[OrganizacionNode]:
        if self.nombre == nombre:
            return self
        for hijo in self.hijos.values():
            resultado = hijo.buscar(nombre)
            if resultado:
                return resultado
        return None

    def profundidad(self, nombre: str, nivel: int = 0) -> int:
        if self.nombre == nombre:
            return nivel
        for hijo in self.hijos.values():
            resultado = hijo.profundidad(nombre, nivel + 1)
            if resultado != -1:
                return resultado
        return -1

    def recorrido_por_niveles(self) -> Generator[str, None, None]:
        cola = deque([self])
        while cola:
            actual = cola.popleft()
            yield actual.nombre
            for hijo in actual.hijos.values():
                cola.append(hijo)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.recorrido_por_niveles()
