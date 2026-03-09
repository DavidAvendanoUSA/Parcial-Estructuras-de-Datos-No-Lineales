import time
from typing import List


class TrieNode:
    def __init__(self) -> None:
        self.hijos = {}
        self.es_palabra = False


class Trie:
    def __init__(self) -> None:
        self.raiz = TrieNode()

    def insertar(self, palabra: str) -> None:
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                nodo.hijos[letra] = TrieNode()
            nodo = nodo.hijos[letra]
        nodo.es_palabra = True

    def buscar(self, palabra: str) -> bool:
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                return False
            nodo = nodo.hijos[letra]
        return nodo.es_palabra

    def buscar_prefijo(self, prefijo: str) -> bool:
        nodo = self.raiz
        for letra in prefijo:
            if letra not in nodo.hijos:
                return False
            nodo = nodo.hijos[letra]
        return True


class HashDiccionario:
    def __init__(self) -> None:
        self.tabla = {}

    def insertar(self, palabra: str) -> None:
        self.tabla[palabra] = True

    def buscar(self, palabra: str) -> bool:
        return palabra in self.tabla

    def buscar_prefijo(self, prefijo: str) -> bool:
        return any(p.startswith(prefijo) for p in self.tabla)


def comparar(palabras: List[str], consultas: List[str]) -> None:
    trie = Trie()
    hash_dic = HashDiccionario()

    for p in palabras:
        trie.insertar(p)
        hash_dic.insertar(p)

    inicio = time.perf_counter()
    for c in consultas:
        trie.buscar(c)
    tiempo_trie_exacto = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for c in consultas:
        hash_dic.buscar(c)
    tiempo_hash_exacto = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for c in consultas:
        trie.buscar_prefijo(c)
    tiempo_trie_prefijo = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for c in consultas:
        hash_dic.buscar_prefijo(c)
    tiempo_hash_prefijo = time.perf_counter() - inicio

    print(f"Busqueda exacta  - Trie: {tiempo_trie_exacto:.6f}s | Hash: {tiempo_hash_exacto:.6f}s")
    print(f"Busqueda prefijo - Trie: {tiempo_trie_prefijo:.6f}s | Hash: {tiempo_hash_prefijo:.6f}s")
