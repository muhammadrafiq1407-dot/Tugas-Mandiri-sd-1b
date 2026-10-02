from datetime import datetime
import unittest

from src.models.mahasiswa import Mahasiswa
from src.struktur_data.queue_system import QueueSystem, QueueEmptyError


class TestQueueSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.queue = QueueSystem()

    def test_01_antrean_baru_harus_kosong(self) -> None:
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)
        self.assertEqual(len(self.queue.display()), 0)

    def test_02_enqueue_satu_mahasiswa(self) -> None:
        mhs = Mahasiswa(nama="Ahmad Dahlan", nim="12550111001", no_antrian=0, keperluan="KRS")
        self.queue.enqueue(mhs)

        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.peek().nama, "Ahmad Dahlan")
        self.assertEqual(mhs.no_antrian, 1)

    def test_03_enqueue_beberapa_mahasiswa(self) -> None:
        m1 = Mahasiswa("Ahmad", "12550111001", 0, "KRS")
        m2 = Mahasiswa("Budi", "12550111002", 0, "KHS")
        m3 = Mahasiswa("Citra", "12550111003", 0, "Ijazah")

        self.queue.enqueue(m1)
        self.queue.enqueue(m2)
        self.queue.enqueue(m3)

        self.assertEqual(self.queue.size(), 3)
        self.assertEqual(m1.no_antrian, 1)
        self.assertEqual(m2.no_antrian, 2)
        self.assertEqual(m3.no_antrian, 3)

    def test_04_dequeue_mengambil_mahasiswa_paling_awal_fifo(self) -> None:
        m1 = Mahasiswa("Ahmad", "12550111001", 0, "KRS")
        m2 = Mahasiswa("Budi", "12550111002", 0, "KHS")
        self.queue.enqueue(m1)
        self.queue.enqueue(m2)

        dilayani = self.queue.dequeue()
        self.assertEqual(dilayani.nama, "Ahmad")
        self.assertEqual(dilayani.nim, "12550111001")
        self.assertEqual(self.queue.size(), 1)

    def test_05_urutan_fifo_konsisten_pada_banyak_operasi(self) -> None:
        daftar_nama = ["Dewi", "Eko", "Farhan", "Gita", "Hadi"]
        for idx, nama in enumerate(daftar_nama, start=1):
            self.queue.enqueue(Mahasiswa(nama, f"1255011100{idx}", 0, "Layanan"))

        # Verifikasi urutan keluaran harus persis sama dengan urutan masuk
        for expected_nama in daftar_nama:
            dilayani = self.queue.dequeue()
            self.assertEqual(dilayani.nama, expected_nama)

        self.assertTrue(self.queue.is_empty())

    def test_06_peek_tidak_menghapus_data(self) -> None:
        mhs = Mahasiswa("Indah", "12550111010", 0, "Cuti")
        self.queue.enqueue(mhs)

        peek1 = self.queue.peek()
        self.assertEqual(peek1.nama, "Indah")
        self.assertEqual(self.queue.size(), 1)

        peek2 = self.queue.peek()
        self.assertEqual(peek2.nama, "Indah")
        self.assertEqual(self.queue.size(), 1)

    def test_07_size_sesuai_dengan_jumlah_elemen(self) -> None:
        self.assertEqual(self.queue.size(), 0)
        self.queue.enqueue(Mahasiswa("Joko", "12550111020", 0, "Ujian"))
        self.assertEqual(self.queue.size(), 1)
        self.queue.enqueue(Mahasiswa("Kartika", "12550111021", 0, "Beasiswa"))
        self.assertEqual(self.queue.size(), 2)
        self.queue.dequeue()
        self.assertEqual(self.queue.size(), 1)
        self.queue.dequeue()
        self.assertEqual(self.queue.size(), 0)

    def test_08_dequeue_pada_antrean_kosong_melempar_exception(self) -> None:
        with self.assertRaises(QueueEmptyError):
            self.queue.dequeue()

    def test_09_peek_pada_antrean_kosong_melempar_exception(self) -> None:
        with self.assertRaises(QueueEmptyError):
            self.queue.peek()

    def test_10_display_tidak_mengubah_isi_antrean(self) -> None:
        m1 = Mahasiswa("Lukman", "12550111030", 0, "Transkrip")
        m2 = Mahasiswa("Maya", "12550111031", 0, "Magang")
        self.queue.enqueue(m1)
        self.queue.enqueue(m2)

        tampilan = self.queue.display()
        self.assertEqual(len(tampilan), 2)
        self.assertIn("Lukman", tampilan[0])
        self.assertIn("Maya", tampilan[1])
        # Pastikan ukuran dan posisi tidak berubah
        self.assertEqual(self.queue.size(), 2)
        self.assertEqual(self.queue.peek().nama, "Lukman")

    def test_11_validasi_model_mahasiswa(self) -> None:
        with self.assertRaises(ValueError):
            Mahasiswa("", "123", 0, "KRS")
        with self.assertRaises(ValueError):
            Mahasiswa("Budi", "", 0, "KRS")
        with self.assertRaises(ValueError):
            Mahasiswa("Budi", "123", 0, "")

    def test_12_pencatatan_kecepatan_waktu_eksekusi(self) -> None:
        m = Mahasiswa("Nanda", "12550111040", 0, "Skripsi")
        self.queue.enqueue(m)
        self.assertGreaterEqual(self.queue.last_execution_time_ns, 0)
        self.queue.dequeue()
        self.assertGreaterEqual(self.queue.last_execution_time_ns, 0)


if __name__ == "__main__":
    unittest.main()
