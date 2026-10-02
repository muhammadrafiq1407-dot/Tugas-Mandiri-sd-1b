from datetime import datetime
import unittest

from src.models.petugas import AktivitasPetugas
from src.struktur_data.stack_system import StackSystem, StackEmptyError


class TestStackSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.stack = StackSystem(max_capacity=10)

    def _buat_aktivitas(self, nama: str, aksi: str) -> AktivitasPetugas:
        return AktivitasPetugas(
            id_petugas="PTG01",
            nama=nama,
            aktivitas=aksi,
            waktu=datetime.now()
        )

    def test_01_stack_baru_harus_kosong(self) -> None:
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(len(self.stack.display()), 0)

    def test_02_push_satu_aktivitas(self) -> None:
        act = self._buat_aktivitas("Rina", "Verifikasi berkas mahasiswa")
        evicted = self.stack.push(act)

        self.assertFalse(evicted)
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek().aktivitas, "Verifikasi berkas mahasiswa")

    def test_03_push_beberapa_aktivitas(self) -> None:
        self.stack.push(self._buat_aktivitas("Rina", "Aksi 1"))
        self.stack.push(self._buat_aktivitas("Rina", "Aksi 2"))
        self.stack.push(self._buat_aktivitas("Rina", "Aksi 3"))

        self.assertEqual(self.stack.size(), 3)
        self.assertEqual(self.stack.peek().aktivitas, "Aksi 3")

    def test_04_pop_mengambil_aktivitas_terakhir_lifo(self) -> None:
        self.stack.push(self._buat_aktivitas("Bambang", "Aksi A"))
        self.stack.push(self._buat_aktivitas("Bambang", "Aksi B"))

        undone = self.stack.pop()
        self.assertEqual(undone.aktivitas, "Aksi B")
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek().aktivitas, "Aksi A")

    def test_05_urutan_lifo_konsisten_pada_banyak_operasi(self) -> None:
        aksi_list = ["Input KRS", "Cetak Transkrip", "Update No HP", "Setuju Cuti"]
        for aksi in aksi_list:
            self.stack.push(self._buat_aktivitas("Hendra", aksi))

        # Pop harus mengembalikan urutan terbalik (LIFO)
        self.assertEqual(self.stack.pop().aktivitas, "Setuju Cuti")
        self.assertEqual(self.stack.pop().aktivitas, "Update No HP")
        self.assertEqual(self.stack.pop().aktivitas, "Cetak Transkrip")
        self.assertEqual(self.stack.pop().aktivitas, "Input KRS")
        self.assertTrue(self.stack.is_empty())

    def test_06_peek_tidak_menghapus_data(self) -> None:
        self.stack.push(self._buat_aktivitas("Rina", "Validasi Ijazah"))

        peek1 = self.stack.peek()
        self.assertEqual(peek1.aktivitas, "Validasi Ijazah")
        self.assertEqual(self.stack.size(), 1)

        peek2 = self.stack.peek()
        self.assertEqual(peek2.aktivitas, "Validasi Ijazah")
        self.assertEqual(self.stack.size(), 1)

    def test_07_size_sesuai_dengan_jumlah_elemen(self) -> None:
        self.assertEqual(self.stack.size(), 0)
        self.stack.push(self._buat_aktivitas("Rina", "Aksi 1"))
        self.assertEqual(self.stack.size(), 1)
        self.stack.push(self._buat_aktivitas("Rina", "Aksi 2"))
        self.assertEqual(self.stack.size(), 2)
        self.stack.pop()
        self.assertEqual(self.stack.size(), 1)
        self.stack.pop()
        self.assertEqual(self.stack.size(), 0)

    def test_08_pop_pada_stack_kosong_melempar_exception(self) -> None:
        with self.assertRaises(StackEmptyError):
            self.stack.pop()

    def test_09_peek_pada_stack_kosong_melempar_exception(self) -> None:
        with self.assertRaises(StackEmptyError):
            self.stack.peek()

    def test_10_display_menampilkan_urutan_terbaru_ke_terlama(self) -> None:
        self.stack.push(self._buat_aktivitas("Petugas", "Pertama"))
        self.stack.push(self._buat_aktivitas("Petugas", "Kedua"))
        self.stack.push(self._buat_aktivitas("Petugas", "Ketiga (Puncak)"))

        tampilan = self.stack.display()
        self.assertEqual(len(tampilan), 3)
        # Indeks 0 pada display harus elemen paling atas / terbaru
        self.assertIn("Ketiga (Puncak)", tampilan[0])
        self.assertIn("Kedua", tampilan[1])
        self.assertIn("Pertama", tampilan[2])
        # Pastikan tidak ada perubahan status stack
        self.assertEqual(self.stack.size(), 3)

    def test_11_batas_maksimal_10_undo(self) -> None:
        for i in range(1, 13):  # Push 12 elemen berturut-turut
            evicted = self.stack.push(self._buat_aktivitas("Petugas", f"Aksi Ke-{i}"))
            if i > 10:
                self.assertTrue(evicted, f"Elemen ke-{i} harus memicu eviction elemen terlama.")
            else:
                self.assertFalse(evicted)

        # Ukuran stack harus tetap maksimal 10
        self.assertEqual(self.stack.size(), 10)

        # Elemen terlama (Aksi Ke-1 dan Aksi Ke-2) harus sudah terbuang
        semua_aksi = [act.aktivitas for act in self.stack.get_all()]
        self.assertNotIn("Aksi Ke-1", semua_aksi)
        self.assertNotIn("Aksi Ke-2", semua_aksi)
        self.assertIn("Aksi Ke-3", semua_aksi)
        self.assertIn("Aksi Ke-12", semua_aksi)

        # Pop harus mengambil Aksi Ke-12 terlebih dahulu
        self.assertEqual(self.stack.pop().aktivitas, "Aksi Ke-12")

    def test_12_validasi_model_petugas(self) -> None:
        with self.assertRaises(ValueError):
            AktivitasPetugas("", "Petugas A", "Aksi")
        with self.assertRaises(ValueError):
            AktivitasPetugas("PTG01", "", "Aksi")
        with self.assertRaises(ValueError):
            AktivitasPetugas("PTG01", "Petugas A", "")

    def test_13_pencatatan_kecepatan_waktu_eksekusi(self) -> None:
        act = self._buat_aktivitas("Petugas", "Aksi Bench")
        self.stack.push(act)
        self.assertGreaterEqual(self.stack.last_execution_time_ns, 0)
        self.stack.pop()
        self.assertGreaterEqual(self.stack.last_execution_time_ns, 0)


if __name__ == "__main__":
    unittest.main()
