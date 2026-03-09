from __future__ import annotations
from typing import Dict, Generator, Optional, List
import heapq


class ResultadoBusqueda:
    def __init__(self, titulo: str, prioridad: int) -> None:
        self.titulo: str = titulo
        self.prioridad: int = prioridad

    def __lt__(self, other: ResultadoBusqueda) -> bool:
        return self.prioridad > other.prioridad


class TrieNode:
    def __init__(self) -> None:
        self.hijos: Dict[str, TrieNode] = {}
        self.documentos: List[ResultadoBusqueda] = []
        self.es_palabra: bool = False


class MotorBusqueda:
    def __init__(self) -> None:
        self.raiz = TrieNode()

    def indexar(self, titulo: str, prioridad: int) -> None:
        nodo = self.raiz
        for letra in titulo:
            if letra not in nodo.hijos:
                nodo.hijos[letra] = TrieNode()
            nodo = nodo.hijos[letra]
        nodo.es_palabra = True
        heapq.heappush(nodo.documentos, ResultadoBusqueda(titulo, prioridad))

    def buscar(self, prefijo: str) -> Generator[ResultadoBusqueda, None, None]:
        nodo = self.raiz
        for letra in prefijo:
            if letra not in nodo.hijos:
                return
            nodo = nodo.hijos[letra]
        yield from self._dfs_resultados(nodo)

    def _dfs_resultados(self, nodo: TrieNode) -> Generator[ResultadoBusqueda, None, None]:
        heap_copia = list(nodo.documentos)
        while heap_copia:
            yield heapq.heappop(heap_copia)
        for hijo in nodo.hijos.values():
            yield from self._dfs_resultados(hijo)
