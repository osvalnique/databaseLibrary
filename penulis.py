from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from authorization import auth
from models import Penulis, db
from route import blueprint

#API get Tabel Penulis
@blueprint.route('/penulis')    
def get_all_penulis():
    if auth() == None:
        return "Access Denied", 401
    
    return jsonify([
        {'id_penulis' : author.penulis_id,
    'nama_penulis' : author.nama_penulis,
    'kewarganegaraan' : author.kewarganegaraan,
    'tahun_lahir' : author.tahun_lahir
    }
    for author in Penulis.query.all()
    ])
    
#API get Tabel Penulis by ID
@blueprint.route('/penulis/<int:id>')
def get_penulis(id):
    if auth() == None:
        return "Access Denied", 401
    
    author = Penulis.query.filter_by(penulis_id=id).first_or_404()
    
    return {'id_penulis' : author.penulis_id,
    'nama_penulis' : author.nama_penulis,
    'kewarganegaraan' : author.kewarganegaraan,
    'tahun_lahir' : author.tahun_lahir
    }
    
#API post Tabel Penulis    
@blueprint.route('/penulis', methods=['POST'])
def tambah_penulis():
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    data = request.get_json()
    error = []
    if not 'nama_penulis' in data:
        error.append('Nama Penulis')
    if not 'kewarganegaraan' in data:
        error.append('Kewarganegaraan')
    if not 'tahun_lahir' in data:
        error.append('Tahun Lahir')

    if len(error)> 0:
        return jsonify({'error': f'Masukkan {error}'}), 400
    
    p = Penulis(
    nama_penulis = data['nama_penulis'],
    kewarganegaraan = data['kewarganegaraan'],
    tahun_lahir = data['tahun_lahir']
		)
    db.session.add(p)
    # db.session.commit()
    return {
     'nama_penulis' : p.nama_penulis,
     'kewarganegaraan' : p.kewarganegaraan,
     'tahun_lahir' : p.tahun_lahir
	}, 201

#API put data Penulis
@blueprint.route('/penulis/<int:id>', methods=['PUT'])
def update_penulis(id):
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    data = request.get_json()
    penulis = Penulis.query.filter_by(id_penulis=id).first()
    penulis.id_penulis = data['penulis_id']
    penulis.nama_penulis = data['nama_penulis']
    penulis.kewarganegaraan = data['kewarganegaraan']
    penulis.tahun_lahir = data['tahun_lahir']
    
    # db.session.commit()
    
#API delete data Penulis
@blueprint.route('/penulis/<int:id>', methods=['DELETE'])
def hapus_penulis(id):
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
        
    penulis = Penulis.query.filter_by(penulis_id=id).first_or_404()
    db.session.delete(penulis)
    # db.session.commit()
    return {'Success': 'Author deleted successfully'}
    
            