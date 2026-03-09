from __future__ import annotations
from typing import Dict, Generator, Optional, List


class TrieNode:
    def __init__(self) -> None:
        self.hijos: Dict[str, TrieNode] = {}
        self.es_palabra: bool = False


class CorrectorOrtografico:
    def __init__(self) -> None:
        self.raiz = TrieNode()

    def cargar_diccionario(self, palabras: List[str]) -> None:
        for palabra in palabras:
            self._insertar(palabra)

    def _insertar(self, palabra: str) -> None:
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                nodo.hijos[letra] = TrieNode()
            nodo = nodo.hijos[letra]
        nodo.es_palabra = True

    def verificar(self, palabra: str) -> bool:
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                return False
            nodo = nodo.hijos[letra]
        return nodo.es_palabra

    def buscar_prefijo(self, prefijo: str) -> Optional[TrieNode]:
        nodo = self.raiz
        for letra in prefijo:
            if letra not in nodo.hijos:
                return None
            nodo = nodo.hijos[letra]
        return nodo

    def sugerencias(self, prefijo: str) -> Generator[str, None, None]:
        nodo = self.buscar_prefijo(prefijo)
        if nodo is None:
            return
        yield from self._dfs(nodo, prefijo)

    def _dfs(self, nodo: TrieNode, prefijo_actual: str) -> Generator[str, None, None]:
        if nodo.es_palabra:
            yield prefijo_actual
        for letra, hijo in nodo.hijos.items():
            yield from self._dfs(hijo, prefijo_actual + letra)
