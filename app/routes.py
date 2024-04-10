from flask import render_template, url_for, jsonify, redirect, flash, request
from flask_login import current_user, logout_user, login_user, login_required

from app import app, db
from app.models import Pertanyaan, User, Room, Hasiltest, Roomsiswa
from app.forms import LoginForm, DaftarForm, BuatClassForm, JoinRoomForm, EditSoalForm


@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Username atau Password Salah", "danger")
            return redirect(url_for("login"))
        flash("Login Berhasil","success")
        login_user(user)
        print("user status=",user.status)
        if user.status == "admin":
            return redirect(url_for("edit_soal"))
        if user.status == "siswa" and not Hasiltest.query.filter_by(nip_nis=current_user.nip_nis).first():
            return redirect(url_for("test"))
        return redirect(url_for("akun"))
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/daftar", methods=["GET","POST"])
def daftar():
    form = DaftarForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        cek = User.query.filter_by(nip_nis=form.nip_nis.data).first()
        if cek:
            flash(f"Maaf nip atau nis telah terdaftar oleh pengguna: {cek.username}", "warning")
            return redirect(url_for('daftar'))
        try:
            user = User(nip_nis=form.nip_nis.data, username=form.username.data,status=form.status.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Berhasil mendaftar, silahkan Login","success")
            return redirect(url_for('login'))
        except:
            flash("Terjadi kesalahan, periksa inputan","danger")
            db.session.rollback()
            return redirect(url_for("daftar"))
    return render_template("daftar.html", form=form)


@app.route("/")
def index():
    return render_template("index.html", title="")


@app.route("/test", methods=["GET","POST"])
@login_required
def test():
    # if current_user.hasil_test():
    #     return redirect(url_for('akun'))
    data = Pertanyaan.query.all()
    datastr = request.get_data()
    if datastr:
        datastr = datastr.decode('utf-8')
        visual = 0
        auditorial = 0
        kinestetik = 0
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
        # if visual and auditorial and kinestetik:
        #     flash("Anda tidak mengisih test dengan benar","danger")
        #     return redirect(url_for("test"))
        user = User.query.get(current_user.id)
        user.set_hasil_test(visual=visual,auditorial=auditorial,kinestetik=kinestetik)
        try:
            db.session.add(user)
            db.session.commit()
            flash("Berhasil melakukan Tes Gaya Belajar","info")
        except:
            db.session.rollback()
            flash("Terjadi kesalahan","danger")
        return redirect(url_for('akun'))
    return render_template("test.html", qs1=data[:10], qs2=data[10:20], qs3=data[20:], title="Tes Gaya Belajar")


@app.route("/akun", methods=["GET","POST"])
@login_required
def akun():    
    if current_user.status == "guru":
        form = BuatClassForm()
        if form.validate_on_submit():
            cek = Room.query.filter_by(kode_room=form.kode_room.data).first()
            if cek:
                flash(f"Kode Class {form.kode_room.data} sudah digunakan", "danger")
                return redirect(url_for("akun"))
            panjang = len(form.kode_room.data)
            if panjang <= 0 or panjang > 10:
                flash("Kode Room tidak boleh kosong atau memiliki lebih dari 10 karakter","danger")
                return redirect(url_for('akun'))
            room = Room(kode_room=form.kode_room.data, nama_room=form.nama_room.data,nip_nis=current_user.nip_nis)
            try:
                db.session.add(room)
                db.session.commit()
                flash(f"Room {form.nama_room.data} berhasil di buat!","success")
            except:
                db.session.rollback()
                flash("Terjadi kesalahan","danger")
            return redirect(url_for('akun'))
        return render_template("guru.html", room=current_user.guru_room(), form=form)
    else:
        form = JoinRoomForm()
        if form.validate_on_submit():
            cek = Roomsiswa.query.filter_by(nip_nis=current_user.nip_nis, kode_room=form.kode_room.data).first()
            if cek:
                flash(f"Anda telah terdaftar pada kelas {cek.room().nama_room}!","warning")
                return redirect(url_for('akun'))
            room = Room.query.filter_by(kode_room=form.kode_room.data).first()
            if room is None:
                flash("Room tidak ditemukan!","warning")
                return redirect(url_for('akun'))
            siswa = User.query.get(current_user.id)
            siswa.gabung_room(kode_room=room.kode_room)
            try:
                db.session.add(siswa)
                db.session.commit()
                flash(f"Berhasil terdaftar pada Room {room.nama_room}","success")
            except:
                db.session.rollback()
                flash("Terjadi kesalahan","danger")
            return redirect(url_for('akun'))
        room = current_user.siswa_room()
        print(room)
        for isi in room:
            print(isi.room().nama_room)
            print(isi.hasil_test())
        return render_template("siswa.html", room=room, form=form)


@app.route("/latihan-visual")
def latihan_visual():
    return render_template("latihanVisual.html", title="Latihan Gaya Belajar Visual")

@app.route("/latihan-auditorial")
def latihan_auditorial():
    return render_template("latihanAuditorial.html", title="Latihan Gaya Belajar Visual")        

@app.route("/latihan-kinestetik")
def latihan_kinestetik():
    return render_template("latihanKinestetik.html", title="Latihan Gaya Belajar Visual")
        

@app.route("/edit-soal", methods=["GET","POST"])
@login_required
def edit_soal():
    form = EditSoalForm()
    pertanyaan = Pertanyaan.query.all()
    return render_template("edit_soal.html", title="Edit Soal", pertanyaan=pertanyaan)
        

@app.route("/profile/<status>")
@login_required
def profile(status):
    if status == 'guru' and current_user.status == 'guru':
        return "Hello guru"
    else:
        return "Hello suswa"
    

@app.route("/api", methods=["GET","POST"])
@login_required
def postdata():
    try:
        data = request.json
        pertanyaan = Pertanyaan.query.get(int(data['id']))
        pertanyaan.isi = data['text']
        db.session.add(pertanyaan)
        db.session.commit()
        print(data['id'])
        return jsonify({"status":"Success","message":"data diterima"})
    except:
        db.session.rollback()
        return jsonify({"status":"Error","message":"Terjadi kesalahan!"})