# Personal Portfolio Website
Name : Enzo Susilo
NPM : 2506584382
Class : PBP B

Repositori ini berisi kode sumber (*source code*) untuk website portofolio pribadi yang dikembangkan sebagai pemenuhan tugas dari mata kuliah Pemrograman Berbasis Platform (PBP) Fasilkom UI. 

## PWS Deployment Link
* [Tautan PWS / Deployment](https://enzo-susilo-myportofolio.pws.cs.ui.ac.id/)

## Instruksi Setup (Cara Menjalankan Secara Lokal)
Untuk menjalankan proyek ini di komputer lokal Anda, ikuti langkah-langkah berikut:
1. Pastikan Python sudah terinstal di sistem Anda.
2. *Clone* repositori ini ke perangkat lokal Anda.
3. Buka terminal/command prompt, lalu arahkan ke direktori proyek ini.
4. Jalankan perintah berikut untuk menyalakan *local server*:
   `python manage.py runserver`
5. Buka *browser* pilihan Anda dan akses alamat `http://localhost:8000`.

## Progress Log
* **Week 1 - 7 September 2026 (Tugas 1)**
  * Menambahkan tampilan website mengikuti instruksi Tutorial 1.
  * Menambahkan section Experience, Education (Academic Milestones).
* **Week 2 - 14 September 2026 (Tugas 2)**
  * Memindahkan section Academic Milestones (Education) ke template yang berbeda/halaman baru.
  * Menerapkan arsitektur MVT untuk data yang ditampilkan pada website (menjadi dinamis,tidak hardcoded lagi).
  * Melakukan beberapa penyesuaian seperti pada format academic milestones dan mengganti experience pada halaman profile menjadi "committee".

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5. Elemen `<section>` digunakan untuk membagi halaman ke dalam area tematik besar (seperti `<section id="education">` dan `<section id="experience">`), sementara tag `<article>` membungkus setiap entri individual (seperti riwayat organisasi staf IGI CompFest atau pengajar BETIS). Penggunaan elemen semantik ini memberikan struktur hierarki yang jauh lebih bermakna bagi Search Engine Optimization (SEO) (dari hasil search saya) dan screen reader dibandingkan sekadar menggunakan `<div>` yang hanya berfungsi sebagai pembungkus tata letak kosmetik.

2. Tantangan tata letak terbesar adalah mempertahankan keterbacaan Bento Box Layout pada bagian edukasi. Di layar desktop, saya menggunakan grid-template-columns: 1.8fr 1fr agar membagi ruang secara asimetris. Namun, saat dievaluasi pada layar mobile, menjejalkan tata letak tersebut membuat teks terlalu sempit. Oleh karena itu, saya menggunakan media query @media (max-width: 600px) untuk memprioritaskan tata letak vertikal menjadi satu kolom penuh (grid-template-columns: 1fr). Selain tantangan grid, interaksi layar sentuh juga membuat animasi hover bawaan desktop menjadi bermasalah (glitch) dan memotong gambar logo (pada section academic milestones). Sebagai penyelesaian, saya memprioritaskan keutuhan visual dengan menonaktifkan efek zoom (transform: none) dan menerapkan object-fit: contain khusus di resolusi mobile agar gambar tidak mendominasi rasio layar kecil.

3. Batasan utama dari static web murni adalah proses pembaruan konten yang repetitif dan tidak efisien. Jika saya ingin menambahkan riwayat pengalaman baru, saya harus mengubah struktur HTML dan mengonfigurasi CSS secara manual. Berdasarkan batasan tersebut, fungsionalitas dinamis yang paling ingin saya tambahkan adalah integrasi database menggunakan arsitektur Model-View-Template (MVT). Sistem ini akan memungkinkan penambahan, pengeditan, atau penghapusan entri portofolio secara dinamis melalui halaman admin panel tanpa perlu merombak kode sumber.

**AI Disclosure & Log Prompting**
* Tools: ChatGPT

* Log Prompting ChatGPT: https://chatgpt.com/share/6a9e9301-9b2c-83ec-b5b1-ef0d78dd04f1

* Bagian yang dibantu AI: Pada tugas 1 ini, saya menambahkan section baru untuk Academic Milestones (Education) dan Experience di  halaman yang sama. Saya menginginkan desain yang modern, yaitu menggunakan referensi Bento Box Layout untuk edukasi/academic milestones dan Vertical Timeline kayak LinkedIn untuk riwayat organisasi. Saya menggunakan bantuan AI untuk membantu saya generate kerangka dasar HTML dan hitungan grid CSS sesuai ide yang ingin saya implementasikan dan juga menambahkan constraint seperti instruksi dari soal. Saya juga menggunakan bantuan AI untuk membantu saya memberi contoh standard open resource read-me serta pertanyaan random lainnya.

* Kritik Keterbatasan AI & Perbaikan Manual yang Saya Lakukan:
Walaupun AI sangat membantu menyusun kerangka awalnya, desain bawaannya masih cukup kaku dan ada beberapa fungsionalitas yang terlewat, sehingga saya harus melakukan perombakan manual:

    * Modifikasi Grid Bento Box untuk Academic Milestones: AI awalnya menyarankan pembagian rasio kolom 1.5fr 1fr. Setelah saya evaluasi, saya mengubahnya secara manual menjadi 1.8fr 1fr agar kotak utama memiliki ruang yang lebih lega, sehingga teks deskripsi jurusan saya tidak berantakan memanjang ke bawah.

    * Merapikan Proporsi Logo di Timeline pada bagian Experience: Kode dari AI membatasi ukuran logo organisasi hanya 70% dan mengurungnya dengan garis tepi (border), yang membuat logo terpotong saat terkena animasi hover zoom. Saya memperbaiki CSS-nya mandiri dengan menghapus border dan memaksimalkan proporsi menjadi width: 100%; height: 100%; object-fit: cover;. Hasilnya, logo berlatar belakang (seperti logo UI atau BETIS) bisa menyebar penuh dan pas di dalam lingkaran timeline.

    * Menyambungkan Menu Navigasi: AI membuatkan kerangka `<section id="experience">` di struktur bawah, tetapi lupa menyambungkannya ke menu atas. Saya harus menyisipkan elemen `<a href="#experience">` secara manual di dalam tag `<nav>` agar navigasi scroll halamannya bisa berfungsi.

    * Menyesuaikan Aset & Konten Asli: AI menulis jalur direktori gambar (path) yang salah sehingga memicu broken image. Saya merapikan struktur folder lokal secara manual, sekaligus merombak total teks dummy bawaan AI menggunakan data asli saya (nilai IELTS Band 7, medali SASMO, serta deskripsi kepanitiaan DDP0 , KMK Fasilkom, BETIS, dan IGI CompFest).

    * Penyesuaian Animasi Layar Sentuh (Mobile/Hp): AI memberikan efek animasi `:hover` yang bekerja baik di desktop dengan kursor, namun menimbulkan *glitch* visual dan membuat logo terpotong saat disentuh di layar HP. Saya secara manual mematikan efek `transform` dan menambahkan `object-fit: contain` khusus pada `@media (max-width: 600px)` agar logo statis, proporsional, dan warnanya langsung terlihat utuh tanpa perlu interaksi layar sentuh.

### Tugas 2

1. Ketika pengguna membuka halaman *Academic Milestones/Achievements* (misalnya menekan tautan di *navbar*), *browser* mengirimkan HTTP *Request* ke *server*.
* Pertama, *request* diterima oleh pengatur rute utama (yang ada di proyek `portofolio` ), lalu diteruskan ke `urls.py` di dalam aplikasi `main`.
* Di `main/urls.py`, *path* URL (`achievements/`) akan dipetakan untuk memanggil fungsi `show_achievements` di dalam `views.py`.
* *View* tersebut kemudian berkomunikasi dengan `models.py` untuk mengambil seluruh objek data dari model `Achievement` yang ada di dalam *database*.
* Setelah data didapatkan, *View* membungkusnya ke dalam *context dictionary* dan mengirimkannya ke `achievements.html` (*Template*).
* *Template* kemudian menggunakan *Django Template Language* (DTL) untuk me-*render* data tersebut menjadi elemen-elemen HTML (menggunakan perulangan). HTML final ini lalu dikirimkan kembali ke *browser* pengguna sebagai HTTP *Response* untuk ditampilkan.

2. Menyimpan data pada model (*database*) memastikan adanya pemisahan antara antarmuka visual (UI) dan logika data (*Separation of Concerns*). Jika data di-*hardcode* di dalam *template*, penambahan data baru akan memaksa pengembang untuk membongkar dan mengubah kode HTML, yang berisiko merusak layout dan memakan waktu.
Dampaknya terhadap pemeliharaan sangat signifikan, yakni aplikasi menjadi jauh lebih *scalable*. Jika ada penambahan sertifikasi atau pencapaian baru, saya hanya perlu menginputnya melalui panel Django Admin. Sistem DTL akan otomatis me-*render* kartu baru di *website* tanpa perlu menyentuh sebaris pun kode HTML atau CSS.

3. 
* `makemigrations`: Berfungsi untuk mencatat perubahan yang kita tulis di file `models.py` setelah membuat models baru dan menerjemahkannya menjadi sebuah "cetak biru" atau skema instruksi (file Python di folder `migrations/`). Perintah ini belum menyentuh *database* secara langsung, hanya menyiapkan riwayat perubahannya saja.
* `migrate`: Berfungsi untuk mengeksekusi cetak biru yang dibuat oleh `makemigrations` ke dalam *database* secara nyata (mengubah struktur tabel menggunakan SQL).
* **Contoh:** Ketika saya membuat model `Achievement` baru dengan *field* `title`, `description`, `category`, `year`, dan `thumbnail`, saya harus menjalankan `makemigrations` untuk mencatat pembuatan model ini, lalu menjalankan `migrate` agar tabel `main_achievement` benar-benar terbuat di dalam *database* SQLite.

**AI Disclosure & Log Prompting (Tugas 2)**
Tugas 2 ini saya kerjakan dengan bantuan AI untuk memastikan implementasi Django MVT berjalan efektif tanpa merusak struktur antarmuka yang sudah ada. Pada tugas ini saya memindahkan 1 section pada halaman utama saya ke halaman baru, yaitu section academic milestones (achievements).

* **Tools yang dipakai:** Google Gemini
* **Strategi Prompting:** *Context-aware prompting*. Saya memberikan instruksi tugas kepada AI, dipadukan dengan memberikan *screenshot* struktur folder *project*, serta *copy-paste* langsung kode CSS, HTML, dan file Python saya. Hal ini dilakukan agar AI dapat memberikan instruksi/panduan untuk saya yang spesifik/jelas sesuai hierarki proyek saya, bukan instruksi *template* yang umum (sesuai permintaan saya bagian mana yang ingin dipandu untuk dipindahkan).
* **Bagian spesifik yang dibantu AI:**
  1. Merancang logika DTL (Django Template Language) terstruktur di dalam *template* menggunakan `{% forloop.first %}`. Bantuan ini sangat membantu projek saya agar data dinamis dari *database* tetap bisa menyesuaikan diri dengan tata letak Bento Grid CSS yang sudah saya miliki (kartu pertama selalu besar, sisanya kartu kecil).
  2. Menyusun strategi pemisahan revisi (*atomic commits*) yang sesuai dengan standar *Conventional Commits* untuk poin disiplin Git.
  3. Merumuskan struktur *Unit Test* yang mencakup pengecekan HTTP 200, kemunculan data di DTL, serta validasi pesan *empty state*.
* **Analisis Kritis & Intervensi Mandiri:**
  Saya tidak sekadar menyalin kode secara buta, melainkan melakukan validasi logika terhadap kode yang dihasilkan AI. Beberapa contohnya :
  * **Konseptualisasi Kategori Data:** Saya memutuskan untuk menyatukan riwayat edukasi formal (S1 Ilmu Komputer) dan penghargaan (SASMO, IELTS) ke dalam satu model universal `Achievement` menggunakan fitur `CATEGORY_CHOICES`, daripada membuat tabel terpisah yang kurang efisien secara struktur *database*.
  * **Validasi Mekanisme Tata Letak (DTL):** Saya secara aktif meninjau alasan di balik struktur perulangan DTL yang disarankan. Saya memvalidasi bahwa penggunaan `forloop.first` mutlak diperlukan untuk memisahkan *rendering* HTML antara "kartu fitur besar" (kiri) dan "kartu kecil" (kanan) agar rasio *Bento Grid/layout* saya tidak rusak saat data bertambah di kemudian hari.
  * **Debugging Proses Pengujian:** Saat mengeksekusi *unit test* secara lokal, terminal awalnya hanya mendeteksi 6 fungsi tes dari total 9 tes yang ada. Saya melakukan peninjauan lingkungan pengembangan lokal untuk memastikan sinkronisasi penyimpanan *file* sebelum akhirnya seluruh *test* berhasil divalidasi dengan status `OK`.
  * Saya juga mengubah yang awalnya statis seperti 'MATHEMATICS' jadi dinamis menggunakan `{{ achievement.get_category_display }}`. Jadi hanya berdasarkan category yang dipilih.
  * Saya menganalisis fungsi dari sintaks spesifik yang disarankan AI untuk memastikan kesesuaian dengan desain awal. Misalnya, saya memvalidasi penggunaan grid-column: 1 / -1 pada pesan empty state agar teks membentang penuh dan tidak terjepit di satu sel grid. Juga ada trik penomoran visual 0{{ forloop.counter0 }} untuk memastikan urutan indeks kartu kecil (01, 02, dst.) di DTL tetap menghasilkan output yang identik dengan desain statis saya yang sebelumnya.