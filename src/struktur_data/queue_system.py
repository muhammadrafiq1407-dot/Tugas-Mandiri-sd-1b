from __future__ import annotations
from collections import deque
import time
from typing import Deque, List, Optional

from ..models.mahasiswa import Mahasiswa


class QueueEmptyError(Exception):
    pass


class QueueSystem:
    def __init__(self) -> None:
        self._queue: Deque[Mahasiswa] = deque()
        self._next_nomor_antrian: int = 1
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

    def enqueue(self, mahasiswa: Mahasiswa) -> None:
        start_time = time.perf_counter_ns()
        try:
            mahasiswa.no_antrian = self._next_nomor_antrian
            self._next_nomor_antrian += 1
            self._queue.append(mahasiswa)
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def dequeue(self) -> Mahasiswa:
        start_time = time.perf_counter_ns()
        try:
            if self.is_empty():
                raise QueueEmptyError("Antrean kosong! Tidak ada mahasiswa yang dapat dilayani.")
            return self._queue.popleft()
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def peek(self) -> Mahasiswa:
        start_time = time.perf_counter_ns()
        try:
            if self.is_empty():
                raise QueueEmptyError("Antrean kosong! Tidak ada mahasiswa di urutan terdepan.")
            return self._queue[0]
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        start_time = time.perf_counter_ns()
        try:
            return len(self._queue)
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def display(self) -> List[str]:
        start_time = time.perf_counter_ns()
        try:
            return [str(mhs) for mhs in self._queue]
        finally:
            self._last_execution_time_ns = time.perf_counter_ns() - start_time

    def get_all(self) -> List[Mahasiswa]:
        return list(self._queue)

    def clear(self) -> None:
        self._queue.clear()
        self._next_nomor_antrian = 1
