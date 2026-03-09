

# Parcial: Estructuras de Datos No Lineale Parte 2 
#### David Alejandro Avendaño Lopez


## Ejercicio 1: Arbol N-ario (Estructura Organizacional)

| Operacion     | Complejidad | Razon                                              |
|---------------|-------------|----------------------------------------------------|
| agregar_hijo  | O(1)        | Insercion directa en dict por clave                |
| buscar        | O(n)        | Recorre todos los nodos en peor caso               |
| eliminar_hijo | O(1)        | Eliminacion directa en dict por clave              |
| __iter__      | O(n)        | Visita cada nodo exactamente una vez (DFS)         |


### Codigo: 

```python
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
```

### Explicación

En este ejercicio se implementa un árbol N-ario para representar una estructura organizacional. La idea es que cada nodo represente una persona o un área dentro de la organización y que pueda tener varios hijos, que serían sus subordinados.

Cada nodo guarda su nombre y un diccionario con sus hijos. Usar un diccionario ayuda a poder acceder o eliminar un hijo rápidamente usando su nombre como clave.

El método agregar_hijo sirve para añadir un nuevo nodo como subordinado, pero primero revisa que no exista otro con el mismo nombre.
El método buscar recorre el árbol de forma recursiva hasta encontrar el nodo con el nombre que se está buscando.

También se puede eliminar un hijo con eliminar_hijo, que básicamente lo borra del diccionario.

Para recorrer todo el árbol se usa un recorrido DFS, que visita primero el nodo actual y luego sus hijos. Esto se implementa con un generador para poder iterar fácilmente por todos los nodos.

Finalmente, el método mostrar_arbol imprime la estructura con indentación para que se vea mejor la jerarquía.

---

## Ejercicio 2: Trie (Autocompletado de Comandos)

| Operacion    | Complejidad | Razon                                              |
|--------------|-------------|----------------------------------------------------|
| insertar     | O(m)        | Recorre m caracteres de la palabra                 |
| buscar       | O(m)        | Navega m nodos hasta el fin de la palabra          |
| sugerir      | O(m + k)    | O(m) para llegar al prefijo, O(k) para k resultados|
| eliminar     | O(m)        | Recursion de profundidad m                         |

### Codigo: 

```python
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
```


### Explicación

En este ejercicio se implementa un Trie, que es una estructura que se usa mucho para manejar palabras o sistemas de autocompletado.

La idea es que cada nodo representa un carácter y las palabras se forman siguiendo caminos dentro del árbol. Cada nodo guarda un diccionario con los siguientes caracteres posibles.

El método insertar recorre letra por letra la palabra y va creando nodos si no existen. Cuando llega al final marca ese nodo como fin de palabra.

El método buscar revisa si una palabra completa existe en el Trie. También se incluye tiene_prefijo, que permite saber si hay alguna palabra que empiece con cierto prefijo.

La función sugerir sirve para el autocompletado. Primero encuentra el nodo donde termina el prefijo y luego recorre todos los nodos debajo de él para devolver las palabras completas.

También hay un método eliminar, que borra una palabra usando recursión y elimina nodos que ya no se usan para mantener el Trie limpio.

---

## Ejercicio 3: Hash Table (Registro de Estudiantes)

| Operacion    | Complejidad      | Razon                                              |
|--------------|------------------|----------------------------------------------------|
| __setitem__  | O(1) amortizado  | O(1) directo, O(n) solo al hacer rehash            |
| __getitem__  | O(1) promedio    | Acceso por indice de bucket; O(n) si todo colisiona|
| __delitem__  | O(1) promedio    | Igual que getitem, recorre la cadena del bucket    |
| __contains__ | O(1) promedio    | Delega a getitem                                   |

### Codigo: 

```python
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
```

### Explicación

En este ejercicio se implementa una tabla hash para guardar información de estudiantes usando su ID como clave.

La tabla funciona con un arreglo donde cada posición puede guardar una lista de elementos. Esto se hace para manejar colisiones, que ocurren cuando diferentes claves generan el mismo índice.

El método _hash calcula la posición donde debería ir la clave usando una función hash basada en los caracteres del ID.

Cuando se agrega un estudiante con __setitem__, primero se revisa el factor de carga. Si la tabla está muy llena se hace un rehash, que básicamente consiste en aumentar la capacidad de la tabla y volver a insertar todos los elementos.

