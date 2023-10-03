from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from authorization import auth
from models import Kategori, db
from route import blueprint

#API get Tabel Kategori
@blueprint.route('/kategori')
def get_all_kategori():
    if auth() == None:
        return "Access Denied", 401
    
    return jsonify([
		{'id_kategori' : kategori.kategori_id,
   'kategori' : kategori.kategori,
   'deskripsi_kategori' : kategori.deskripsi_kategori
   } 
  for kategori in Kategori.query.all()
	])

#API get Tabel Kategori by ID    
@blueprint.route('/kategori/<int:id>')
def get_kategori(id):
    if auth() == None:
        return "Access Denied", 401
    
    kategori = Kategori.query.filter_by(kategori_id=id).first_or_404()
    
    return {'id_kategori' : kategori.kategori_id,
   'kategori' : kategori.kategori,
   'deskripsi_kategori' : kategori.deskripsi_kategori
   }

#API post Tabel Kategori
@blueprint.route('/kategori', methods=['POST'])
def tambah_kategori():
    data = request.get_json()
    error = []
    if not 'kategori' in data:
        error.append('Kategori')
    if not 'deskripsi_kategori' in data:
        error.append('Deskripsi')
        
    k = Kategori(
        kategori = data['kategori'],
        deskripsi_kategori = data['deskripsi_kategori']
    )
    db.session.add(k)
    db.session.commit()
    return {
    'kategori' : k.kategori,
    'deskripsi_kategori' : k.deskripsi_kategori
    }, 201
    
#API put data Kategori
@blueprint.route('/kategori/<int:id>', methods=['PUT'])
def update_kategori(id):
    users = auth()
    if users is None:
        return "Access Denied", 401
    if users.admin == False:
        return 'Only Admin is Allowed'
    data = request.get_json()
  
    kategori = Kategori.query.filter(id_kategori=id).first()
    kategori.id_kategori : data['id_kategori']
    kategori.kategori : data['kategori']
    kategori.deskripsi_kategori : data['deskripsi_kategori']
    

#API delete data Kategori
@blueprint.route('/kategori/<int:id>', methods=['DELETE'])
def hapus_kategori(id):
    users = auth()
    if users is None:
        return "Access Denied", 401
    
    if users.admin == False:
        return 'Only Admin is Allowed'
    
    kategori = Kategori.query.filter_by(kategori_id=id).first_or_404()
    db.session.delete(kategori)
    # db.session.commit()
    return {'Success': 'Category deleted successfully'}

