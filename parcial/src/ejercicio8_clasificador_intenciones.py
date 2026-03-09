from __future__ import annotations
from typing import Dict, Generator, Optional, List


class TrieNode:
    def __init__(self) -> None:
        self.hijos: Dict[str, TrieNode] = {}
        self.es_palabra: bool = False
        self.intencion: Optional[str] = None


class ClasificadorIntenciones:
    def __init__(self) -> None:
        self.raiz = TrieNode()

    def registrar_palabra(self, palabra: str, intencion: str) -> None:
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                nodo.hijos[letra] = TrieNode()
            nodo = nodo.hijos[letra]
        nodo.es_palabra = True
        nodo.intencion = intencion

    def clasificar(self, texto: str) -> Dict[str, int]:
        conteo: Dict[str, int] = {}
        for palabra in texto.lower().split():
            nodo = self.raiz
            for letra in palabra:
                if letra not in nodo.hijos:
                    break
                nodo = nodo.hijos[letra]
            else:
                if nodo.es_palabra and nodo.intencion:
                    intencion = nodo.intencion
                    conteo[intencion] = conteo.get(intencion, 0) + 1
        return conteo

    def sugerencias_prefijo(self, prefijo: str) -> Generator[str, None, None]:
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
