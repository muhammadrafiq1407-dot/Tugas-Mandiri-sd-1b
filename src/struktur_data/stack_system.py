from __future__ import annotations
import time
from typing import List, Optional

from ..models.petugas import AktivitasPetugas


class StackEmptyError(Exception):
    pass


class StackSystem:
    MAX_CAPACITY: int = 10

    def __init__(self, max_capacity: int = 10) -> None:
        self.MAX_CAPACITY = max_capacity
        self._stack: List[AktivitasPetugas] = []
        self._last_execution_time_ns: int = 0

    @property
    def last_execution_time_ns(self) -> int:
        return self._last_execution_time_ns

    @property
    def last_execution_time_us(self) -> float:
        return self._last_execution_time_ns / 1_000.0

    @property
    def last_execution_time_ms(self) -> float:
        return self._last_execution_time_ns / 1_000_000.0

    def push(self, aktivitas: AktivitasPetugas) -> bool:
        start_time = time.perf_counter_ns()
        evicted = False
        try:
            if len(self._stack) >= self.MAX_CAPACITY:
                self._stack.pop(0)
                evicted = True
            self._stack.append(aktivitas)
            return evicted
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def pop(self) -> AktivitasPetugas:
        start_time = time.perf_counter_ns()
        try:
            if self.is_empty():
                raise StackEmptyError("Stack kosong! Tidak ada aktivitas yang dapat di-undo.")
            return self._stack.pop()
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def peek(self) -> AktivitasPetugas:
        start_time = time.perf_counter_ns()
        try:
            if self.is_empty():
                raise StackEmptyError("Stack kosong! Tidak ada aktivitas untuk dilihat.")
            return self._stack[-1]
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def size(self) -> int:
        start_time = time.perf_counter_ns()
        try:
            return len(self._stack)
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def display(self) -> List[str]:
        start_time = time.perf_counter_ns()
        try:
            # Iterasi mundur dari puncak stack (terbaru) ke dasar stack (terlama)
            return [str(act) for act in reversed(self._stack)]
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def get_all(self) -> List[AktivitasPetugas]:
        return list(reversed(self._stack))

    def clear(self) -> None:
        self._stack.clear()
