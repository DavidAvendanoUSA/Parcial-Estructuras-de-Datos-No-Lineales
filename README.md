
# Abstract
El presente trabajo intenta implementar y explorar distintas estructuras de datos no lineales y aplicar estas estructuras para resolver dichos problemas utilizando tales estructuras para resolver problemas de cómputo en la disciplina de estructuras de datos no lineales impartida en el programa de computación de la inteligencia artificial. específicamente, se han implementado estructuras de datos no lineales de los siguientes tipos: árboles n-arios, estructuras de prueba, tablas hash, colas de prioridad basadas en montones. Los árboles N-arios se emplearon para representar jerarquías, como en organizaciones, genealogías, menús de aplicaciones y grafos de dependencias de software, permitiendo recorridos tanto en amplitud como en profundidad con una complejidad de O(n). Las estructuras Trie fueron utilizadas para crear sistemas de autocompletado, corrección de errores ortográficos, clasificación de intenciones y motores de búsqueda, aprovechando su eficacia de O(L) en inserciones y búsquedas por prefijo. Las tablas hash con encadenamiento y redimensionamiento dinámico facilitaron el almacenamiento y recuperación de registros de estudiantes en tiempo O(1) amortizado. Finalmente, las colas de prioridad implementadas sobre heaps binarios permitieron diseñar planificadores de tareas y simuladores de red con gestión eficiente de prioridades en O(log n). La integración de estas estructuras demuestra cómo cada una complementa a las demás dentro de un sistema computacional completo: los árboles organizan información jerárquica, los Trie optimizan la búsqueda textual, las tablas hash garantizan acceso rápido por clave y los heaps gestionan recursos bajo criterios de prioridad, conformando en conjunto una solución robusta y eficiente aplicable a sistemas operativos, motores de búsqueda y plataformas de gestión académica.

# Parcial de Datos No Lineales Parte 1
#### David Alejandro Avendaño Lopez
---

## Ejercicios Complejos - Arboles N-arios

---

### Ejercicio 1: Estructura Organizacional

```python
from __future__ import annotations
from typing import Dict, Optional, Generator
from collections import deque


class OrganizacionNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.hijos: Dict[str, OrganizacionNode] = {}

    def agregar_hijo(self, hijo: OrganizacionNode) -> None:
        self.hijos[hijo.nombre] = hijo

    def buscar(self, nombre: str) -> Optional[OrganizacionNode]:
        if self.nombre == nombre:
            return self
        for hijo in self.hijos.values():
            resultado = hijo.buscar(nombre)
            if resultado:
                return resultado
        return None

    def profundidad(self, nombre: str, nivel: int = 0) -> int:
        if self.nombre == nombre:
            return nivel
        for hijo in self.hijos.values():
            resultado = hijo.profundidad(nombre, nivel + 1)
            if resultado != -1:
                return resultado
        return -1

    def recorrido_por_niveles(self) -> Generator[str, None, None]:
        cola = deque([self])
        while cola:
            actual = cola.popleft()
            yield actual.nombre
            for hijo in actual.hijos.values():
                cola.append(hijo)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.recorrido_por_niveles()
```

**Complejidad:**

| Operacion   | Complejidad |
|-------------|-------------|
| Insertar    | O(1)        |
| Buscar      | O(n)        |
| Eliminar    | O(n)        |
| Recorrido   | O(n)        |

---

### Ejercicio 3: Arbol Genealogico

```python
from __future__ import annotations
from typing import Dict, Optional, List, Generator
from collections import deque


class PersonaNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.hijos: Dict[str, PersonaNode] = {}
        self.padre: Optional[PersonaNode] = None

    def agregar_hijo(self, hijo: PersonaNode) -> None:
        hijo.padre = self
        self.hijos[hijo.nombre] = hijo

    def buscar(self, nombre: str) -> Optional[PersonaNode]:
        if self.nombre == nombre:
            return self
        for hijo in self.hijos.values():
            resultado = hijo.buscar(nombre)
            if resultado:
                return resultado
        return None

    def ancestros(self) -> Generator[str, None, None]:
        actual = self.padre
        while actual:
            yield actual.nombre
            actual = actual.padre

    def generaciones(self, nivel: int = 0) -> int:
        if not self.hijos:
            return nivel
        return max(hijo.generaciones(nivel + 1) for hijo in self.hijos.values())

    def recorrido(self) -> Generator[str, None, None]:
        cola = deque([self])
        while cola:
            actual = cola.popleft()
            yield actual.nombre
            for hijo in actual.hijos.values():
                cola.append(hijo)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.recorrido()
```

**Complejidad:**

