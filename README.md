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

Modifikasi Grid Bento Box untuk Academic Milestones: AI awalnya menyarankan pembagian rasio kolom 1.5fr 1fr. Setelah saya evaluasi, saya mengubahnya secara manual menjadi 1.8fr 1fr agar kotak utama memiliki ruang yang lebih lega, sehingga teks deskripsi jurusan saya tidak berantakan memanjang ke bawah.

Merapikan Proporsi Logo di Timeline pada bagian Experience: Kode dari AI membatasi ukuran logo organisasi hanya 70% dan mengurungnya dengan garis tepi (border), yang membuat logo terpotong saat terkena animasi hover zoom. Saya memperbaiki CSS-nya mandiri dengan menghapus border dan memaksimalkan proporsi menjadi width: 100%; height: 100%; object-fit: cover;. Hasilnya, logo berlatar belakang (seperti logo UI atau BETIS) bisa menyebar penuh dan pas di dalam lingkaran timeline.

Menyambungkan Menu Navigasi: AI membuatkan kerangka `<section id="experience">` di struktur bawah, tetapi lupa menyambungkannya ke menu atas. Saya harus menyisipkan elemen `<a href="#experience">` secara manual di dalam tag `<nav>` agar navigasi scroll halamannya bisa berfungsi.

Menyesuaikan Aset & Konten Asli: AI menulis jalur direktori gambar (path) yang salah sehingga memicu broken image. Saya merapikan struktur folder lokal secara manual, sekaligus merombak total teks dummy bawaan AI menggunakan data asli saya (nilai IELTS Band 7, medali SASMO, serta deskripsi kepanitiaan DDP0 , KMK Fasilkom, BETIS, dan IGI CompFest).

Penyesuaian Animasi Layar Sentuh (Mobile/Hp): AI memberikan efek animasi `:hover` yang bekerja baik di desktop dengan kursor, namun menimbulkan *glitch* visual dan membuat logo terpotong saat disentuh di layar HP. Saya secara manual mematikan efek `transform` dan menambahkan `object-fit: contain` khusus pada `@media (max-width: 600px)` agar logo statis, proporsional, dan warnanya langsung terlihat utuh tanpa perlu interaksi layar sentuh.