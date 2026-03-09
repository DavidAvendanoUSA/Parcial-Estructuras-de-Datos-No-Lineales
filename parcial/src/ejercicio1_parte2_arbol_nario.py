from __future__ import annotations
from typing import Optional, Iterator, Generator


class OrganizacionNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.hijos: dict[str, OrganizacionNode] = {}

    def agregar_hijo(self, nodo: OrganizacionNode) -> None:
        if nodo.nombre in self.hijos:
            raise ValueError(f"Ya existe un hijo con el nombre '{nodo.nombre}'.")
        self.hijos[nodo.nombre] = nodo

    def buscar(self, nombre: str) -> Optional[OrganizacionNode]:
        if self.nombre == nombre:
            return self
        for hijo in self.hijos.values():
            resultado = hijo.buscar(nombre)
            if resultado:
                return resultado
        return None

    def eliminar_hijo(self, nombre: str) -> None:
        if nombre not in self.hijos:
            raise KeyError(f"No existe un hijo con el nombre '{nombre}'.")
        del self.hijos[nombre]

    def _recorrer_dfs(self) -> Generator[OrganizacionNode, None, None]:
        yield self
        for hijo in self.hijos.values():
            yield from hijo._recorrer_dfs()

    def __iter__(self) -> Iterator[OrganizacionNode]:
        yield from self._recorrer_dfs()

    def __repr__(self) -> str:
        return f"OrganizacionNode(nombre='{self.nombre}', hijos={list(self.hijos.keys())})"

    def __str__(self) -> str:
        return self.nombre

    def mostrar_arbol(self, nivel: int = 0) -> None:
        prefijo = "    " * nivel + ("- " if nivel > 0 else "")
        print(f"{prefijo}{self.nombre}")
        for hijo in self.hijos.values():
            hijo.mostrar_arbol(nivel + 1)


if __name__ == "__main__":
    rectoria = OrganizacionNode("Rectoria")
    fac_ing = OrganizacionNode("Facultad de Ingenieria")
    fac_cien = OrganizacionNode("Facultad de Ciencias")
    fac_hum = OrganizacionNode("Facultad de Humanidades")

    for prog in ["Ing. Sistemas", "Ing. Civil", "Ing. Electronica"]:
        fac_ing.agregar_hijo(OrganizacionNode(prog))
    for prog in ["Matematicas", "Fisica", "Quimica"]:
        fac_cien.agregar_hijo(OrganizacionNode(prog))
    for prog in ["Filosofia", "Historia"]:
        fac_hum.agregar_hijo(OrganizacionNode(prog))

    rectoria.agregar_hijo(fac_ing)
    rectoria.agregar_hijo(fac_cien)
    rectoria.agregar_hijo(fac_hum)

    rectoria.mostrar_arbol()
    for nodo in rectoria:
        print(nodo.nombre)
    print(rectoria.buscar("Ing. Sistemas"))
