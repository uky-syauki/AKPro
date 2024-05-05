from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, TextAreaField


class DaftarForm(FlaskForm):
    nip_nis = StringField("NIP atau NIS")
    status = RadioField('Options', choices=[('guru', 'Guru'), ('siswa', 'Siswa')])
    username = StringField("Nama Pengguna")
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo('ulang_password', message='Password harus sama')
    ])
    ulang_password = PasswordField("Ulang Password")
    daftar = SubmitField("Daftar")


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    login = SubmitField("Login")
    
    
class BuatClassForm(FlaskForm):
    kode_room = StringField("Kode Room")
    nama_room = StringField("Nama Room")
    buat = SubmitField("Buat")


class JoinRoomForm(FlaskForm):
    kode_room = StringField("Kode Room")
    gabung = SubmitField("Gabung Room")
    


class EditSoalForm(FlaskForm):
    id = StringField("Soal ke", default="tes")
    soal = TextAreaField("Pertanyaan", default="")
    update = SubmitField("Update")
    
