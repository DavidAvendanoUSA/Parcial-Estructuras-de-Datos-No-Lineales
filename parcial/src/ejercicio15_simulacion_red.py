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
