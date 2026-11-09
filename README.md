# Personal Portfolio Website
Name : Enzo Susilo
NPM : 2506584382
Class : PBP B

Repositori ini berisi kode sumber (*source code*) untuk website portofolio pribadi yang dikembangkan sebagai pemenuhan tugas dari mata kuliah Pemrograman Berbasis Platform (PBP) Fasilkom UI. 

## PWS Deployment Link
* [Tautan PWS / Deployment](https://enzo-susilo-myportofolio.pws.cs.ui.ac.id/)

## Instruksi Setup (Cara Menjalankan Secara Lokal)
Environment pengujian menggunakan Python 3.13, Django seri 5.2, dan DRF seri 3.18. Jalankan dari folder yang berisi `manage.py`. Contoh untuk PowerShell Windows:

```powershell
py -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Jika `env` sudah ada, cukup aktifkan kembali. Untuk development lokal, gunakan `PRODUCTION=False` pada `.env` lokal agar memakai SQLite dan cookie sesuai HTTP lokal. `.env`, database lokal, dan virtual environment tidak disimpan ke Git.

```powershell
python manage.py migrate
python manage.py check
python manage.py runserver
```

Buka `http://localhost:8000`. Jika belum ada pemilik portofolio lokal, jalankan `python manage.py createsuperuser` dan masukkan kredensial secara interaktif. Untuk menguji Editor, buat Group bernama tepat `Editor` melalui Django Admin dan tambahkan akun uji biasa ke grup tersebut. Keanggotaan grup ini digunakan oleh permission aplikasi; tidak perlu mengganti pendekatannya menjadi `has_perm()`.

Jika aktivasi environment tidak tersedia, setiap command `python` dapat diganti dengan `.\env\Scripts\python.exe`. Di PWS, pertahankan konfigurasi production, database, dan origin HTTPS milik deployment.

## Progress Log
* **Week 1 - 7 September 2026 (Tugas 1)**
  * Menambahkan tampilan website mengikuti instruksi Tutorial 1.
  * Menambahkan section Experience, Education (Academic Milestones).
* **Week 2 - 14 September 2026 (Tugas 2)**
  * Memindahkan section Academic Milestones (Education) ke template yang berbeda/halaman baru.
  * Menerapkan arsitektur MVT untuk data yang ditampilkan pada website (menjadi dinamis,tidak hardcoded lagi).
  * Melakukan beberapa penyesuaian seperti pada format academic milestones dan mengganti experience pada halaman profile menjadi "committee".
* **Week 3 - 21 September 2026 (Tugas 3)**
  * Mengimplementasikan `ModelForm` (`ExperienceForm`) dan fitur CRUD (Create, Read, Update, Delete) beserta *JSON views* untuk *section Experience*.
  * Mengintegrasikan tombol aksi CRUD, fitur pencarian, dan memisahkan komponen *modal* konfirmasi hapus ke dalam *layout* utama.
  * Meningkatkan UI/UX dengan menambahkan efek transisi *hover* (terangkat) pada tombol global dan animasi *zoom* pada komponen *card*.
  * Melakukan perbaikan *bug* minor pada *unit test* (`tests.py`) serta melengkapi dokumentasi tugas.
* **Week 4 - 28 September 2026 (Tugas 4)**
  * Mengimplementasikan autentikasi dan otorisasi menggunakan pembatasan akses @login_required dan pengecekan hak akses is_superuser serta grup Editor menggunakan is_admin, jadi di django admin web tinggal buat group namany editor.
  * Menambahkan relasi ManyToManyField pada model Experience untuk fitur interaktif pemberian star.
  * Mengamankan endpoint API JSON dengan menerapkan parameter use_natural_foreign_keys=True untuk mencegah kebocoran data sensitif user ID.
* **Week 5 - 5 Oktober 2026 (Tugas 5)**
  * Mengubah halaman Experience agar memuat dan menampilkan data secara asinkron melalui AJAX menggunakan endpoint JSON manual.
  * Menambahkan pencarian berdasarkan judul dengan *debouncing* 300 milidetik, termasuk tampilan *loading*, *empty state*, dan *error state*.
  * Memindahkan form tambah Experience ke dalam modal berbasis Popover API dan mengirimkan form melalui Fetch API dengan proteksi CSRF serta status respons 201, 400, dan 403.
  * Mempertahankan fitur *star* dan pembatasan akses dari Tugas 4, serta menambahkan perlindungan XSS pada sisi klien dan server.
  * Menambahkan pengujian untuk endpoint AJAX, otorisasi, validasi form, pencarian, dan sanitasi masukan.
* **9 November 2026 (Tugas 6)**
  * Melanjutkan fondasi permission dan API Experience dari Tutorial 07 menjadi API DRF lengkap untuk bagian pilihan Tugas 3-5.
  * Menambahkan informasi star read-only, pencarian judul, dan endpoint star berbasis akun session.
  * Menghubungkan halaman Experience ke API baru untuk daftar, pencarian, tambah, star/unstar, dan hapus tanpa reload dokumen.
  * Mengubah halaman edit yang sudah ada agar menyimpan perubahan melalui PATCH, dengan akses untuk Editor dan superuser.
  * Menambahkan test validasi, empat peran, CSRF, tampilan form, escaping, dan regresi Projects; seluruh 50 test app `main` lulus pada pemeriksaan lokal.

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


### Tugas 3

1. Kita menggunakan `ModelForm` karena jauh lebih efisien dan mengadopsi prinsip *DRY (Don't Repeat Yourself)*. Daripada harus mengetik tag `<input>` HTML satu per satu dan membuat validasi manual dari nol, `ModelForm` secara otomatis membaca skema dari model `Experience` saya (seperti *title*, *description*, *category*) dan langsung men-*generate* elemen form HTML yang sesuai beserta sistem validasinya.
Terkait `{% csrf_token %}`, ini adalah mekanisme keamanan wajib dari Django untuk mencegah serangan *Cross-Site Request Forgery* (CSRF). Token ini memastikan bahwa data form yang dikirim (di-*submit*) ke *server* benar-benar berasal dari website saya sendiri, bukan dari *script* jahat atau *website* pihak ketiga yang mencoba memalsukan aksi seolah-olah itu adalah saya pengguna aslinya.

2. JSON (*JavaScript Object Notation*) jauh lebih disukai karena sintaksnya sangat ringan, ringkas, dan mudah dibaca oleh kita manusia. Berbeda dengan XML yang sangat boros karakter karena harus menggunakan tag penutup berlapis (seperti HTML). Selain itu, JSON adalah format *native* dari JavaScript. Di era web modern di mana hampir semua *frontend* menggunakan JavaScript, memproses data JSON bisa langsung dilakukan tanpa perlu di-*parsing* secara rumit seperti XML, sehingga performa pertukaran data antara *Client* dan *Server* menjadi jauh lebih cepat.

3. Alurnya dimulai ketika *URL routing* memanggil fungsi `get_experience_json` di `views.py`. Fungsi tersebut akan melakukan *query* ke *database* (`Experience.objects.all()`) untuk mengambil seluruh objek riwayat pengalaman saya. Setelah data didapat, data tersebut dimasukkan ke dalam fungsi `serializers.serialize("json", experiences)` untuk diubah menjadi format teks JSON, lalu dikembalikan ke *browser* melalui `HttpResponse` dengan *content-type* `application/json`.
Proses *serialization* ini diperlukan karena *browser* atau aplikasi klien tidak mengerti apa itu "Objek Model Django" atau Python. Objek-objek kompleks dari *database* tersebut harus "diterjemahkan" (diserialisasi) ke dalam format universal berbasis teks (seperti JSON) agar bisa ditransmisikan lewat protokol HTTP dan dibaca oleh sistem apa pun.


**AI Disclosure & Log Prompting (Tugas 3)**

*   **Tools:** Google Gemini Pro 
*   **Log Prompting:** https://share.gemini.google/0pltDWZ1KlW8
*   **Strategi Prompting:** Saya tidak menggunakan AI untuk memberi saya kode yang langsung selesai/tinggal saya copas all in one. Saya menggunakan AI untuk memandu saya langkah demi langkah sesuai instruksi tugas 3, menanyakan konsep-konsep yang membuat saya bingung selama pengerjaan, serta meminta panduan *commit* yang benar dan profesional.
Pada tugas ini saya memilih halaman experience dari portofolio saya untuk ditambahkan fitur CRUD.
*   **Bagian spesifik yang dibantu AI:**
    1. Memahami alur logika `ModelForm` dan cara kerja deserialisasi JSON pada *views*.
    2. Kerangka untuk implementasi form,view,url, dan template dasar. (Ai memandu saya dalam alur pembuatan form ini, serta mengoreksi kesalahan saya ketika saya menyesuaikan sendiri dari yang sudah ada pada project)
    3. Memberikan panduan penggunaan *conventional commits* untuk memenuhi kriteria rubrik disiplin Git.

*   **Kritik Keterbatasan AI & Perbaikan Manual yang Saya Lakukan:**
    Saya tidak menggunakan kode AI secara mentah karena AI biasanya memberikan *template* yang statis dan kaku. Beberapa perombakan dan manual yang saya lakukan:
    *  **Adaptasi Logika Model & Form:** Walaupun AI langsung memberikan struktur kode `routing` dan `redirect` yang tepat, saya tidak sekadar melakukan *copy-paste*. Saya memverifikasi sendiri bagaimana logika tersebut diadaptasi untuk model `Experience` saya. Saya memastikan bahwa *form* untuk menambah dan memperbarui data menggunakan `get_object_or_404(Experience, pk=experience_id)` dan `instance=experience`, serta dikembalikan secara konsisten ke rute `main:show_experience` menggunakan satu *template* yang sama, yaitu `experiences_form.html`.
    *  **Implementasi Komponen Modal delete:** Pada panduan awalnya, AI tidak menginstruksikan saya untuk membuat direktori atau *file* komponen baru untuk fitur penghapusan data. Namun, dengan inisiatif sendiri agar struktur kode lebih rapi seperti pola pada proyek sebelumnya, saya memisahkan implementasi *HTML Native Popover* tersebut ke dalam *file* `components/experience_delete_modal.html`. Saya mengadaptasi kode komponen *modal* yang sudah ada, mengganti konteksnya menjadi `experience`, dan mengintegrasikannya ke HTML utama agar lebih *reusable* dan bersih.
    *  **Kustomisasi Ekstra Interaktivitas (UI/UX):** Kode dari AI hanya mewarisi gaya CSS lama yang polos. Untuk mencapai poin maksimal pada rubrik kesesuaian topik (fitur ekstra), saya bereksperimen secara manual memodifikasi CSS global. Saya menambahkan hierarki warna tombol (aksi utama, sekunder, *danger*) serta memberikan efek transisi `transform` dan `box-shadow`. Hasilnya, setiap tombol dan kartu pengalaman (*card*) memiliki animasi membesar dan terangkat saat di-*hover*.
    *  **Human Error pada Unit Test:** Saat menjalankan *automated testing* (`tests.py`), saya mendapati *error* pada bagian ekspektasi teks. Ini murni kesalahan saya, di mana saya secara manual mengganti teks *empty state* di HTML dari "pengalaman" menjadi "experience", tetapi lupa menyamakan *string* tersebut di *file* pengujian. Saya mengidentifikasi perbedaan *string* ini secara mandiri dan menyinkronkannya sehingga *test* kembali *Pass*.

### Tugas 4
**AI Disclosure & Log Prompting (Tugas 4)**

*   **Tools:** Google Gemini Pro 
*   **Log Prompting:** -
*   **Strategi Prompting:** Saya tidak menggunakan AI untuk memberi saya kode yang langsung selesai/tinggal saya copas all in one. Saya menggunakan AI untuk memandu saya langkah demi langkah sesuai instruksi tugas 4, serta mengkonfirmasi jawaban saya apakah sudah benar atau belum dan panduan commit yang benar.
Pada tugas ini saya memilih halaman experience dari portofolio saya untuk memenuhi instruksi tugas 4
*   **Bagian spesifik yang dibantu AI:**
    1. Merancang logika server-side authorization untuk mengecek keanggotaan pengguna di dalam Django Group ("Editor") beserta pembatasan akses @login_required.
    2. Menyusun urutan atomic commit (pemisahan commit untuk migrasi, routing, views.py, dan UI) agar riwayat Git terstruktur.

*   **Kritik Keterbatasan AI & Perbaikan Manual yang Saya Lakukan:**
    *  **Keterbatasan Logika DTL (Django Template Language):** Karena HTML Django tidak bisa mengeksekusi query filter grup secara langsung di dalam template, AI memberikan dua opsi: menggunakan sistem Permissions bawaan atau membuat variabel context baru. Saya melakukan analisis mandiri dan memilih pendekatan variabel is_admin di views.py (is_admin = request.user.is_superuser or request.user.groups.filter(name="Editor").exists()). Saya menyisipkan variabel ini secara manual agar tag HTML saya tetap bersih ({% if is_admin %}) dan saya tidak perlu mengatur ulang permissions satu per satu di panel admin.
    *  **Kepatuhan Ketat pada Tutorial API:** Saat mengamankan endpoint JSON dari kebocoran data sensitif (user ID pada field star), AI awalnya merekomendasikan best practice industri dengan menyembunyikan field tersebut secara total menggunakan parameter fields=(...). Saya mengoreksi instruksi ini secara mandiri dengan merujuk pada gambar panduan tutorial, lalu mengubahnya menjadi implementasi use_natural_foreign_keys=True di dalam serializers.serialize agar ID diterjemahkan menjadi username aslinya, memastikan kode saya 100% akurat dengan ekspektasi asisten dosen.
    * **Pemisahan Hak Akses Spesifik/otorisasi (Superuser vs Editor):** AI awalnya menyarankan logika otorisasi yang menggabungkan hak akses Superuser dan Editor ke dalam satu variabel (is_admin), sehingga peran Editor berpotensi bisa melakukan Create dan Delete. Setelah saya meninjau ulang rubrik hak akses minimum, saya menyadari bahwa Editor seharusnya hanya memiliki hak Update. Saya kemudian secara mengganti views.py dan template HTML, yaitu fungsi Create dan Delete hanya untuk is_superuser, dan Update (tombol Edit) hanya untuk grup Editor. Juga pada project jg saya batasi editor gabisa ngeliat tombol delete atau create, walau pada projek ga ada tombol edit
    * **Perbaikan message stacking** : awalnya ngestack di page login

### Tugas 5

1. *Debouncing* adalah teknik untuk menunda pemanggilan suatu fungsi sampai pengguna berhenti melakukan aksi selama waktu tertentu. Pada pencarian Experience, setiap perubahan pada kolom pencarian akan membatalkan `setTimeout` sebelumnya dan membuat jadwal baru selama 300 milidetik. Dengan demikian, permintaan AJAX baru dikirim setelah pengguna berhenti mengetik sejenak, bukan pada setiap karakter yang dimasukkan.
Teknik ini penting karena dapat mengurangi jumlah *request* ke server, penggunaan jaringan, dan beban kueri database. Selain *debouncing*, implementasi saya menggunakan `AbortController` untuk membatalkan permintaan sebelumnya sehingga respons lama tidak menimpa hasil pencarian terbaru.

2. `fetch()` mengembalikan sebuah `Promise`, bukan langsung objek respons. `await fetch(...)` digunakan untuk menunggu sampai server memberikan objek `Response`, sedangkan `await response.json()` menunggu sampai isi respons selesai dibaca dan diubah menjadi data JavaScript.
Jika `await` dihilangkan tanpa menggantinya dengan rangkaian `.then()`, variabel yang diterima masih berupa `Promise`. Akibatnya, properti seperti `response.ok` atau metode untuk membaca data belum dapat digunakan sebagaimana mestinya, dan kode berikutnya dapat berjalan sebelum data tersedia. `await` hanya menjeda fungsi `async` yang sedang berjalan, bukan membekukan seluruh halaman browser.

3. *Cross-Site Scripting* (XSS) adalah serangan ketika masukan berbahaya berupa HTML atau JavaScript disisipkan ke halaman lalu dijalankan pada browser pengguna lain. Django Template secara bawaan melakukan *auto-escaping* terhadap nilai yang ditampilkan dengan sintaks `{{ ... }}`. Namun, pada halaman berbasis AJAX, data JSON dirangkai menjadi HTML melalui JavaScript dan dimasukkan menggunakan `innerHTML`, sehingga perlindungan otomatis dari Django Template tidak ikut bekerja.
Karena itu, implementasi saya mengubah setiap nilai teks menjadi bentuk aman menggunakan fungsi `escapeHtml()` sebelum dimasukkan ke HTML. Pada server, `ExperienceForm` juga membersihkan tag HTML dari `title` dan `description` menggunakan `strip_tags` sebagai pertahanan tambahan. Pesan toast ditampilkan menggunakan `textContent`. Sanitasi sisi server tetap tidak menggantikan kewajiban melakukan *escaping* sesuai konteks pada sisi klien.

**AI Disclosure & Log Prompting (Tugas 5)**

* **Tools yang dipakai:** Google Gemini (utama) dan asisten pemrograman AI di IDE.
* **Log Prompting:** https://share.gemini.google/SWbX4RIEebSS
* **Strategi Prompting:** Saya lebih dahulu meminta Gemini memberikan panduan Tugas 5 tanpa menyertakan kode proyek. Setelah itu, saya mencoba untuk menyesuaikan sesuai dengan tutorial 5 sebelumny, lalu saya kirim ke gemini untuk dicek apakah sudah sesuai kah penyesuaiannya. Saya juga ada minta ai agent pada IDE untuk buatin unit test karena itu paling susah sih bagi saya dan disarankan gemini.
Pada tugas ini saya memilih halaman experience dari portofolio saya untuk memenuhi instruksi tugas 5
* **Bagian spesifik yang dibantu AI:**
  1. Gemini membantu memberikan gambaran awal mengenai endpoint JSON, penggunaan Fetch API, *debouncing*, modal AJAX, dan mitigasi XSS.
  2. Gemini membantu menyusun tahapan *Conventional Commits* agar perubahan dapat disimpan secara bertahap dan terstruktur.

* **Kritik Keterbatasan AI & Penyesuaian yang Dilakukan:**
  * **Asumsi struktur model yang tidak sesuai:** Gemini menggunakan field `company`, `stars`, dan `user`, sedangkan model proyek menggunakan `category`, `thumbnail`, dan relasi `starred_by`, serta tidak memiliki field `user`. Instruksi seperti `experience.user = request.user` tidak digunakan karena akan menyebabkan kesalahan. Endpoint dan form disesuaikan dengan field model yang sebenarnya.
  * **Hak akses terlalu luas:** Gemini menyarankan agar seluruh pengguna yang telah login dapat menambah data. Hal ini tidak sesuai dengan aturan Tugas 4 yang sudah diterapkan. Implementasi akhirnya mempertahankan Create dan Delete khusus Superuser, Update untuk Superuser atau Editor, Read untuk semua pengguna, dan Star untuk pengguna yang telah login.
  * **Ketergantungan Bootstrap yang tidak tersedia:** Contoh Gemini memakai `bootstrap.Modal`, atribut `data-bs-*`, dan kelas `d-none`, padahal proyek tidak memuat Bootstrap. Modal kemudian dibuat menggunakan HTML Native Popover API dan kelas CSS yang telah digunakan oleh proyek.
  * **Komponen proyek tidak dimanfaatkan:** Gemini membuat sistem toast baru dan nama template generik seperti `experience_page.html`, padahal proyek sudah memiliki fungsi global `showToast`, template `experience.html`, serta pola komponen modal sendiri. Solusi disesuaikan agar memakai komponen dan konvensi yang sudah ada.
  * **Fitur lama berisiko hilang:** Contoh kartu dinamis dari Gemini belum mempertahankan tombol Star, Edit, dan Delete beserta aturan tampil untuk setiap peran. Rendering AJAX diperbaiki agar seluruh fungsi dari Tugas 4 tetap tersedia setelah data dimuat ulang.
  * **Penanganan validasi dan keamanan belum cukup kuat:** Respons error awal menggunakan representasi mentah `form.errors`, dan fungsi *escaping* mengasumsikan semua input selalu berupa string. Implementasi diperbaiki dengan `form.errors.get_json_data()`, konversi `String(value ?? '')`, pembersihan tag pada `ExperienceForm`, dan pengecekan keberadaan form sebelum memasang *event listener*.

### Tugas 6

1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!**

   REST (*Representational State Transfer*) adalah gaya arsitektur untuk merancang interaksi dengan resource. Pada implementasi ini, URL menunjukkan resource, HTTP method menyatakan tindakan, dan response menggunakan status yang sesuai. Misalnya, `GET /api/v1/experience/` membaca daftar, `POST` pada URL yang sama membuat data, dan `PATCH /api/v1/experience/<uuid>/` memperbarui sebagian data. JSON hanya format representasi; endpoint yang mengembalikan JSON belum otomatis memiliki pengaturan resource, method, dan kontrak yang konsisten dengan REST. Prinsip stateless juga berkaitan dengan kemandirian setiap request. Penggunaan session Django di proyek ini merupakan pilihan praktis untuk website dengan AJAX dalam session yang sama, bukan contoh REST yang sepenuhnya stateless.

   PUT digunakan ketika klien mengirim representasi pengganti yang lengkap, misalnya mengirim ulang judul, deskripsi, kategori, dan thumbnail setelah menyunting seluruh data Experience. PATCH digunakan ketika hanya beberapa field ingin diubah, misalnya hanya judul Experience. API memakai `partial=True` untuk PATCH sehingga description yang tidak dikirim tetap memakai nilai lama. PUT dengan hanya title ditolak karena description wajib. Pada serializer ini, field opsional yang tidak dikirim saat PUT tidak otomatis selalu dikosongkan; perilakunya mengikuti aturan serializer.

2. **Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?**

   `ExperienceSerializer` mengubah objek model menjadi representasi yang dapat dirender DRF sebagai JSON, dan memvalidasi input sebelum menyimpan perubahan. Daftar field ditulis eksplisit. Field model menyediakan validasi dasar, seperti choices kategori dan format URL thumbnail, sementara `validate_title` dan `validate_description` membersihkan tag HTML serta menolak teks yang menjadi kosong. Validasi `ExperienceForm.clean_*` tidak otomatis dipanggil oleh serializer, sehingga aturan input API ditulis pada serializer itu sendiri.

   Dibanding merakit dictionary satu per satu dalam `JsonResponse`, serializer menyatukan representasi, validasi, serta create/update dalam kontrak yang dapat digunakan kembali. Informasi `star_count`, `is_starred`, dan `starred_by_names` dihitung server dan bersifat read-only. `context` request memungkinkan status star sesuai akun yang sedang melihat. Email, password hash, dan objek User lengkap tidak ikut ditampilkan. `strip_tags` bukan jaminan sanitasi HTML yang menyeluruh; frontend tetap memakai escaping atau `textContent` saat menampilkan data.

3. **Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**

   Autentikasi mengenali siapa pengirim request. `SessionAuthentication` menggunakan session login Django untuk mengisi `request.user`. Otorisasi menentukan tindakan yang boleh dilakukan akun tersebut. `IsPortfolioOwnerOrEditorOrReadOnly` mengizinkan pembacaan publik, pengelolaan penuh oleh superuser, dan PUT/PATCH oleh anggota Group `Editor`. Endpoint star memakai `IsAuthenticated`, sehingga semua akun login boleh memberi atau membatalkan star dengan identitas dari `request.user`.

   Menyembunyikan tombol hanya mengatur tampilan. Pengguna masih dapat mengirim request langsung melalui Console, Browsable API, atau klien lain. Karena itu permission diperiksa di server sebelum operasi tulis. Test penolakan memeriksa status 403 dan isi database agar terbukti data tidak berubah. Peran Editor berlaku pada Experience; permission Projects tetap hanya mengizinkan superuser mengelolanya.

4. **Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**

   Browser mengirim cookie session secara otomatis pada request yang sesuai. Situs lain dapat mencoba memanfaatkan perilaku ini untuk memicu tindakan dengan session pengguna. Karena itu POST, PUT, PATCH, dan DELETE melalui session tetap memerlukan perlindungan CSRF. Halaman Experience merender token CSRF meskipun pengguna tidak memperoleh form tambah, dan setiap fetch yang mengubah data menyertakan header `X-CSRFToken`.

   `force_authenticate` membantu memilih akun langsung dalam test permission, tetapi melewati proses autentikasi normal dan tidak membuktikan bahwa session serta pemeriksaan CSRF bekerja. Test tambahan memakai `APIClient(enforce_csrf_checks=True)` dan `.login()`: request tulis tanpa token ditolak, database tetap sama, lalu operasi dengan token yang diperoleh dari halaman nyata berhasil untuk peran yang diizinkan.

**AI Disclosure & Log Prompting (Tugas 6)**

* **Tools yang dipakai:** ChatGPT/Codex sebagai asisten pemrograman di IDE.
* **Log Prompting:** https://chatgpt.com/s/cx_6af1e599cd3881919920cf599a41909d
* **Strategi Prompting:** Saya memberikan konteks kode proyek dan PDF, lalu meminta AI melanjutkan implementasi dari hasil Tutorial 07. Saya juga meminta penjelasan mengenai hak Editor, perbedaan Group dengan Django Permission, pengujian, serta pembagian commit yang bertahap.

Pada tugas ini saya memilih halaman Experience dari portofolio saya untuk memenuhi instruksi Tugas 6.

* **Bagian spesifik yang dibantu AI:**
  1. Melengkapi serializer dan API Experience untuk pencarian, validasi, star, serta hak akses empat peran.
  2. Menghubungkan halaman Experience dan halaman edit lama ke API melalui fetch, dengan toast, CSRF, dan escaping.
  3. Menulis test API dan halaman, memeriksa hasilnya, menyusun draft jawaban reflektif, serta memberi panduan commit.

* **Kritik Keterbatasan AI & Penyesuaian yang Dilakukan:**
  * **Batas tutorial dan tugas:** Pada pengerjaan sebelumnya, AI sempat memperluas implementasi ketika saya masih berfokus pada Tutorial 07. Saya meminta tambahan tersebut dibatasi kembali. Untuk Tugas 6, cakupan implementasi dicocokkan dengan checklist pada PDF.
  * **Penyesuaian terhadap proyek:** Implementasi memakai model Experience, UUID, relasi `starred_by`, Group `Editor`, form, serta komponen toast yang sudah tersedia. Pengecekan grup dipertahankan karena proyek sebelumnya memakai Group, bukan pemeriksaan izin melalui `has_perm()`.
  * **Format data dan hak akses:** Rendering disesuaikan dari `item.pk`/`item.fields` menjadi objek JSON datar. Permission Experience mempertahankan hak update Editor, sedangkan pengelolaan Projects tetap hanya untuk superuser. Field star dihitung server dan tidak dapat dipalsukan melalui input klien.
  * **Batas pengujian otomatis:** Test memakai database pengujian terpisah dan mencakup session serta CSRF, bukan hanya `force_authenticate`. Hasil test otomatis tetap perlu dilengkapi pemeriksaan visual di browser dan smoke test deployment; hasil lokal tidak dianggap sebagai bukti bahwa semua interaksi PWS sudah teruji.
