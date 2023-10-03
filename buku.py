from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from authorization import auth
from models import Buku, Penulis, Kategori, db
from route import blueprint

#API get Tabel Buku    
@blueprint.route('/buku')
def get_semua_buku():
    if auth() == None:
        return "Access Denied", 401
    return jsonify([
        {'id_buku' : book.id_buku,
         'judul_buku' : book.judul_buku,
         'tahun_pencetakan' : book.tahun_pencetakan,
         'jumlah_halaman' : book.jumlah_halaman,
         'kategori' : book.kategori.kategori,
         'nama_penulis' : [penulis.nama_penulis for penulis in book.daftar_penulis]
         } 
        for book in Buku.query.all()
        ])
    
#API get Tabel Buku by ID
@blueprint.route('/buku/<int:id>')
def get_buku_id(id):
    if auth() == None:
        return "Access Denied", 401
    
    book = Buku.query.filter_by(id_buku=id).first()
    return jsonify({
        'id_buku' : book.id_buku,
         'judul_buku' : book.judul_buku,
         'tahun_pencetakan' : book.tahun_pencetakan,
         'jumlah_halaman' : book.jumlah_halaman,
         'kategori' : book.kategori.kategori,
         'nama_penulis' : [penulis.nama_penulis for penulis in book.daftar_penulis]
         })
    
#API post Tabel Buku
@blueprint.route('/buku', methods=['POST'])
def tambah_buku():
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    data = request.get_json()
    error = []
    if not 'judul_buku' in data:
        error.append('Judul Buku')
    if not 'tahun_pencetakan' in data:
        error.append('Tahun Pencetakan')
    if not 'jumlah_halaman' in data:
        error.append('Jumlah Halaman')
    if not 'kategori_id' in data:
        error.append('Kategori Id')
    if not 'penulis' in data:
        error.append('Id Penulis')
        
    if len(error)> 0:
        return jsonify({'error': f'Masukkan {error}'}), 400
	
    b = Buku(
	        judul_buku = data['judul_buku'],
            tahun_pencetakan = data['tahun_pencetakan'],
            jumlah_halaman = data['jumlah_halaman'],
            kategori_id = data['kategori_id'],
		)
    db.session.add(b)
    for id in data['penulis']:
        p = Penulis().query.filter_by(penulis_id=id).first()
        if p == None:
            return jsonify({'error' : f'Penulis id {id} tidak terdaftar'}), 400
        b.daftar_penulis.append(p)
   
    # db.session.commit()
    return {
     'judul_buku': b.judul_buku,
     'tahun_pencetakan': b.tahun_pencetakan, 
     'jumlah_halaman': b.jumlah_halaman,
     'kategori_id' : b.kategori_id,
     'penulis' : [p.nama_penulis for p in b.daftar_penulis]
	}, 201

#API put data Buku
@blueprint.route('/buku/<int:id>', methods=['PUT'])
def update_buku(id):
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    data = request.get_json()
    book = Buku.query.filter_by(id_buku=id).first()
    book.judul_buku = data['judul_buku']
    book.tahun_pencetakan = data['tahun_pencetakan']
    book.jumlah_halaman = data['jumlah_halaman']
    book.kategori_id = data['kategori_id']
    book.daftar_penulis =  data['daftar_penulis']
    db.session.commit()
    return jsonify({
     'judul_buku': book.judul_buku,
     'tahun_pencetakan': book.tahun_pencetakan, 
     'jumlah_halaman': book.jumlah_halaman,
     'kategori' : book.kategori.kategori,
     'nama_penulis' : [b.nama_penulis for b in book.daftar_penulis]
	})

#API delete data Buku
@blueprint.route('/buku/<int:id>', methods=['DELETE'])
def hapus_buku(id):
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    book = Buku.query.filter_by(id_buku=id).first_or_404()
    db.session.delete(book)
    # db.session.commit()
    return {'Success': 'Book deleted successfully'}
