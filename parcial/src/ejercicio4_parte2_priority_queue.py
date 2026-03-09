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


if __name__ == "__main__":
    planificador = PlanificadorKernel()
    tareas = [
        Tarea("actualizar_pantalla",  Prioridad.BAJA),
        Tarea("leer_teclado",         Prioridad.ALTA),
        Tarea("interrupcion_disco",   Prioridad.CRITICA),
        Tarea("proceso_usuario_app",  Prioridad.NORMAL),
        Tarea("recolector_basura",    Prioridad.INACTIVO),
        Tarea("sincronizar_reloj",    Prioridad.ALTA),
        Tarea("interrupcion_red",     Prioridad.CRITICA),
        Tarea("comprimir_logs",       Prioridad.BAJA),
    ]
    for tarea in tareas:
        planificador.encolar(tarea)

    print(planificador)
    print(planificador.peek())
    for tarea in planificador.ejecutar_todas():
        print(f"{tarea.nombre} ({Prioridad(tarea.prioridad).name}) PID={tarea.pid}")
