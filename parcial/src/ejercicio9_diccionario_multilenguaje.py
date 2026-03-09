from __future__ import annotations
from typing import Dict, Generator, Optional


class TrieNode:
    def __init__(self) -> None:
        self.hijos: Dict[str, TrieNode] = {}
        self.traducciones: Dict[str, str] = {}
        self.es_palabra: bool = False


class DiccionarioMultilenguaje:
    def __init__(self) -> None:
        self.raiz = TrieNode()

    def insertar(self, palabra: str, idioma: str, traduccion: str) -> None:
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                nodo.hijos[letra] = TrieNode()
            nodo = nodo.hijos[letra]
        nodo.es_palabra = True
        nodo.traducciones[idioma] = traduccion

    def buscar(self, palabra: str) -> Optional[TrieNode]:
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                return None
            nodo = nodo.hijos[letra]
        return nodo if nodo.es_palabra else None

    def traducir(self, palabra: str, idioma: str) -> Optional[str]:
        nodo = self.buscar(palabra)
        if nodo is None:
            return None
        return nodo.traducciones.get(idioma)

    def palabras_por_prefijo(self, prefijo: str) -> Generator[str, None, None]:
        nodo = self.raiz
        for letra in prefijo:
            if letra not in nodo.hijos:
                return
            nodo = nodo.hijos[letra]
        yield from self._dfs(nodo, prefijo)

    def _dfs(self, nodo: TrieNode, prefijo_actual: str) -> Generator[str, None, None]:
        if nodo.es_palabra:
            yield prefijo_actual
        for letra, hijo in nodo.hijos.items():
            yield from self._dfs(hijo, prefijo_actual + letra)
