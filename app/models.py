from app import db

class Pertanyaan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(15))
    isi = db.Column(db.String(200))
    def __repr__(self):
        return f"<ID {self.id}>"