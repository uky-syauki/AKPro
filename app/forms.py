from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField


class DaftarForm(FlaskForm):
    nip_nis = StringField("NIP atau NIS")
    # status = StringField("Status")
    status = RadioField('Options', choices=[('guru', 'Guru'), ('siswa', 'Siswa')])
    username = StringField("Nama Pengguna")
    password = PasswordField("Password")
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
    