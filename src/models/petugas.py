# src/models/petugas.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class AktivitasPetugas:
    id_petugas: str
    nama: str
    aktivitas: str
    waktu: datetime = None
    id_aktivitas: str = None

    def __post_init__(self) -> None:
        if not self.id_petugas or not self.id_petugas.strip():
            raise ValueError("ID Petugas tidak boleh kosong.")
        if not self.nama or not self.nama.strip():
            raise ValueError("Nama Petugas tidak boleh kosong.")
        if not self.aktivitas or not self.aktivitas.strip():
            raise ValueError("Deskripsi aktivitas tidak boleh kosong.")
        if self.waktu is None:
            self.waktu = datetime.now()
        if self.id_aktivitas is None:
            self.id_aktivitas = f"ACT-{uuid.uuid4().hex[:6].upper()}"

    def __str__(self) -> str:
        waktu_str = self.waktu.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"[{self.id_aktivitas}] Petugas: {self.nama} ({self.id_petugas}) | "
            f"Aktivitas: {self.aktivitas} | Waktu: {waktu_str}"
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "id_aktivitas": self.id_aktivitas,
            "id_petugas": self.id_petugas,
            "nama": self.nama,
            "aktivitas": self.aktivitas,
            "waktu": self.waktu.strftime("%Y-%m-%d %H:%M:%S"),
        }
