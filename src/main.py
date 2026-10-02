from __future__ import annotations
from datetime import datetime
import os
import sys
import time
from typing import Optional

try:
    from .models.mahasiswa import Mahasiswa
    from .models.petugas import AktivitasPetugas
    from .struktur_data.queue_system import QueueSystem, QueueEmptyError
    from .struktur_data.stack_system import StackSystem, StackEmptyError
except ImportError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from src.models.mahasiswa import Mahasiswa
    from src.models.petugas import AktivitasPetugas
    from src.struktur_data.queue_system import QueueSystem, QueueEmptyError
    from src.struktur_data.stack_system import StackSystem, StackEmptyError


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    print("=" * 80)
    print("   SISTEM LAYANAN ADMINISTRASI MAHASISWA & MANAJEMEN LOG AKTIVITAS PETUGAS   ")
    print("           Tugas Mandiri 1b - Struktur Data Linear (Queue & Stack)          ")
    print("=" * 80)
    print("  Nama  : Muhammad Rafiq Al-ghifari     NIM   : 12550111036                  ")
    print("  Prodi : Teknik Informatika             Kampus: UIN Sultan Syarif Kasim Riau")
    print("=" * 80)


def format_duration(ns: int) -> str:
    if ns < 1_000:
        return f"{ns} ns (Nanodetik)"
    elif ns < 1_000_000:
        return f"{ns / 1_000:.2f} µs (Mikrodetik)"
    else:
        return f"{ns / 1_000_000:.4f} ms (Milidetik)"


