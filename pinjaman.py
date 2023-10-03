from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from authorization import auth
from models import Peminjaman, db
from route import blueprint


#API post Pinjaman
@blueprint.route('/pinjaman')
def get_all_pinjaman():
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    return jsonify([
        {'id_pinjaman': pinjaman.id_pinjaman,
        'user_id' : pinjaman.user_id,
        'judul_buku' : pinjaman.buku.judul_buku,
        'id_buku' : pinjaman.id_buku,
        'tanggal_pinjam' : pinjaman.tanggal_pinjam,
        'tanggal_kembali' : pinjaman.tanggal_kembali,
        'petugas' : pinjaman.petugas_id,
        'status_kembali' : pinjaman.status_kembali}
        for pinjaman in Peminjaman.query.all()
        ])
                            
@blueprint.route('/pinjaman', methods=['POST'])
def post_pinjaman():
    users = auth()
    print(users)
    data = request.get_json()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    p = Peminjaman(
        user_id = data['user_id'],
        id_buku = data['id_buku'],
        tanggal_kembali = data['tanggal_kembali'],
        petugas_id = data['petugas_id']  
    )
    db.session.add(p)
    db.session.commit()
    return 'Pinjaman Berhasil'

@blueprint.route('/kembalikan_pinjaman/<int:id>', methods=['PUT'])
def update_pinjaman(id):
    users = auth()
    
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    peminjaman = Peminjaman.query.filter_by(id_pinjaman=id).first_or_404()
    peminjaman.status_kembali =  True
    
    db.session.commit()
    return 'Buku Dikembalikan'