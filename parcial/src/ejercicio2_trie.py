from __future__ import annotations
from typing import Optional, Generator


class TrieNode:
    def __init__(self) -> None:
        self.hijos: dict[str, TrieNode] = {}
        self.es_fin: bool = False
        self.palabra_completa: Optional[str] = None


class Trie:
    def __init__(self) -> None:
        self._raiz: TrieNode = TrieNode()
        self._total_palabras: int = 0

    def insertar(self, palabra: str) -> None:
        if not palabra:
            raise ValueError("La palabra no puede estar vacia.")
        nodo = self._raiz
        for caracter in palabra:
            if caracter not in nodo.hijos:
                nodo.hijos[caracter] = TrieNode()
            nodo = nodo.hijos[caracter]
        if not nodo.es_fin:
            nodo.es_fin = True
            nodo.palabra_completa = palabra
            self._total_palabras += 1

    def buscar(self, palabra: str) -> bool:
        nodo = self._navegar_hasta(palabra)
        return nodo is not None and nodo.es_fin

    def tiene_prefijo(self, prefijo: str) -> bool:
        return self._navegar_hasta(prefijo) is not None

    def sugerir(self, prefijo: str) -> Generator[str, None, None]:
        nodo_inicio = self._navegar_hasta(prefijo)
        if nodo_inicio is None:
            return
        yield from self._recolectar_palabras(nodo_inicio)

    def eliminar(self, palabra: str) -> bool:
        return self._eliminar_recursivo(self._raiz, palabra, 0)

    def _navegar_hasta(self, prefijo: str) -> Optional[TrieNode]:
        nodo = self._raiz
        for caracter in prefijo:
            if caracter not in nodo.hijos:
                return None
            nodo = nodo.hijos[caracter]
        return nodo

    def _recolectar_palabras(self, nodo: TrieNode) -> Generator[str, None, None]:
        if nodo.es_fin and nodo.palabra_completa:
            yield nodo.palabra_completa
        for hijo in nodo.hijos.values():
            yield from self._recolectar_palabras(hijo)

    def _eliminar_recursivo(self, nodo: TrieNode, palabra: str, indice: int) -> bool:
        if indice == len(palabra):
            if not nodo.es_fin:
                return False
            nodo.es_fin = False
            nodo.palabra_completa = None
            self._total_palabras -= 1
            return True
        caracter = palabra[indice]
        if caracter not in nodo.hijos:
            return False
        self._eliminar_recursivo(nodo.hijos[caracter], palabra, indice + 1)
        if not nodo.hijos[caracter].hijos and not nodo.hijos[caracter].es_fin:
            del nodo.hijos[caracter]
        return True

    def __len__(self) -> int:
        return self._total_palabras

    def __contains__(self, palabra: str) -> bool:
        return self.buscar(palabra)


if __name__ == "__main__":
    trie = Trie()
    comandos = [
        "git commit", "git clone", "git checkout", "git branch",
        "git pull", "git push", "git status", "git log",
        "docker run", "docker build", "docker ps", "docker stop",
        "python --version", "python -m pytest", "pip install",
        "ls", "ls -la", "ln -s",
    ]
    for cmd in comandos:
        trie.insertar(cmd)

    for prefijo in ["git", "docker", "ls", "py", "xyz"]:
        print(f"'{prefijo}': {list(trie.sugerir(prefijo))}")

    print("git commit" in trie)
    print("git comi" in trie)
