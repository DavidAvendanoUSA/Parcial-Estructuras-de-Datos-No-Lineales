from __future__ import annotations
from typing import Dict, Optional, Generator
from collections import deque


class ModuloNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.dependencias: Dict[str, ModuloNode] = {}

    def agregar_dependencia(self, modulo: ModuloNode) -> None:
        self.dependencias[modulo.nombre] = modulo

    def buscar(self, nombre: str) -> Optional[ModuloNode]:
        if self.nombre == nombre:
            return self
        for dep in self.dependencias.values():
            resultado = dep.buscar(nombre)
            if resultado:
                return resultado
        return None

    def impacto_de_cambio(self, nombre: str) -> Generator[str, None, None]:
        if self.nombre == nombre:
            yield from self.recorrido()
        for dep in self.dependencias.values():
            yield from dep.impacto_de_cambio(nombre)

    def grado(self) -> int:
        return len(self.dependencias)

    def recorrido(self) -> Generator[str, None, None]:
        cola = deque([self])
        while cola:
            actual = cola.popleft()
            yield actual.nombre
            for dep in actual.dependencias.values():
                cola.append(dep)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.recorrido()
