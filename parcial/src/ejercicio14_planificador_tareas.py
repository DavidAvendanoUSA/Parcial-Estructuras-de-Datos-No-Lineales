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
