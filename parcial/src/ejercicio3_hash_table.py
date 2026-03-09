from __future__ import annotations
from typing import Optional, Iterator, Any
from dataclasses import dataclass, field


@dataclass
class Estudiante:
    id_estudiante: str
    nombre: str
    programa: str
    semestre: int = 1

    def __repr__(self) -> str:
        return (
            f"Estudiante(id='{self.id_estudiante}', "
            f"nombre='{self.nombre}', programa='{self.programa}')"
        )


@dataclass
class _Entrada:
    clave: str
    valor: Any
    siguiente: Optional[_Entrada] = field(default=None, repr=False)


class HashTable:
    _FACTOR_CARGA_MAX: float = 0.75
    _CAPACIDAD_INICIAL: int = 16

    def __init__(self, capacidad: int = _CAPACIDAD_INICIAL) -> None:
        if capacidad < 1:
            raise ValueError("La capacidad debe ser al menos 1.")
        self._capacidad: int = capacidad
        self._tabla: list[Optional[_Entrada]] = [None] * self._capacidad
        self._tamano: int = 0

    def _hash(self, clave: str) -> int:
        hash_val: int = 5381
        for caracter in clave:
            hash_val = ((hash_val << 5) + hash_val) + ord(caracter)
        return hash_val % self._capacidad

    def _rehash(self) -> None:
        nueva_capacidad = self._capacidad * 2
        capacidad_anterior = self._capacidad
        tabla_anterior = self._tabla
        self._capacidad = nueva_capacidad
        self._tabla = [None] * nueva_capacidad
        self._tamano = 0
        for i in range(capacidad_anterior):
            nodo = tabla_anterior[i]
            while nodo is not None:
                self._insertar_entrada(nodo.clave, nodo.valor)
                nodo = nodo.siguiente

    def _insertar_entrada(self, clave: str, valor: Any) -> None:
        indice = self._hash(clave)
        nodo = self._tabla[indice]
        while nodo is not None:
            if nodo.clave == clave:
                nodo.valor = valor
                return
            nodo = nodo.siguiente
        nueva_entrada = _Entrada(clave=clave, valor=valor, siguiente=self._tabla[indice])
        self._tabla[indice] = nueva_entrada
        self._tamano += 1

    def __setitem__(self, clave: str, valor: Any) -> None:
        if self.factor_carga >= self._FACTOR_CARGA_MAX:
            self._rehash()
        self._insertar_entrada(clave, valor)

    def __getitem__(self, clave: str) -> Any:
        indice = self._hash(clave)
        nodo = self._tabla[indice]
        while nodo is not None:
            if nodo.clave == clave:
                return nodo.valor
            nodo = nodo.siguiente
        raise KeyError(f"Clave '{clave}' no encontrada.")

    def __delitem__(self, clave: str) -> None:
        indice = self._hash(clave)
        nodo = self._tabla[indice]
        anterior: Optional[_Entrada] = None
        while nodo is not None:
            if nodo.clave == clave:
                if anterior:
                    anterior.siguiente = nodo.siguiente
                else:
                    self._tabla[indice] = nodo.siguiente
                self._tamano -= 1
                return
            anterior = nodo
            nodo = nodo.siguiente
        raise KeyError(f"Clave '{clave}' no encontrada.")

    def __contains__(self, clave: str) -> bool:
        try:
            self[clave]
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[str]:
        for i in range(self._capacidad):
            nodo = self._tabla[i]
            while nodo is not None:
                yield nodo.clave
                nodo = nodo.siguiente

    def __repr__(self) -> str:
        return (
            f"HashTable(tamano={self._tamano}, "
            f"capacidad={self._capacidad}, "
            f"factor_carga={self.factor_carga:.2f})"
        )

    @property
    def factor_carga(self) -> float:
        return self._tamano / self._capacidad

    def obtener(self, clave: str, por_defecto: Any = None) -> Any:
        try:
            return self[clave]
        except KeyError:
            return por_defecto

    def items(self) -> Iterator[tuple[str, Any]]:
        for clave in self:
            yield clave, self[clave]


if __name__ == "__main__":
    tabla: HashTable = HashTable(capacidad=8)
    estudiantes = [
        Estudiante("EST001", "Ana Garcia",     "Ing. Sistemas", 4),
        Estudiante("EST002", "Carlos Ruiz",    "Matematicas",   2),
        Estudiante("EST003", "Maria Lopez",    "Ing. Civil",    6),
        Estudiante("EST004", "Luis Torres",    "Fisica",        3),
        Estudiante("EST005", "Sofia Martinez", "Quimica",       5),
        Estudiante("EST006", "Pedro Gomez",    "Filosofia",     1),
        Estudiante("EST007", "Laura Sanchez",  "Historia",      7),
    ]
    for est in estudiantes:
        tabla[est.id_estudiante] = est

    print(tabla)
    print(tabla["EST003"])
    tabla["EST001"] = Estudiante("EST001", "Ana Garcia H.", "Ing. Sistemas", 5)
    print(tabla["EST001"])
    print("EST002" in tabla)
    del tabla["EST007"]
    for id_est, est in tabla.items():
        print(f"{id_est}: {est.nombre}")
