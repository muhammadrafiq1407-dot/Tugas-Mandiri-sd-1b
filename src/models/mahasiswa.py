from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Mahasiswa:
    nama: str
    nim: str
    no_antrian: int
    keperluan: str
    waktu_daftar: datetime = None

    def __post_init__(self) -> None:
        if not self.nama or not self.nama.strip():
            raise ValueError("Nama mahasiswa tidak boleh kosong.")
        if not self.nim or not self.nim.strip():
            raise ValueError("NIM mahasiswa tidak boleh kosong.")
        if not self.keperluan or not self.keperluan.strip():
            raise ValueError("Keperluan layanan tidak boleh kosong.")
        if self.waktu_daftar is None:
            self.waktu_daftar = datetime.now()

    def __str__(self) -> str:
        waktu_str = self.waktu_daftar.strftime("%H:%M:%S")
        return (
            f"[No. {self.no_antrian:03d}] {self.nama:<20} | NIM: {self.nim:<12} | "
            f"Keperluan: {self.keperluan:<25} | Waktu: {waktu_str}"
        )

    def to_dict(self) -> dict[str, str | int]:
        return {
            "no_antrian": self.no_antrian,
            "nama": self.nama,
            "nim": self.nim,
            "keperluan": self.keperluan,
            "waktu_daftar": self.waktu_daftar.strftime("%Y-%m-%d %H:%M:%S"),
        }
