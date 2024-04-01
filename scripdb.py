from app import db, app
# from app.models import Pertanyaan

# app.app_context().push()

data = {
    "visual": [
        "Jika mengerjakan soal atau tugas Bahasa Indonesia saya selalu membaca instruksinya terlebih dahulu",
        "Saya lebih suka membaca buku dan melihat gambar, daripada mendengar penjelasan orang lain",
        "Saya lebih mudah memahami pelajaran Bahasa Indonesia apabila saya membacanya dengan baik.",
        "Saya mengalami kesulitan mengingat dengan cara melihat daripada mendengar",
        "Saya lebih senang membaca dalam hati dengan cepat dan mudah memahami",
        "Saya memanfaakan waktu luang dengan membaca buku Bahasa Indonesia",
        "Gambar-gambar dan poster yang ada pada buku paket  Bahasa Indonesia sangat membantu saya dalam mengingat dan memahami pelajaran",
        "Saya lebih mudah mengingat cerita yang berisi banyak gambar dan berwarna dibandingkan dengan tanpa gambar",
        "Saya senang memberi tanda atau warna (stabilo) pada informasi-informasi penting yang ada di buku tukis atau paket Bahasa Indonesia",
        "Saya senang memperhatikan ilustrasi gambar atau warna yang terdapat dalam buku tulis atau buku paket Bahasa Indonesia."
    ],
    "auditorial":[
        "Saya mudah menerima informasi yang disampaikan secara langsung oleh guru",
        "Saya lebih senang mendengarkan penjelasan materi Bahasa Indonesia melalui video pembelajaran",
        "Saya senang membaca materi Bahasa Indonesia dengan suara keras dan mendengarkan sendiri",
        "Saya lebih mudah mengingat hafalan pelajaran dengan cara mendengarkan penjelasan guru",
        "Ketika sedang membaca materi Bahasa Indonesia, saya sering membaca dengan keras daripada membaca dalam hati",
        "Saat guru menjelaskan materi Bahasa Indonesia secara online, saya mengulanginya dengan berbicara dalam hati.",
        "Saya lebih senang membaca materi dibandingkan mencatat isi materi pelajaran Bahasa Indonesia",
        "Saya lebih mudah menghapal lagu dibandingkan dengan menghapal materi dibuku",
        "Saya senang mendengarkan penjelasan orang lain sebab membantu saya dalam memahami materi pelajaran.",
        "Pada saat liburan sekolah saya lebih senang mendengarkan musik daripada membaca buku"
    ],
    "kinestetik":[
        "Saya menyenangi belajar langsung praktek daripada belajar hanya mendengarkan penjelasan guru secara online",
        "Ketika belajar, tangan saya tidak bisa diam memainkan pulpen atau benda-benda lain yang ada didekat saya",
        "Saya mudah menghafal materi dengan cara berjalanjalan sambil mempraktikan secara langsung",
        "Saya dapat memahami pelajaran melalui bantuan penjelasan dari teman pada saat kerja kelompok dengan cara melihat gerakan tubuh atau fisik.",
        "Ketika diberikan tugas praktik di rumah saya langsung mengerjakannya",
        "Ketika ditanya oleh orang lain dengan cekatan, saya sering menjawab dengan isyarat tubuh seperti halnya mengangguk",
        "Ketika sedang tidak belajar saya lebih senang bermain dengan teman daripada duduk diam",
        "Ketika mengerjakan tugas online saya langsung mengerjakannya tanpa membaca instruksinya terlebih dahulu",
        "Saya tidak suka menjawab soal-soal yang ada di buku paket Bahasa Indonesia",
        "Belajar sambil mempraktikan secara langsung di rumah membuat saya lebih mudah memahami materi pelajaran"
    ]
}

if __name__=="__main__":
    for isi in data:
        role = isi
        print(isi, end=":\n")
        for isi2 in data[isi]:
            print(f"\t{isi2}")
            try:
                qs = Pertanyaan(role=isi, isi=isi2)
                db.session.add(qs)
                db.session.commit()
            except:
                print("Err")
                db.session.rollback()
                break
