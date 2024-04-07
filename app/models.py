from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(10)) # siswa / guru / admin
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(130))
    kode_room = db.Column(db.String(10))
    nip_nis = db.Column(db.String(15), unique=True)
    def guru_room(self):
        hasil = Room.query.filter_by(nip_nis=self.nip_nis).all()
        return hasil
    def siswa_room(self):
        hasil = Roomsiswa.query.filter_by(nip_nis=self.nip_nis).all()
        return hasil
    def set_hasil_test(self, visual, auditorial, kinestetik):
        hasil = Hasiltest(nip_nis=self.nip_nis, visual=visual,auditorial=auditorial,kinestetik=kinestetik)
        db.session.add(hasil)
        db.session.commit()
    def hasil_test(self):
        hasil = Hasiltest.query.filter_by(nip_nis=self.nip_nis).first()
        # hitung = self.hitung_hasil(hasil.visual,hasil.auditorial, hasil.kinestetik)
        # hasil.visual = hitung[0]
        # hasil.auditorial = hitung[1]
        # hasil.kinestetik = hitung[2]
        return hasil
    def buat_room(self, kode_room, nama_room):
        broom = Room(kode_room=kode_room, nip_nis=self.nip_nis, nama_room=nama_room)
        db.session.add(broom)
        db.session.commit()
    def gabung_room(self,kode_room):
        gabung = Roomsiswa(kode_room=kode_room,nip_nis=self.nip_nis)
        db.session.add(gabung)
        db.session.commit()
    def set_password(self, passwd):
        self.password_hash = generate_password_hash(passwd)
    def hitung_hasil(self):
        hasil = Hasiltest.query.filter_by(nip_nis=self.nip_nis).first()
        n1 = hasil.visual + 1; n2 = hasil.auditorial + 1; n3 = hasil.kinestetik + 1
        hasil = [round(n1/(n1+n2+n3)*100),round(n2/(n1+n2+n3)*100),round(n3/(n1+n2+n3)*100)]
        if sum(hasil) < 100:
            hasil[-1] += 1
        print(hasil, sum(hasil), self.username)
        return hasil
    def check_password(self, passwd):
        return check_password_hash(self.password_hash, passwd)
    def __repr__(self):
        return f"<User {self.username}>"
    
# uki pi@10@20


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kode_room = db.Column(db.String(10), unique=True)
    nip_nis = db.Column(db.String(15))
    nama_room = db.Column(db.String(50))
    def siswa(self):
        return Roomsiswa.query.filter_by(kode_room=self.kode_room).all()
    def __repr__(self):
        return f"<Room {self.kode_room}>"
    

class Pertanyaan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(15))
    isi = db.Column(db.String(200))
    def __repr__(self):
        return f"<ID {self.id}>"
    
    
class Roomsiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kode_room = db.Column(db.String(10))
    nip_nis = db.Column(db.String(15))
    def hitung_hasil(self):
        hasil = Hasiltest.query.filter_by(nip_nis=self.nip_nis).first()
        n1 = hasil.visual + 1; n2 = hasil.auditorial + 1; n3 = hasil.kinestetik + 1
        hasil = [round(n1/(n1+n2+n3)*100),round(n2/(n1+n2+n3)*100),round(n3/(n1+n2+n3)*100)]
        if sum(hasil) < 100:
            hasil[-1] += 1
        return hasil
    def room(self):
        return Room.query.filter_by(kode_room=self.kode_room).first()
    def hasil_test(self):
        return Hasiltest.query.filter_by(nip_nis=self.nip_nis).first()
    def siswa(self):
        return User.query.filter_by(nip_nis=self.nip_nis).first()
    def __repr__(self):
        return f"Roomsiswa <{self.kode_room}>"

    
class Hasiltest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nip_nis = db.Column(db.String(15))
    visual = db.Column(db.Integer)
    auditorial = db.Column(db.Integer)
    kinestetik = db.Column(db.Integer)
    def siswa(self):
        return User.query.filter_by(nip_nis=self.nip_nis).first()
    def __repr__(self):
        return f"<Hasiltest {self.nip_nis}>"

