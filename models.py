from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime
import bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ernest2210@localhost:5432/databuku'
db = SQLAlchemy(app)

# data_pinjaman = db.Table('data_pinjaman',
#     db.Column('id_pinjaman', db.Integer, db.ForeignKey('peminjaman.id_pinjaman'), primary_key=True),
# db.Column('id_buku', db.Integer, db.ForeignKey('buku.id_buku'), primary_key = True))

class Peminjaman(db.Model):
    id_pinjaman = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    id_buku = db.Column(db.Integer, db.ForeignKey('buku.id_buku'), nullable=False)
    tanggal_pinjam = db.Column(db.DateTime, default=datetime.date.today(), nullable=False)
    tanggal_kembali = db.Column(db.DateTime, nullable=False)
    petugas_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status_kembali = db.Column(db.Boolean, nullable=False, default=False)
    
    # member = relationship("Users", back_populates="peminjaman_member",foreign_keys='Peminjaman.user_id')
    # petugas = relationship("Users", back_populates="petugas",foreign_keys='Peminjaman.petugas_id')
    # daftar_buku = db.relationship('Buku', secondary=data_pinjaman, lazy='subquery',
    #     backref=db.backref('pinjaman', lazy=True))

class Users(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    
    # peminjaman_member = relationship("Users", back_populates="member",foreign_keys='Peminjaman.user_id')
    # petugas = relationship("Users", back_populates="petugas",foreign_keys='Peminjaman.petugas_id')
                
#Tabel
penulis_buku = db.Table('penulis_buku',
    db.Column('penulis_id', db.Integer, db.ForeignKey('penulis.penulis_id'), primary_key=True),
    db.Column('id_buku', db.Integer, db.ForeignKey('buku.id_buku'), primary_key=True))
class Buku(db.Model):
    __tablename__ = 'buku'
    
    id_buku = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judul_buku = db.Column(db.String(255), nullable=False)
    tahun_pencetakan = db.Column(db.Integer)
    jumlah_halaman = db.Column(db.Integer)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.kategori_id'), nullable=False)
    #Relationship
    daftar_penulis = db.relationship('Penulis', secondary=penulis_buku, lazy='subquery',
        backref=db.backref('daftar_buku', lazy=True))
    
    daftar_pinjaman = db.relationship('Peminjaman', backref='buku', lazy=True )
    
class Kategori(db.Model):
    kategori_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kategori = db.Column(db.String(50), nullable=False)
    deskripsi_kategori = db.Column(db.String(255))
    daftar_buku = db.relationship('Buku', backref='kategori', lazy=True )
    
    def __repr__(self):
        return f'Kategori Buku <{self.kategori}>'
    
class Penulis(db.Model):
    penulis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_penulis = db.Column(db.String(255), nullable=False)
    kewarganegaraan = db.Column(db.String(50), nullable=False)
    tahun_lahir = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'Nama Penulis <{self.nama_penulis}>'