El método __getitem__ permite obtener un estudiante usando su ID. Si hay colisiones, se recorre la lista hasta encontrar el correcto.

También se pueden eliminar elementos con __delitem__, y hay otros métodos como __contains__ o __len__ para usar la estructura de forma parecida a un diccionario normal de Python.

---

## Ejercicio 4: Priority Queue (Planificador de Kernel)

| Operacion          | Complejidad  | Razon                                            |
|--------------------|--------------|--------------------------------------------------|
| encolar            | O(log n)     | heappush mantiene la propiedad del heap          |
| desencolar         | O(log n)     | heappop restaura la propiedad del heap           |
| peek               | O(1)         | Acceso directo al indice 0 del arreglo           |
| cambiar_prioridad  | O(n)         | Busqueda lineal + heapify para reconstruir       |
| ejecutar_todas     | O(n log n)   | n llamadas a desencolar, cada una O(log n)       |


### Codigo: 

```python
from __future__ import annotations
import heapq
import time
from dataclasses import dataclass, field
from typing import Optional, Iterator
from enum import IntEnum


class Prioridad(IntEnum):
    CRITICA  = 0
    ALTA     = 1
    NORMAL   = 2
    BAJA     = 3
    INACTIVO = 4


@dataclass
class Tarea:
    nombre: str
    prioridad: int
    timestamp: float = field(default_factory=time.time)
    pid: Optional[int] = field(default=None)
    descripcion: str = field(default="")

    def __lt__(self, otra: Tarea) -> bool:
        if self.prioridad != otra.prioridad:
            return self.prioridad < otra.prioridad
        return self.timestamp < otra.timestamp

    def __le__(self, otra: Tarea) -> bool:
        return self == otra or self < otra

    def __eq__(self, otra: object) -> bool:
        if not isinstance(otra, Tarea):
            return NotImplemented
        return self.nombre == otra.nombre and self.prioridad == otra.prioridad

    def __repr__(self) -> str:
        nivel = Prioridad(self.prioridad).name if self.prioridad in Prioridad._value2member_map_ else str(self.prioridad)
        return f"Tarea(nombre='{self.nombre}', prioridad={nivel}, pid={self.pid})"


class PlanificadorKernel:
    def __init__(self) -> None:
        self._heap: list[Tarea] = []
        self._pid_counter: int = 1000

    def encolar(self, tarea: Tarea) -> Tarea:
        if tarea.pid is None:
            tarea.pid = self._pid_counter
            self._pid_counter += 1
        heapq.heappush(self._heap, tarea)
        return tarea

    def desencolar(self) -> Tarea:
        if self.esta_vacia():
            raise IndexError("No hay tareas en la cola.")
        return heapq.heappop(self._heap)

    def peek(self) -> Optional[Tarea]:
        return self._heap[0] if self._heap else None

    def esta_vacia(self) -> bool:
        return len(self._heap) == 0

    def ejecutar_todas(self) -> Iterator[Tarea]:
        while not self.esta_vacia():
            yield self.desencolar()

    def cambiar_prioridad(self, nombre: str, nueva_prioridad: int) -> bool:
        for tarea in self._heap:
            if tarea.nombre == nombre:
                tarea.prioridad = nueva_prioridad
                heapq.heapify(self._heap)
                return True
        return False

    def __len__(self) -> int:
        return len(self._heap)

    def __repr__(self) -> str:
        return f"PlanificadorKernel(tareas_pendientes={len(self)})"
```


### Explicación

En este ejercicio se implementa una cola de prioridad que simula cómo un sistema operativo podría manejar tareas o procesos.

Las tareas se guardan en un heap usando el módulo heapq de Python. Esto permite que siempre se pueda acceder rápidamente a la tarea con mayor prioridad.

Cada tarea tiene un nombre, una prioridad y un timestamp. El timestamp sirve para mantener el orden cuando dos tareas tienen la misma prioridad.

El método encolar agrega una tarea al heap y le asigna un PID si no tiene uno.
El método desencolar retira la tarea con mayor prioridad.

peek permite ver cuál es la siguiente tarea a ejecutar sin eliminarla.

También se puede cambiar la prioridad de una tarea con cambiar_prioridad, lo que requiere reorganizar el heap para mantener el orden correcto.

Finalmente, ejecutar_todas permite ejecutar todas las tareas en orden de prioridad hasta que la cola quede vacía.
