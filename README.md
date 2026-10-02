# SISTEM LAYANAN ADMINISTRASI MAHASISWA & UNDO AKTIVITAS PETUGAS
### Implementasi Struktur Data Linear: Queue & Stack Menggunakan Python

---

## 📌 IDENTITAS AKADEMIK
* **Nama Mahasiswa** : Muhammad Rafiq Al-ghifari
* **NIM**            : 12550111036
* **Program Studi**  : Teknik Informatika
* **Perguruan Tinggi**: UIN Sultan Syarif Kasim Riau
* **Mata Kuliah**    : Struktur Data
* **Tugas**          : Tugas Mandiri 1b (Queue & Stack)
* **Bahasa**         : Python 3.8+

---

## 1. DESKRIPSI & LATAR BELAKANG STUDI KASUS

Dalam operasional pelayanan administrasi kampus, terdapat dua kebutuhan komputasi linear yang fundamental:

1. **Sistem Antrean Mahasiswa (FIFO - First-In, First-Out):** Mahasiswa yang datang terlebih dahulu harus mendapatkan pelayanan administrasi lebih awal dibandingkan mahasiswa yang datang kemudian. Pola antrean ini dimodelkan menggunakan struktur data **Queue**.
2. **Sistem Undo Log Aktivitas Petugas (LIFO - Last-In, First-Out):** Ketika petugas administrasi melakukan kesalahan input atau ingin membatalkan aksi operasional terbaru, sistem harus membatalkan aksi paling akhir terlebih dahulu. Pola ini dimodelkan menggunakan struktur data **Stack** dengan batasan riwayat undo maksimal **10 aktivitas**.

Aplikasi ini dibangun berbasis **Command Line Interface (CLI)** dengan arsitektur modular, *Clean Code*, *Separation of Concerns* (SoC), *Object-Oriented Programming* (OOP), penanganan error komprehensif, serta dilengkapi fitur **Pencatatan Timestamp (`datetime`) & Benchmark Waktu Eksekusi Algoritma Real-time (`perf_counter_ns`)**.

---

## 2. PRINSIP STRUKTUR DATA & ALASAN PEMILIHAN

### A. Queue (Sistem Antrean Mahasiswa)
* **Prinsip**: First-In, First-Out (FIFO).
* **Implementasi**: `collections.deque` (Double-Ended Queue).
* **Operasi Utama**:
  * `enqueue(mahasiswa)`: Menambahkan mahasiswa ke belakang antrean (`deque.append()`) dalam waktu **O(1)**.
  * `dequeue()`: Mengambil & menghapus mahasiswa terdepan (`deque.popleft()`) dalam waktu **O(1)**.
  * `peek()`: Mengakses elemen pertama tanpa menghapus (`deque[0]`) dalam waktu **O(1)**.
* **Alasan Pemilihan `deque`**:
  Berbeda dengan Python `list` di mana operasi `pop(0)` membutuhkan pergeseran memori untuk seluruh elemen sebesar **O(n)**, `collections.deque` diimplementasikan sebagai *doubly linked list of blocks* dalam bahasa C. Hal ini menjamin penambahan dan pengurangan elemen di kedua ujung beroperasi konsisten pada **O(1)**.

### B. Stack (Sistem Undo Aktivitas Petugas)
* **Prinsip**: Last-In, First-Out (LIFO).
* **Implementasi**: Python `list`.
* **Kapasitas Undo**: Dibatasi maksimal **10 aktivitas**.
* **Operasi Utama**:
  * `push(aktivitas)`: Menambahkan aksi ke puncak stack (`list.append()`) dalam waktu **amortized O(1)**.
  * `pop()`: Mengambil & membatalkan aksi terakhir (`list.pop()`) dalam waktu **O(1)**.
  * `peek()`: Melihat aksi di puncak stack (`list[-1]`) dalam waktu **O(1)**.
* **Alasan Pemilihan `list`**:
  Operasi pada akhir array dinamis Python (`append` dan `pop()`) tidak memerlukan pergeseran elemen sehingga sangat efisien dengan kompleksitas **O(1)**. Kebijakan batas 10 undo menjaga penggunaan memori tetap minimal dan relevan.

---

## 3. ARSITEKTUR & STRUKTUR DIREKTORI

Struktur direktori proyek dirancang secara modular:

```text
tugas-mandiri-1b/
│
├── src/
│   ├── __init__.py            # Inisialisasi package & ekspor modul
│   │
│   ├── models/                # Domain models (Entitas Data)
│   │   ├── __init__.py
│   │   ├── mahasiswa.py       # Class Mahasiswa (nama, nim, no_antrian, keperluan, datetime)
│   │   └── petugas.py         # Class AktivitasPetugas (id, nama, aktivitas, timestamp)
│   │
│   ├── queue_system.py        # Logika Queue (FIFO) berbasis collections.deque + Benchmark
│   ├── stack_system.py        # Logika Stack (LIFO) berbasis list + Max 10 Undo + Benchmark
│   └── main.py                # CLI Interface & Orchestrator Menu Interaktif
│
├── tests/                     # Pengujian otomatis (Unit Testing)
│   ├── __init__.py
│   ├── test_queue.py          # 12 Unit test untuk QueueSystem
│   └── test_stack.py          # 13 Unit test untuk StackSystem & Limit 10
│
├── docs/
│   └── screenshots/           # Dokumentasi hasil tangkapan layar pengujian
│
├── .gitignore                 # Filter file cache & lingkungan virtual
├── README.md                  # Dokumentasi teknis & laporan akademik
└── requirements.txt           # Spesifikasi dependensi (Zero external dependencies)
```