| Operacion    | Complejidad |
|--------------|-------------|
| Generaciones | O(n)        |
| Recorrido    | O(n)        |

---

### Ejercicio 4: Menu de Aplicacion

```python
from __future__ import annotations
from typing import Dict, Optional, Generator
from collections import deque


class MenuNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.subopciones: Dict[str, MenuNode] = {}

    def agregar_subopcion(self, nodo: MenuNode) -> None:
        self.subopciones[nodo.nombre] = nodo

    def buscar(self, nombre: str) -> Optional[MenuNode]:
        if self.nombre == nombre:
            return self
        for sub in self.subopciones.values():
            resultado = sub.buscar(nombre)
            if resultado:
                return resultado
        return None

    def recorrido_por_niveles(self) -> Generator[str, None, None]:
        cola = deque([self])
        while cola:
            actual = cola.popleft()
            yield actual.nombre
            for sub in actual.subopciones.values():
                cola.append(sub)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.recorrido_por_niveles()
```

**Complejidad:**

| Operacion | Complejidad |
|-----------|-------------|
| Recorrido | O(n)        |

---

### Ejercicio 5: Dependencias de Software

```python
from __future__ import annotations
from typing import Dict, Optional, Generator
from collections import deque


class ModuloNode:
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.dependencias: Dict[str, ModuloNode] = {}

    def agregar_dependencia(self, modulo: ModuloNode) -> None:
        self.dependencias[modulo.nombre] = modulo

    def buscar(self, nombre: str) -> Optional[ModuloNode]:
        if self.nombre == nombre:
            return self
        for dep in self.dependencias.values():
            resultado = dep.buscar(nombre)
            if resultado:
                return resultado
        return None

    def impacto_de_cambio(self, nombre: str) -> Generator[str, None, None]:
        if self.nombre == nombre:
            yield from self.recorrido()
        for dep in self.dependencias.values():
            yield from dep.impacto_de_cambio(nombre)

    def grado(self) -> int:
        return len(self.dependencias)

    def recorrido(self) -> Generator[str, None, None]:
        cola = deque([self])
        while cola:
            actual = cola.popleft()
            yield actual.nombre
            for dep in actual.dependencias.values():
                cola.append(dep)

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.recorrido()
```

**Complejidad:**

| Operacion           | Complejidad |
|---------------------|-------------|
| Agregar dependencia | O(1)        |
| Buscar modulo       | O(n)        |
| Impacto de cambio   | O(n)        |
| Grado del nodo      | O(1)        |
| Recorrido           | O(n)        |

---

## Ejercicios Complejos - Trie

---

### Ejercicio 6: Autocompletado

```python
from __future__ import annotations
from typing import Dict, Generator, Optional


class TrieNode:
    def __init__(self) -> None:
        self.hijos: Dict[str, TrieNode] = {}
        self.es_palabra: bool = False


class Autocompletado:
    def __init__(self) -> None:
        self.raiz = TrieNode()

    def insertar(self, palabra: str) -> None:
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                nodo.hijos[letra] = TrieNode()
            nodo = nodo.hijos[letra]
        nodo.es_palabra = True

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
```

**Complejidad:**

| Operacion      | Complejidad |
|----------------|-------------|
| Insertar       | O(L)        |
| Buscar prefijo | O(L)        |
| Sugerencias    | O(L + k)    |
| Espacio        | O(n * L)    |

---

### Ejercicio 7: Corrector Ortografico

```python
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
```

**Complejidad:**

| Operacion           | Complejidad |
|---------------------|-------------|
| Cargar diccionario  | O(n * L)    |
| Verificar palabra   | O(L)        |
| Buscar prefijo      | O(L)        |
| Generar sugerencias | O(L + k)    |
| Espacio             | O(n * L)    |

---

### Ejercicio 8: Clasificador de Intenciones

```python
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
```

**Complejidad:**

| Operacion               | Complejidad |
|-------------------------|-------------|
| Clasificar texto        | O(m * L)    |
| Sugerencias por prefijo | O(L + k)    |
| Espacio                 | O(n * L)    |

---

### Ejercicio 9: Diccionario Multilenguaje

```python
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
```

---

### Ejercicio 10: Motor de Busqueda

```python
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
```

**Complejidad:**

| Operacion            | Complejidad |
|----------------------|-------------|
| DFS resultados       | O(n)        |
| Insertar en heap     | O(log n)    |
| Buscar con prioridad | O(n log n)  |
| Espacio              | O(n * L)    |

---

## Ejercicios Complejos - Tablas Hash

---

### Ejercicio 11: Registro de Estudiantes

```python
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
```

---

### Ejercicio 12: Comparacion Hash vs Trie

