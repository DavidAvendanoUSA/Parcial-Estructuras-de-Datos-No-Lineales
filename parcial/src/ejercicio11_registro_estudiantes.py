from __future__ import annotations
from typing import List, Tuple, Optional


class HashTable:
    def __init__(self, capacidad: int = 10) -> None:
        self.capacidad: int = capacidad
        self.tabla: List[List[Tuple[str, str]]] = [[] for _ in range(capacidad)]
        self.tamano: int = 0

    def _hash(self, clave: str) -> int:
        return sum(ord(c) for c in clave) % self.capacidad

    def __setitem__(self, clave: str, valor: str) -> None:
        indice = self._hash(clave)
        for i, (k, _) in enumerate(self.tabla[indice]):
            if k == clave:
                self.tabla[indice][i] = (clave, valor)
                return
        self.tabla[indice].append((clave, valor))
        self.tamano += 1
        if self.tamano / self.capacidad > 0.75:
            self._redimensionar()

    def __getitem__(self, clave: str) -> Optional[str]:
        indice = self._hash(clave)
        for k, v in self.tabla[indice]:
            if k == clave:
                return v
        raise KeyError(clave)

    def __delitem__(self, clave: str) -> None:
        indice = self._hash(clave)
        for i, (k, _) in enumerate(self.tabla[indice]):
            if k == clave:
                self.tabla[indice].pop(i)
                self.tamano -= 1
                return
        raise KeyError(clave)

    def __contains__(self, clave: str) -> bool:
        try:
            self[clave]
            return True
        except KeyError:
            return False

    def _redimensionar(self) -> None:
        entradas = [(k, v) for bucket in self.tabla for k, v in bucket]
        self.capacidad *= 2
        self.tabla = [[] for _ in range(self.capacidad)]
        self.tamano = 0
        for k, v in entradas:
            self[k] = v

    def items(self):
        for bucket in self.tabla:
            for k, v in bucket:
                yield k, v
