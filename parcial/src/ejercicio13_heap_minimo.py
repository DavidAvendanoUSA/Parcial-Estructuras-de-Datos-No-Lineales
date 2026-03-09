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