```python
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
```

**Comparacion de estructuras:**

| Criterio               | Trie       | Hash         |
|------------------------|------------|--------------|
| Buscar palabra exacta  | O(L)       | O(1) promedio|
| Buscar por prefijo     | Eficiente  | No eficiente |
| Memoria                | Mayor      | Menor        |
| Autocompletado         | Excelente  | No natural   |
| Escalabilidad prefijo  | Excelente  | Baja         |
| Colisiones             | No existen | Si existen   |

---

## Ejercicios Complejos - Heaps

---

### Ejercicio 13: Heap Minimo

```python
from __future__ import annotations
from typing import List, Optional
import heapq


class HeapMinimo:
    def __init__(self) -> None:
        self.heap: List[int] = []

    def insertar(self, valor: int) -> None:
        heapq.heappush(self.heap, valor)

    def extraer_minimo(self) -> int:
        if not self.heap:
            raise IndexError("El heap esta vacio")
        return heapq.heappop(self.heap)

    def ver_minimo(self) -> Optional[int]:
        return self.heap[0] if self.heap else None

    def construir(self, valores: List[int]) -> None:
        self.heap = valores[:]
        heapq.heapify(self.heap)

    def __len__(self) -> int:
        return len(self.heap)
```

**Complejidad:**

| Operacion          | Complejidad |
|--------------------|-------------|
| Insertar           | O(log n)    |
| Extraer minimo     | O(log n)    |
| Acceder minimo     | O(1)        |
| Construccion total | O(n)        |
| Espacio            | O(n)        |

---

### Ejercicio 14: Planificador de Tareas

```python
from __future__ import annotations
from typing import List
import heapq
import time


class Tarea:
    def __init__(self, nombre: str, prioridad: int) -> None:
        self.nombre: str = nombre
        self.prioridad: int = prioridad
        self.timestamp: float = time.time()

    def __lt__(self, otra: Tarea) -> bool:
        if self.prioridad != otra.prioridad:
            return self.prioridad < otra.prioridad
        return self.timestamp < otra.timestamp

    def __repr__(self) -> str:
        return f"Tarea(nombre='{self.nombre}', prioridad={self.prioridad})"


class PlanificadorTareas:
    def __init__(self) -> None:
        self.heap: List[Tarea] = []

    def agregar_tarea(self, tarea: Tarea) -> None:
        heapq.heappush(self.heap, tarea)

    def ejecutar_siguiente(self) -> Tarea:
        if not self.heap:
            raise IndexError("No hay tareas pendientes")
        return heapq.heappop(self.heap)

    def ver_siguiente(self) -> Tarea:
        if not self.heap:
            raise IndexError("No hay tareas pendientes")
        return self.heap[0]

    def tareas_pendientes(self) -> int:
        return len(self.heap)
```

**Complejidad:**

| Operacion            | Complejidad |
|----------------------|-------------|
| Insertar tarea       | O(log n)    |
| Ejecutar siguiente   | O(log n)    |
| Ver siguiente (peek) | O(1)        |
| Espacio              | O(n)        |

---

### Ejercicio 15: Simulacion de Red

```python
from __future__ import annotations
from typing import List
import heapq
import time


class Paquete:
    def __init__(self, identificador: str, prioridad: int, tamano: int) -> None:
        self.identificador: str = identificador
        self.prioridad: int = prioridad
        self.tamano: int = tamano
        self.timestamp: float = time.time()

    def __lt__(self, otro: Paquete) -> bool:
        if self.prioridad != otro.prioridad:
            return self.prioridad < otro.prioridad
        return self.timestamp < otro.timestamp

    def __repr__(self) -> str:
        return f"Paquete(id='{self.identificador}', prioridad={self.prioridad}, tamano={self.tamano})"


class SimuladorRed:
    def __init__(self, ancho_banda: int) -> None:
        self.ancho_banda: int = ancho_banda
        self.cola: List[Paquete] = []
        self.transmitidos: List[Paquete] = []

    def recibir_paquete(self, paquete: Paquete) -> None:
        heapq.heappush(self.cola, paquete)

    def transmitir_siguiente(self) -> Paquete:
        if not self.cola:
            raise IndexError("No hay paquetes en cola")
        paquete = heapq.heappop(self.cola)
        self.transmitidos.append(paquete)
        return paquete

    def paquetes_pendientes(self) -> int:
        return len(self.cola)

    def ver_siguiente(self) -> Paquete:
        if not self.cola:
            raise IndexError("No hay paquetes en cola")
        return self.cola[0]
```


# Parcial: Estructuras de Datos No Lineale Parte 2 


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