---

## 4. ANALISIS KOMPLEKSITAS ALGORITMA (TIME & SPACE COMPLEXITY)

| Struktur Data | Operasi | Kompleksitas Waktu | Kompleksitas Ruang | Penjelasan Algoritmik |
| :--- | :--- | :--- | :--- | :--- |
| **Queue** | `enqueue()` | **O(1)** | O(1) | Menambahkan elemen ke bagian belakang `deque` tanpa relokasi elemen lain. |
| **Queue** | `dequeue()` | **O(1)** | O(1) | Mengambil & menghapus pointer kepala (`popleft`) langsung dalam waktu konstan. |
| **Queue** | `peek()` | **O(1)** | O(1) | Mengakses indeks pertama `deque[0]` secara langsung. |
| **Queue** | `is_empty()` | **O(1)** | O(1) | Memeriksa panjang struktur internal `len(_queue) == 0`. |
| **Queue** | `size()` | **O(1)** | O(1) | Mengambil nilai atribut ukuran internal `deque`. |
| **Queue** | `display()` | **O(n)** | O(n) | Melakukan traversal dari awal ke akhir untuk menampilkan seluruh $n$ antrean. |
| **Stack** | `push()` | **O(1) amortized** | O(1) | Menambahkan elemen di akhir list; membuang elemen tertua jika $>10$. |
| **Stack** | `pop()` | **O(1)** | O(1) | Mengambil & menghapus elemen di akhir list tanpa pergeseran elemen lain. |
| **Stack** | `peek()` | **O(1)** | O(1) | Mengakses elemen di indeks puncak `_stack[-1]`. |
| **Stack** | `is_empty()` | **O(1)** | O(1) | Memeriksa `len(_stack) == 0`. |
| **Stack** | `size()` | **O(1)** | O(1) | Mengambil jumlah aktivitas tersimpan ($0 \le n \le 10$). |
| **Stack** | `display()` | **O(n)** | O(n) | Menelusuri seluruh elemen secara terbalik dari puncak ke dasar stack ($n \le 10$). |

---

## 5. PANDUAN INSTALASI & CARA MENJALANKAN

### Persyaratan Lingkungan
* Python versi **3.8** atau lebih tinggi.
* Sistem Operasi: Windows 10/11, macOS, atau Linux.
* Terminal: PowerShell / Command Prompt / VS Code Terminal.

### Langkah Menjalankan Aplikasi
1. Buka terminal pada folder direktori root tugas:
   ```powershell
   cd "e:\Matkul\Struktur Data\Tugas\Tugas Mandiri-1b"
   ```
2. Jalankan aplikasi utama melalui perintah modul Python:
   ```powershell
   python -m src.main
   ```
   *(Atau secara langsung melalui: `python src/main.py`)*

---

## 6. PENGUJIAN OTOMATIS (UNIT TESTING)

Pengujian dilakukan menggunakan framework standar `unittest` untuk memvalidasi algoritma, batasan kapasitas, serta penanganan error.

### Perintah Menjalankan Test
Jalankan perintah berikut dari direktori root proyek:
```powershell
python -m unittest discover -s tests -v
```

