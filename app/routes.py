from flask import render_template, url_for, jsonify, redirect, flash, request
from flask_login import current_user, logout_user, login_user, login_required

from app import app, db
from app.models import Pertanyaan, User, Room, Hasiltest, Roomsiswa
from app.forms import LoginForm, DaftarForm, BuatClassForm, JoinRoomForm


@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for("login"))
        flash("Login Berhasil")
        login_user(user)
        print("Berhasil")
        if user.status == "siswa":
            return redirect(url_for("test"))
        return redirect(url_for("akun"))
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/daftar", methods=["GET","POST"])
def daftar():
    form = DaftarForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        try:
            user = User(nip_nis=form.nip_nis.data, username=form.username.data,status=form.status.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            return redirect(url_for("daftar"))
    return render_template("daftar.html", form=form)

@app.route("/")
def index():
    return render_template("index.html", title="")


@app.route("/test", methods=["GET","POST"])
@login_required
def test():
    if current_user.hasil_test():
        return redirect(url_for('akun'))
    data = Pertanyaan.query.all()
    datastr = request.get_data()
    if datastr:
        datastr = datastr.decode('utf-8')
        visual = 0
        auditorial = 0
        kinestetik = 0
        # processed_data = {}
        for pair in datastr.split('&'):
            key, value = pair.split('=')
            if int(key[8:]) <= 10:
                if value == "yes":
                    visual += 1
            elif int(key[8:]) <= 20:
                if value == "yes":
                    auditorial += 1
            else:
                if value == "yes":
                    kinestetik += 1
        user = User.query.get(current_user.id)
        user.set_hasil_test(visual=visual,auditorial=auditorial,kinestetik=kinestetik)
        db.session.add(user)
        db.session.commit()
        print(f"Visual: {visual}")
        print(f"Auditorial: {auditorial}")
        print(f"Kinestetik: {kinestetik}")
            # processed_data[key] = value
        
        # for isi in processed_data:
        #     print(f"{isi[8:]}: {processed_data[isi]}")
    # db.session.rollback()
    return render_template("test.html", qs1=data[:10], qs2=data[10:20], qs3=data[20:], title="Tes Gaya Belajar")


@app.route("/akun", methods=["GET","POST"])
def akun():    
    if current_user.status == "guru":
        form = BuatClassForm()
        if form.validate_on_submit():
            print(form.kode_room.data)
            print(form.nama_room.data)
            room = Room(kode_room=form.kode_room.data, nama_room=form.nama_room.data,nip_nis=current_user.nip_nis)
            db.session.add(room)
            db.session.commit()
            return redirect(url_for('akun'))
        # room_dan_siswa = {}
        # room = Room.query.filter_by(nip_nis=current_user.nip_nis).all()
        # for isi in room:
        #     room_dan_siswa[isi.nama_room] = []
        #     allSiswa = User.query.filter_by(kode_room=isi.kode_room).all()
        #     for sw in allSiswa:
        #         room_dan_siswa[isi.nama_room].append(sw)
                
        # for siswa in room_dan_siswa:
        #     print(siswa)
        #     for isi in room_dan_siswa[siswa]:
        #         print(isi.username)
        #         print(isi.nip_nis)
        print(current_user.guru_room())
        for isi in current_user.guru_room():
            print(isi.siswa())
            for siswa in isi.siswa():
                print(siswa.siswa())
                sw = siswa.siswa().hasil_test()
                print(sw.visual)
                print(sw.auditorial)
                print(sw.kinestetik)
        return render_template("guru.html", room=current_user.guru_room(), form=form)
    else:
        form = JoinRoomForm()
        if form.validate_on_submit():
            cek = Roomsiswa.query.filter_by(nip_nis=current_user.nip_nis).first()
            if cek:
                flash(f"Anda telah terdaftar pada kelas {cek.nama_room}!")
                return redirect(url_for('akun'))
            room = Room.query.filter_by(kode_room=form.kode_room.data).first()
            if room is None:
                flash("Room tidak ditemukan!")
                return redirect(url_for('akun'))
            siswa = User.query.get(current_user.id)
            siswa.gabung_room(kode_room=room.kode_room)
            db.session.add(siswa)
            db.session.commit()
            return redirect(url_for('akun'))
        room = current_user.siswa_room()
        print(room)
        for isi in room:
            print(isi.room().nama_room)
        return render_template("siswa.html", room=room, form=form)
        

@app.route("/profile/<status>")
@login_required
def profile(status):
    if status == 'guru' and current_user.status == 'guru':
        return "Hello guru"
    else:
        return "Hello suswa"

@app.route("/api", methods=["POST"])
def postdata():
    data = request.get_data()
    if not data:
        return jsonify({"status":"Error","message":"tidak ada data"})
    print(type(data))
    print(dir(data))
    
    return jsonify({"status":"Success","message":"data diterima"})