def print_perf_badge(action_name: str, duration_ns: int, complexity: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print("-" * 80)
    print(f"⏱️  [LOG EKSEKUSI & BENCHMARK ALGORITMA]")
    print(f"   • Waktu Pencatatan : {timestamp}")
    print(f"   • Operasi          : {action_name}")
    print(f"   • Kompleksitas     : {complexity}")
    print(f"   • Durasi Eksekusi  : {format_duration(duration_ns)}")
    print("-" * 80)


def pause() -> None:
    input("\n[Tekan ENTER untuk melanjutkan...]")


def get_nonempty_input(prompt: str) -> str:
    while True:
        try:
            value = input(prompt).strip()
            if value:
                return value
            print("⚠️  Input tidak boleh kosong. Silakan masukkan kembali.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperasi dibatalkan.")
            return ""


def submenu_queue(queue: QueueSystem, stack: StackSystem) -> None:
    while True:
        clear_screen()
        print_banner()
        print("\n📂 [MENU UTAMA > 1. SISTEM ANTREAN MAHASISWA (QUEUE - FIFO)]")
        print(f"   Kapasitas Terisi : {queue.size()} Mahasiswa dalam antrean\n")
        print("   [1] Tambah Mahasiswa ke Antrean (Enqueue - O(1))")
        print("   [2] Layani Mahasiswa Terdepan  (Dequeue - O(1))")
        print("   [3] Lihat Mahasiswa Berikutnya (Peek - O(1))")
        print("   [4] Tampilkan Seluruh Antrean  (Display - O(n))")
        print("   [5] Cek Status & Jumlah Antrean (Size & IsEmpty - O(1))")
        print("   [6] Isi Data Contoh Otomatis (Demo FIFO Batch)")
        print("   [0] Kembali ke Menu Utama")
        print("-" * 80)

        pilihan = input("Masukkan pilihan [0-6]: ").strip()

        if pilihan == "1":
            print("\n--- TAMBAH MAHASISWA KE ANTREAN (ENQUEUE) ---")
            nama = get_nonempty_input("Nama Lengkap Mahasiswa : ")
            if not nama:
                continue
            nim = get_nonempty_input("NIM Mahasiswa          : ")
            if not nim:
                continue
            keperluan = get_nonempty_input("Keperluan Administrasi : ")
            if not keperluan:
                continue

            try:
                mhs = Mahasiswa(nama=nama, nim=nim, no_antrian=0, keperluan=keperluan)
                queue.enqueue(mhs)
                print(f"\n✅ Mahasiswa berhasil masuk antrean:")
                print(f"   👉 {mhs}")
                print_perf_badge("Queue.enqueue()", queue.last_execution_time_ns, "O(1) - deque.append()")

                act = AktivitasPetugas(
                    id_petugas="SYSTEM",
                    nama="Sistem Antrean",
                    aktivitas=f"Mendaftarkan antrean No.{mhs.no_antrian:03d} ({mhs.nama} - {mhs.keperluan})"
                )
                stack.push(act)
            except Exception as err:
                print(f"\n❌ Gagal menambahkan mahasiswa: {err}")
            pause()

        elif pilihan == "2":
            print("\n--- LAYANI MAHASISWA (DEQUEUE) ---")
            try:
                mhs = queue.dequeue()
                print(f"\n🔔 [PANGGILAN LAYANAN]")
                print(f"   Sedang Melayani: {mhs.nama} (No. Antrean: {mhs.no_antrian:03d})")
                print(f"   NIM            : {mhs.nim}")
                print(f"   Keperluan      : {mhs.keperluan}")
                print(f"   Waktu Datang   : {mhs.waktu_daftar.strftime('%H:%M:%S')}")
                print_perf_badge("Queue.dequeue()", queue.last_execution_time_ns, "O(1) - deque.popleft()")

                # Catat ke stack untuk riwayat
                act = AktivitasPetugas(
                    id_petugas="CS-01",
                    nama="Petugas Layanan",
                    aktivitas=f"Melayani antrean No.{mhs.no_antrian:03d} ({mhs.nama} - {mhs.keperluan})"
                )
                stack.push(act)
            except QueueEmptyError as err:
                print(f"\n⚠️  {err}")
                print_perf_badge("Queue.dequeue() [Empty Check]", queue.last_execution_time_ns, "O(1)")
            pause()

        elif pilihan == "3":
            print("\n--- LIHAT MAHASISWA BERIKUTNYA (PEEK) ---")
            try:
                mhs = queue.peek()
                print(f"\n👀 Mahasiswa di urutan paling depan:")
                print(f"   👉 {mhs}")
                print_perf_badge("Queue.peek()", queue.last_execution_time_ns, "O(1) - deque[0]")
            except QueueEmptyError as err:
                print(f"\n⚠️  {err}")
                print_perf_badge("Queue.peek() [Empty Check]", queue.last_execution_time_ns, "O(1)")
            pause()

        elif pilihan == "4":
            print("\n--- SELURUH MAHASISWA DALAM ANTREAN (FIFO DISPLAY) ---")
            antrean_list = queue.display()
            if not antrean_list:
                print("\nℹ️  Antrean saat ini KOSONG. Belum ada mahasiswa yang menunggu.")
            else:
                print(f"\nTotal Mahasiswa Menunggu: {len(antrean_list)}\n")
                print(f"{'Posisi':<8} | {'Detail Mahasiswa'}")
                print("-" * 80)
                for idx, item_str in enumerate(antrean_list, start=1):
                    prefix = "👉 [DEPAN]" if idx == 1 else f"   [{idx}]   "
                    print(f"{prefix} | {item_str}")
            print_perf_badge("Queue.display()", queue.last_execution_time_ns, "O(n) - Iterasi n elemen")
            pause()

        elif pilihan == "5":
            print("\n--- STATUS DAN JUMLAH ANTREAN ---")
            size = queue.size()
            is_empty = queue.is_empty()
            print(f"   • Status Antrean : {'KOSONG' if is_empty else 'TERISI'}")
            print(f"   • Jumlah Antrean : {size} Mahasiswa")
            print_perf_badge("Queue.size() & is_empty()", queue.last_execution_time_ns, "O(1)")
            pause()

        elif pilihan == "6":
            print("\n--- MEMUAT DATA CONTOH (BATCH DEMO) ---")
            contoh_data = [
                ("Ahmad Dahlan", "12550111001", "Legalitas Ijazah"),
                ("Siti Aisyah", "12550111002", "Pengajuan Beasiswa"),
                ("Budi Pratama", "12550111003", "Konsultasi KRS"),
                ("Nurul Hidayah", "12550111004", "Surat Keterangan Aktif"),
                ("Fajar Ramadhan", "12550111005", "Pengambilan KTM"),
            ]
            for nama, nim, kep in contoh_data:
                m = Mahasiswa(nama=nama, nim=nim, no_antrian=0, keperluan=kep)
                queue.enqueue(m)
                print(f"   ➕ Masuk: {m}")
            print("\n✅ Berhasil menambahkan 5 mahasiswa contoh ke dalam antrean.")
            print_perf_badge("Queue.enqueue() [Batch 5x]", queue.last_execution_time_ns, "O(1) per operasi")
            pause()

        elif pilihan == "0":
            break
        else:
            print("\n⚠️  Pilihan tidak valid! Silakan masukkan angka sesuai menu.")
            pause()


def submenu_stack(stack: StackSystem) -> None:
    while True:
        clear_screen()
        print_banner()
        print("\n📂 [MENU UTAMA > 2. SISTEM UNDO AKTIVITAS PETUGAS (STACK - LIFO)]")
        print(f"   Riwayat Tersimpan : {stack.size()}/{stack.MAX_CAPACITY} Aktivitas (Maksimal 10 Undo)\n")
        print("   [1] Catat Aktivitas Baru      (Push - O(1))")
        print("   [2] Batalkan Aktivitas Terakhir (Undo / Pop - O(1))")
        print("   [3] Lihat Aktivitas Terakhir  (Peek - O(1))")
        print("   [4] Tampilkan Riwayat Undo    (Display Terbaru -> Terlama - O(n))")
        print("   [5] Cek Status & Ukuran Stack (Size & IsEmpty - O(1))")
        print("   [6] Isi Data Contoh Aktivitas (Demo Batas 10 Undo)")
        print("   [0] Kembali ke Menu Utama")
        print("-" * 80)

        pilihan = input("Masukkan pilihan [0-6]: ").strip()

        if pilihan == "1":
            print("\n--- CATAT AKTIVITAS PETUGAS BARU (PUSH) ---")
            id_petugas = get_nonempty_input("ID Petugas (misal: PTG01) : ")
            if not id_petugas:
                continue
            nama_petugas = get_nonempty_input("Nama Lengkap Petugas       : ")
            if not nama_petugas:
                continue
            aktivitas_desc = get_nonempty_input("Deskripsi Tindakan / Aksi  : ")
            if not aktivitas_desc:
                continue

            try:
                act = AktivitasPetugas(
                    id_petugas=id_petugas,
                    nama=nama_petugas,
                    aktivitas=aktivitas_desc,
                    waktu=datetime.now()
                )
                evicted = stack.push(act)
                print(f"\n✅ Aktivitas berhasil dicatat ke puncak Stack:")
                print(f"   👉 {act}")
                if evicted:
                    print(f"   ⚠️  [BATAS 10 TERCAPAI]: Aktivitas terlama dibuang otomatis dari riwayat undo.")
                print_perf_badge("Stack.push()", stack.last_execution_time_ns, "O(1) amortized - list.append()")
            except Exception as err:
                print(f"\n❌ Gagal mencatat aktivitas: {err}")
            pause()

        elif pilihan == "2":
            print("\n--- BATALKAN AKTIVITAS TERAKHIR (UNDO / POP) ---")
            try:
                act = stack.pop()
                print(f"\n↩️  [BERHASIL DI-UNDO (DIBATALKAN)]")
                print(f"   ID Aksi    : {act.id_aktivitas}")
                print(f"   Petugas    : {act.nama} ({act.id_petugas})")
                print(f"   Aksi Batal : {act.aktivitas}")
                print(f"   Waktu Awal : {act.waktu.strftime('%Y-%m-%d %H:%M:%S')}")
                print_perf_badge("Stack.pop()", stack.last_execution_time_ns, "O(1) - list.pop() di akhir")
            except StackEmptyError as err:
                print(f"\n⚠️  {err}")
                print_perf_badge("Stack.pop() [Empty Check]", stack.last_execution_time_ns, "O(1)")
            pause()

        elif pilihan == "3":
            print("\n--- LIHAT AKTIVITAS TERAKHIR (PEEK) ---")
            try:
                act = stack.peek()
                print(f"\n👀 Aktivitas di puncak Stack (terakhir dicatat):")
                print(f"   👉 {act}")
                print_perf_badge("Stack.peek()", stack.last_execution_time_ns, "O(1) - list[-1]")
            except StackEmptyError as err:
                print(f"\n⚠️  {err}")
                print_perf_badge("Stack.peek() [Empty Check]", stack.last_execution_time_ns, "O(1)")
            pause()

        elif pilihan == "4":
            print("\n--- RIWAYAT AKTIVITAS PETUGAS (LIFO DISPLAY: TERBARU -> TERLAMA) ---")
            riwayat = stack.display()
            if not riwayat:
                print("\nℹ️  Stack KOSONG. Belum ada riwayat aktivitas yang dicatat.")
            else:
                print(f"\nTotal Aktivitas Tersimpan : {len(riwayat)} / {stack.MAX_CAPACITY}\n")
                print(f"{'Urutan Undo':<15} | {'Detail Aktivitas'}")
                print("-" * 80)
                for idx, act_str in enumerate(riwayat, start=1):
                    prefix = "🔝 [Puncak / Ke-1]" if idx == 1 else f"   [Undo ke-{idx:<2}]  "
                    print(f"{prefix} | {act_str}")
            print_perf_badge("Stack.display()", stack.last_execution_time_ns, f"O(n) - Iterasi terbalik {len(riwayat)} elemen")
            pause()

        elif pilihan == "5":
            print("\n--- STATUS DAN UKURAN STACK ---")
            size = stack.size()
            is_empty = stack.is_empty()
            print(f"   • Status Stack         : {'KOSONG' if is_empty else 'TERISI'}")
            print(f"   • Kapasitas Terisi     : {size} dari maksimal {stack.MAX_CAPACITY} aktivitas")
            print(f"   • Sisa Slot Undo       : {stack.MAX_CAPACITY - size} slot")
            print_perf_badge("Stack.size() & is_empty()", stack.last_execution_time_ns, "O(1)")
            pause()

        elif pilihan == "6":
            print("\n--- MEMUAT DATA CONTOH AKTIVITAS (DEMO 12 AKSI UNTUK MENGUJI BATAS 10) ---")
            petugas_sample = [
                ("PTG01", "Rina Marlina", "Mengubah status verifikasi berkas"),
                ("PTG02", "Bambang Tri", "Mencetak transkrip nilai sementara"),
                ("PTG01", "Rina Marlina", "Menyetujui cuti akademik semester genap"),
                ("PTG03", "Hendra Wijaya", "Memvalidasi KRS online mahasiswa"),
                ("PTG02", "Bambang Tri", "Mengunggah surat keterangan riset"),
                ("PTG01", "Rina Marlina", "Menerbitkan surat bebas pustaka"),
                ("PTG03", "Hendra Wijaya", "Mengupdate data no telepon mahasiswa"),
                ("PTG02", "Bambang Tri", "Menginput jadwal seminar proposal"),
                ("PTG01", "Rina Marlina", "Mengganti password akun portal"),
                ("PTG03", "Hendra Wijaya", "Memproses permohonan ijazah"),
                ("PTG02", "Bambang Tri", "Menolak pengajuan karena berkas kurang"),
                ("PTG01", "Rina Marlina", "Mengarsipkan berkas yudisium"),
            ]
            for p_id, p_nama, p_act in petugas_sample:
                act_obj = AktivitasPetugas(id_petugas=p_id, nama=p_nama, aktivitas=p_act)
                evicted = stack.push(act_obj)
                status_ket = "[EVICTED TERLAMA]" if evicted else "[OK]"
                print(f"   ➕ {status_ket} {act_obj.aktivitas}")
            print(f"\n✅ Total 12 aksi dimasukkan. Stack dibatasi secara ketat menjadi {stack.size()} aktivitas terbaru.")
            print_perf_badge("Stack.push() [Batch 12x Test Limit]", stack.last_execution_time_ns, "O(1) amortized")
            pause()

        elif pilihan == "0":
            break
        else:
            print("\n⚠️  Pilihan tidak valid! Silakan masukkan angka sesuai menu.")
            pause()



def submenu_status(queue: QueueSystem, stack: StackSystem) -> None:
    clear_screen()
    print_banner()
    waktu_skrg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n📊 [RINGKASAN STATUS KESELURUHAN SISTEM - {waktu_skrg}]\n")

    print("=" * 80)
    print("🔹 1. STATUS SISTEM ANTREAN (QUEUE - FIFO)")
    print("=" * 80)
    print(f"   • Jumlah Mahasiswa Menunggu : {queue.size()} orang")
    print(f"   • Status Antrean            : {'KOSONG' if queue.is_empty() else 'AKTIF'}")
    if not queue.is_empty():
        depan = queue.peek()
        print(f"   • Mahasiswa Terdepan (Next) : [No.{depan.no_antrian:03d}] {depan.nama} ({depan.keperluan})")
    else:
        print("   • Mahasiswa Terdepan (Next) : Tidak ada (antrean kosong)")

    print("\n" + "=" * 80)
    print("🔹 2. STATUS SISTEM UNDO AKTIVITAS (STACK - LIFO)")
    print("=" * 80)
    print(f"   • Jumlah Riwayat Tersimpan  : {stack.size()} / {stack.MAX_CAPACITY} aktivitas (Batas Max: 10)")
    print(f"   • Status Stack Undo         : {'KOSONG' if stack.is_empty() else 'AKTIF'}")
    if not stack.is_empty():
        top = stack.peek()
        print(f"   • Aksi Terakhir (Top Stack) : [{top.id_aktivitas}] {top.nama} -> {top.aktivitas}")
    else:
        print("   • Aksi Terakhir (Top Stack) : Tidak ada riwayat aktivitas")

    print("=" * 80)
    pause()



def submenu_benchmark() -> None:
    clear_screen()
    print_banner()
    print("\n⚡ [BENCHMARK & ANALISIS KECEPATAN WAKTU EKSEKUSI ALGORITMA]")
    print("Pengujian langsung efisiensi algoritma dengan 50.000 iterasi data secara real-time:\n")

    jumlah_elemen = 50_000
    print(f"⏳ Menjalankan pengujian performa ({jumlah_elemen:,} operasi)... Mohon tunggu sebentar.")

    # 1. Benchmark Queue Deque vs List Pop(0)
    from collections import deque
    q_test = deque()
    t0 = time.perf_counter_ns()
    for i in range(jumlah_elemen):
        q_test.append(i)
    t_q_enqueue = time.perf_counter_ns() - t0

    t0 = time.perf_counter_ns()
    while q_test:
        q_test.popleft()
    t_q_dequeue = time.perf_counter_ns() - t0

    # List pop(0) untuk komparasi (ambil 5.000 sampel agar tidak terlalu lambat)
    sample_list_n = 5_000
    list_bad = list(range(sample_list_n))
    t0 = time.perf_counter_ns()
    while list_bad:
        list_bad.pop(0)
    t_list_pop0 = time.perf_counter_ns() - t0

    # 2. Benchmark Stack List vs Deque
    stack_list = []
    t0 = time.perf_counter_ns()
    for i in range(jumlah_elemen):
        stack_list.append(i)
    t_stack_push = time.perf_counter_ns() - t0

    t0 = time.perf_counter_ns()
    while stack_list:
        stack_list.pop()
    t_stack_pop = time.perf_counter_ns() - t0

    print("\n" + "=" * 80)
    print(f"📊 HASIL PENGUJIAN KECEPATAN WAKTU EKSEKUSI (BENCHMARK)")
    print("=" * 80)
    print(f"1. QUEUE (collections.deque) - {jumlah_elemen:,} Elemen:")
    print(f"   • Enqueue (append)   : {format_duration(t_q_enqueue)} (Rata-rata: {t_q_enqueue/jumlah_elemen:.1f} ns/op) [O(1)]")
    print(f"   • Dequeue (popleft)  : {format_duration(t_q_dequeue)} (Rata-rata: {t_q_dequeue/jumlah_elemen:.1f} ns/op) [O(1)]")
    print(f"\n2. KOMPARASI: list.pop(0) - HANYA {sample_list_n:,} Elemen:")
    print(f"   • Dequeue (pop(0))   : {format_duration(t_list_pop0)} (Rata-rata: {t_list_pop0/sample_list_n:.1f} ns/op) [O(n)]")
    print(f"   💡 Perhatikan: list.pop(0) jauh lebih lambat karena harus menggeser seluruh elemen!")
    print(f"\n3. STACK (Python list) - {jumlah_elemen:,} Elemen:")
    print(f"   • Push (append)      : {format_duration(t_stack_push)} (Rata-rata: {t_stack_push/jumlah_elemen:.1f} ns/op) [Amortized O(1)]")
    print(f"   • Pop (pop akhir)    : {format_duration(t_stack_pop)} (Rata-rata: {t_stack_pop/jumlah_elemen:.1f} ns/op) [O(1)]")
    print("=" * 80)
    pause()


def main() -> None:
    queue = QueueSystem()
    stack = StackSystem(max_capacity=10)

    while True:
        clear_screen()
        print_banner()
        print("\n📋 [MENU UTAMA]")
        print("   [1] Sistem Antrean Mahasiswa           (Queue FIFO)")
        print("   [2] Sistem Undo Aktivitas Petugas      (Stack LIFO - Max 10 Undo)")
        print("   [3] Tampilkan Seluruh Status Sistem    (Monitoring Overview)")
        print("   [4] Benchmark Kecepatan Algoritma      (Real-time Time Complexity Demo)")
        print("   [0] Keluar dari Program")
        print("-" * 80)

        pilihan = input("Masukkan pilihan Anda [0-4]: ").strip()

        if pilihan == "1":
            submenu_queue(queue, stack)
        elif pilihan == "2":
            submenu_stack(stack)
        elif pilihan == "3":
            submenu_status(queue, stack)
        elif pilihan == "4":
            submenu_benchmark()
        elif pilihan == "0":
            print("\n" + "=" * 80)
            print("  Terima kasih telah menggunakan Sistem Layanan Administrasi Mahasiswa.")
            print("  Program selesai dengan sukses. Sampai jumpa!")
            print("=" * 80 + "\n")
            sys.exit(0)
        else:
            print("\n⚠️  Pilihan tidak valid! Silakan masukkan angka [0-4].")
            pause()


if __name__ == "__main__":
    main()