### Hasil Pengujian Aktual (25 Test Case Lolos 100%)
```text
test_01_antrean_baru_harus_kosong (test_queue.TestQueueSystem) ... ok
test_02_enqueue_satu_mahasiswa (test_queue.TestQueueSystem) ... ok
test_03_enqueue_beberapa_mahasiswa (test_queue.TestQueueSystem) ... ok
test_04_dequeue_mengambil_mahasiswa_paling_awal_fifo (test_queue.TestQueueSystem) ... ok
test_05_urutan_fifo_konsisten_pada_banyak_operasi (test_queue.TestQueueSystem) ... ok
test_06_peek_tidak_menghapus_data (test_queue.TestQueueSystem) ... ok
test_07_size_sesuai_dengan_jumlah_elemen (test_queue.TestQueueSystem) ... ok
test_08_dequeue_pada_antrean_kosong_melempar_exception (test_queue.TestQueueSystem) ... ok
test_09_peek_pada_antrean_kosong_melempar_exception (test_queue.TestQueueSystem) ... ok
test_10_display_tidak_mengubah_isi_antrean (test_queue.TestQueueSystem) ... ok
test_11_validasi_model_mahasiswa (test_queue.TestQueueSystem) ... ok
test_12_pencatatan_kecepatan_waktu_eksekusi (test_queue.TestQueueSystem) ... ok
test_01_stack_baru_harus_kosong (test_stack.TestStackSystem) ... ok
test_02_push_satu_aktivitas (test_stack.TestStackSystem) ... ok
test_03_push_beberapa_aktivitas (test_stack.TestStackSystem) ... ok
test_04_pop_mengambil_aktivitas_terakhir_lifo (test_stack.TestStackSystem) ... ok
test_05_urutan_lifo_konsisten_pada_banyak_operasi (test_stack.TestStackSystem) ... ok
test_06_peek_tidak_menghapus_data (test_stack.TestStackSystem) ... ok
test_07_size_sesuai_dengan_jumlah_elemen (test_stack.TestStackSystem) ... ok
test_08_pop_pada_stack_kosong_melempar_exception (test_stack.TestStackSystem) ... ok
test_09_peek_pada_stack_kosong_melempar_exception (test_stack.TestStackSystem) ... ok
test_10_display_menampilkan_urutan_terbaru_ke_terlama (test_stack.TestStackSystem) ... ok
test_11_batas_maksimal_10_undo (test_stack.TestStackSystem) ... ok
test_12_validasi_model_petugas (test_stack.TestStackSystem) ... ok
test_13_pencatatan_kecepatan_waktu_eksekusi (test_stack.TestStackSystem) ... ok

----------------------------------------------------------------------
Ran 25 tests in 0.001s

OK
```

---

## 7. SIMULASI ALGORITMA DAN LOG BENCHMARK

Setiap interaksi pada menu CLI secara langsung mencatat timestamp tanggal dan waktu (`datetime`) serta menghitung waktu eksekusi presisi dalam satuan nanodetik / mikrodetik:

### Contoh Output Eksekusi Queue (FIFO)
```text
✅ Mahasiswa berhasil masuk antrean:
   👉 [No. 001] Ahmad Dahlan         | NIM: 12550111001  | Keperluan: Legalitas Ijazah          | Waktu: 19:45:10
--------------------------------------------------------------------------------
⏱️  [LOG EKSEKUSI & BENCHMARK ALGORITMA]
   • Waktu Pencatatan : 2026-10-02 19:45:10.124
   • Operasi          : Queue.enqueue()
   • Kompleksitas     : O(1) - deque.append()
   • Durasi Eksekusi  : 2.10 µs (Mikrodetik)
--------------------------------------------------------------------------------
```

### Contoh Output Eksekusi Stack (LIFO & Batas 10)
```text
↩️  [BERHASIL DI-UNDO (DIBATALKAN)]
   ID Aksi    : ACT-B81E2F
   Petugas    : Rina Marlina (PTG01)
   Aksi Batal : Mengarsipkan berkas yudisium
   Waktu Awal : 2026-10-02 19:40:00
--------------------------------------------------------------------------------
⏱️  [LOG EKSEKUSI & BENCHMARK ALGORITMA]
   • Waktu Pencatatan : 2026-10-02 19:46:02.891
   • Operasi          : Stack.pop()
   • Kompleksitas     : O(1) - list.pop() di akhir
   • Durasi Eksekusi  : 1.40 µs (Mikrodetik)
--------------------------------------------------------------------------------
```

---

## 8. CHECKLIST KESIAPAN PENGUMPULAN

- [x] Seluruh file implementasi tersedia dan modular (`src/models/`, `src/queue_system.py`, `src/stack_system.py`, `src/main.py`).
- [x] Program utama CLI dapat dijalankan lancar tanpa error pada skenario normal maupun kondisi batas.
- [x] Operasi Queue terbukti berjalan sesuai prinsip FIFO dengan kompleksitas O(1).
- [x] Operasi Stack terbukti berjalan sesuai prinsip LIFO dengan kompleksitas O(1).
- [x] Batasan 10 riwayat undo terbukti aktif dan teruji membuang aksi terlama saat kapasitas penuh.
- [x] Seluruh 25 unit test `unittest` lulus 100% (OK).
- [x] Analisis kompleksitas waktu dan ruang disajikan lengkap.
- [x] Fitur benchmarking waktu eksekusi dan pencatatan timestamp (`datetime`) terintegrasi.
- [x] Dokumentasi `README.md`, `.gitignore`, dan `requirements.txt` lengkap dan rapi.

---

## 9. KESIMPULAN

Struktur data linear memiliki karakteristik spesifik yang menentukan performa dan kesesuaian kasus penggunaan:
1. **Queue (`collections.deque`)** merupakan pilihan optimal untuk sistem layanan antrean publik dengan sifat *First-In, First-Out* karena mampu mengeksekusi operasi `enqueue` dan `dequeue` dalam waktu konstan $O(1)$.
2. **Stack (`list`)** merupakan solusi ideal untuk mekanisme *Undo/Redo* berbasis *Last-In, First-Out* karena operasi pada ujung list beroperasi dalam waktu konstan $O(1)$ amortized, dengan manajemen memori terkendali melalui pembatasan riwayat sebanyak 10 aksi.
