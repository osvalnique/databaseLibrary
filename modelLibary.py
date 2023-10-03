# from flask import Flask, jsonify, request, abort
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import ForeignKey
# import datetime
# import bcrypt



# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ernest2210@localhost:5432/databuku'
# db = SQLAlchemy(app)

# # data_pinjaman = db.Table('data_pinjaman',
# #     db.Column('id_pinjaman', db.Integer, db.ForeignKey('peminjaman.id_pinjaman'), primary_key=True),
# # db.Column('id_buku', db.Integer, db.ForeignKey('buku.id_buku'), primary_key = True))

# class Peminjaman(db.Model):
#     id_pinjaman = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     id_buku = db.Column(db.Integer, db.ForeignKey('buku.id_buku'), nullable=False)
#     tanggal_pinjam = db.Column(db.DateTime, default=datetime.date.today(), nullable=False)
#     tanggal_kembali = db.Column(db.DateTime, nullable=False)
#     petugas_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     status_kembali = db.Column(db.Boolean, nullable=False, default=False)
    
#     # daftar_buku = db.relationship('Buku', secondary=data_pinjaman, lazy='subquery',
#     #     backref=db.backref('pinjaman', lazy=True))

# class Users(db.Model):
#     __tablename__ = 'users'
    
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(60), nullable=False)
#     admin = db.Column(db.Boolean, nullable=False, default=False)

# def auth():
#     data = request.authorization
#     if data != None:
#         username = data.parameters['username']
#         password = data.parameters['password']
        
#         print(username, password)
    
#         user = Users().query.filter_by(username=username).first()
#         # print(user)
#         if username == "" :
#             abort(401, 'Enter Username')
            
#         if password == "" :
#             abort(401, 'Enter Password')
        
#         if user != None:
#             is_match = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
#             if is_match == True:
#                 return user
#             else :
#                 abort(401, 'Password Incorrect')
                
# #Tabel
# penulis_buku = db.Table('penulis_buku',
#     db.Column('penulis_id', db.Integer, db.ForeignKey('penulis.penulis_id'), primary_key=True),
#     db.Column('id_buku', db.Integer, db.ForeignKey('buku.id_buku'), primary_key=True))
# class Buku(db.Model):
#     __tablename__ = 'buku'
    
#     id_buku = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     judul_buku = db.Column(db.String(255), nullable=False)
#     tahun_pencetakan = db.Column(db.Integer)
#     jumlah_halaman = db.Column(db.Integer)
#     kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.kategori_id'), nullable=False)
#     #Relationship
#     daftar_penulis = db.relationship('Penulis', secondary=penulis_buku, lazy='subquery',
#         backref=db.backref('daftar_buku', lazy=True))
    
#     daftar_pinjaman = db.relationship('Peminjaman', backref='buku', lazy=True )
    
# class Kategori(db.Model):
#     kategori_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     kategori = db.Column(db.String(50), nullable=False)
#     deskripsi_kategori = db.Column(db.String(255))
#     daftar_buku = db.relationship('Buku', backref='kategori', lazy=True )
    
#     def __repr__(self):
#         return f'Kategori Buku <{self.kategori}>'
    
# class Penulis(db.Model):
#     penulis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     nama_penulis = db.Column(db.String(255), nullable=False)
#     kewarganegaraan = db.Column(db.String(50), nullable=False)
#     tahun_lahir = db.Column(db.Integer, nullable=False)
    
#     def __repr__(self):
#         return f'Nama Penulis <{self.nama_penulis}>'
    
# with app.app_context():
#     db.create_all()
    
    
# #========================================CRUD API========================================#

# #API post Pinjaman
# @app.route('/pinjaman')
# def get_all_pinjaman():
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     return jsonify([
#         {'id_pinjaman': pinjaman.id_pinjaman,
#         'user_id' : pinjaman.user_id,
#         'judul_buku' : pinjaman.buku.judul_buku,
#         'id_buku' : pinjaman.id_buku,
#         'tanggal_pinjam' : pinjaman.tanggal_pinjam,
#         'tanggal_kembali' : pinjaman.tanggal_kembali,
#         'petugas_id' : pinjaman.petugas_id,
#         'status_kembali' : pinjaman.status_kembali}
#         for pinjaman in Peminjaman.query.all()
#         ])
                            
# @app.route('/pinjaman', methods=['POST'])
# def post_pinjaman():
#     users = auth()
#     print(users)
#     data = request.get_json()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     p = Peminjaman(
#         user_id = data['user_id'],
#         id_buku = data['id_buku'],
#         tanggal_kembali = data['tanggal_kembali'],
#         petugas_id = data['petugas_id']  
#     )
#     db.session.add(p)
#     db.session.commit()
#     return 'Pinjaman Berhasil'

# @app.route('/kembalikan_pinjaman/<int:id>', methods=['PUT'])
# def update_pinjaman(id):
#     users = auth()
    
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
#     peminjaman = Peminjaman.query.filter_by(id_pinjaman=id).first_or_404()
#     peminjaman.status_kembali =  True
    
#     db.session.commit()
#     return 'Buku Dikembalikan'
    
    
# #API get Users
# @app.route('/users')
# def get_users():
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     return jsonify([
#         {'user_id': user.user_id,
#          'username': user.username,
#          'password':user.password,
#          'admin' : user.admin}
#         for user in Users.query.all()
#         ])
    
# #API get Users by ID
# #API post Users
# @app.route('/users', methods=['POST'])
# def add_users():
#     data = request.get_json()
#     # users = auth()
#     # if users is None:
#     #     return "Access Denied", 401
    
#     data['password'] = str(data['password']).encode('utf-8')
#     hashed = bcrypt.hashpw(data['password'], bcrypt.gensalt())
#     hashed = hashed.decode('utf-8')
    
#     user = Users(
#         username = data['username'],
#         password = hashed,
#         admin = data['admin']
#     )
#     db.session.add(user)
#     db.session.commit()
#     return {'user' : 'Berhasil Ditambahkan'}

# #API put Users
# @app.route('/users/<int:id>', methods=['PUT'])
# def update_user(id):
#     user = auth()
#     data = request.get_json()
#     users = Users.query.filter_by(user_id=id).first_or_404()
#     if users is None:
#         return "Access Denied", 401
    
#     if users.username is not user.username:
#         print(users.username)
#         return 'Username is not Match'
    
#     if users.admin == False and data['admin'] == True:
#         return 'Only Admin is Allowed'
    
#     if users.username != data['username']:
#         check = Users.query.filter_by(username=data['username']).first()
#         if check != None:
#             return 'Username Sudah Dipakai', 400
        
#         users.username = data['username']
    
#     data['password'] = str(data['password']).encode('utf-8')
#     hashed = bcrypt.hashpw(data['password'], bcrypt.gensalt())
#     users.password = hashed

#     # users.admin = data['admin']
#     db.session.commit()
    
#     return jsonify([{'user_id': users.user_id,
#          'username': users.username,
#          'password':users.password,
#          'admin' : users.admin}
#     ])
    
# #API delete Users
# @app.route('/users/<int:id>', methods=['DELETE'])
# def delete_users(id):
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     data = Users.query.filter_by(user_id=id).first_or_404()
#     db.session.delete(data)
#     db.session.commit()
#     return {'user': 'Berhasil Dihapus'}
    
# #API get Tabel Buku    
# @app.route('/buku')
# def get_semua_buku():
#     if auth() == None:
#         return "Access Denied", 401

#     return jsonify([
#         {'id_buku' : book.id_buku,
#          'judul_buku' : book.judul_buku,
#          'tahun_pencetakan' : book.tahun_pencetakan,
#          'jumlah_halaman' : book.jumlah_halaman,
#          'kategori' : book.kategori,
#          'nama_penulis' : [penulis.nama_penulis for penulis in book.daftar_penulis]
#          } 
#         for book in Buku.query.all()
#         ])
    
# #API get Tabel Buku by ID
# @app.route('/buku/<int:id>')
# def get_buku_id(id):
#     if auth() == None:
#         return "Access Denied", 401
    
#     book = Buku.query.filter_by(id_buku=id).first()
#     return jsonify({
#         'id_buku' : book.id_buku,
#          'judul_buku' : book.judul_buku,
#          'tahun_pencetakan' : book.tahun_pencetakan,
#          'jumlah_halaman' : book.jumlah_halaman,
#          'kategori' : book.kategori.kategori,
#          'nama_penulis' : [penulis.nama_penulis for penulis in book.daftar_penulis]
#          })

# #API get Tabel Kategori
# @app.route('/kategori')
# def get_all_kategori():
#     if auth() == None:
#         return "Access Denied", 401
    
#     return jsonify([
# 		{'id_kategori' : kategori.kategori_id,
#    'kategori' : kategori.kategori,
#    'deskripsi_kategori' : kategori.deskripsi_kategori
#    } 
#   for kategori in Kategori.query.all()
# 	])

# #API get Tabel Kategori by ID    
# @app.route('/kategori/<int:id>')
# def get_kategori(id):
#     if auth() == None:
#         return "Access Denied", 401
    
#     kategori = Kategori.query.filter_by(kategori_id=id).first_or_404()
    
#     return {'id_kategori' : kategori.kategori_id,
#    'kategori' : kategori.kategori,
#    'deskripsi_kategori' : kategori.deskripsi_kategori
#    }

# #API get Tabel Penulis
# @app.route('/penulis')    
# def get_all_penulis():
#     if auth() == None:
#         return "Access Denied", 401
    
#     return jsonify([
#         {'id_penulis' : author.penulis_id,
#     'nama_penulis' : author.nama_penulis,
#     'kewarganegaraan' : author.kewarganegaraan,
#     'tahun_lahir' : author.tahun_lahir
#     }
#     for author in Penulis.query.all()
#     ])
    
# #API get Tabel Penulis by ID
# @app.route('/penulis/<int:id>')
# def get_penulis(id):
#     if auth() == None:
#         return "Access Denied", 401
    
#     author = Penulis.query.filter_by(penulis_id=id).first_or_404()
    
#     return {'id_penulis' : author.penulis_id,
#     'nama_penulis' : author.nama_penulis,
#     'kewarganegaraan' : author.kewarganegaraan,
#     'tahun_lahir' : author.tahun_lahir
#     }
    
# #API post Tabel Buku
# @app.route('/buku', methods=['POST'])
# def tambah_buku():
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     data = request.get_json()
#     error = []
#     if not 'judul_buku' in data:
#         error.append('Judul Buku')
#     if not 'tahun_pencetakan' in data:
#         error.append('Tahun Pencetakan')
#     if not 'jumlah_halaman' in data:
#         error.append('Jumlah Halaman')
#     if not 'kategori_id' in data:
#         error.append('Kategori Id')
#     if not 'penulis' in data:
#         error.append('Id Penulis')
        
#     if len(error)> 0:
#         return jsonify({'error': f'Masukkan {error}'}), 400
	
#     b = Buku(
# 	        judul_buku = data['judul_buku'],
#             tahun_pencetakan = data['tahun_pencetakan'],
#             jumlah_halaman = data['jumlah_halaman'],
#             kategori_id = data['kategori_id'],
# 		)
#     db.session.add(b)
#     for id in data['penulis']:
#         p = Penulis().query.filter_by(penulis_id=id).first()
#         if p == None:
#             return jsonify({'error' : f'Penulis id {id} tidak terdaftar'}), 400
#         b.daftar_penulis.append(p)
   
#     # db.session.commit()
#     return {
#      'judul_buku': b.judul_buku,
#      'tahun_pencetakan': b.tahun_pencetakan, 
#      'jumlah_halaman': b.jumlah_halaman,
#      'kategori_id' : b.kategori_id,
#      'penulis' : [p.nama_penulis for p in b.daftar_penulis]
# 	}, 201
  
# #API post Tabel Kategori
# @app.route('/kategori', methods=['POST'])
# def tambah_kategori():
#     data = request.get_json()
#     error = []
#     if not 'kategori' in data:
#         error.append('Kategori')
#     if not 'deskripsi_kategori' in data:
#         error.append('Deskripsi')
        
#     k = Kategori(
#         kategori = data['kategori'],
#         deskripsi_kategori = data['deskripsi_kategori']
#     )
#     db.session.add(k)
#     db.session.commit()
#     return {
#     'kategori' : k.kategori,
#     'deskripsi_kategori' : k.deskripsi_kategori
#     }, 201
  
# #API post Tabel Penulis    
# @app.route('/penulis', methods=['POST'])
# def tambah_penulis():
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     data = request.get_json()
#     error = []
#     if not 'nama_penulis' in data:
#         error.append('Nama Penulis')
#     if not 'kewarganegaraan' in data:
#         error.append('Kewarganegaraan')
#     if not 'tahun_lahir' in data:
#         error.append('Tahun Lahir')

#     if len(error)> 0:
#         return jsonify({'error': f'Masukkan {error}'}), 400
    
#     p = Penulis(
#     nama_penulis = data['nama_penulis'],
#     kewarganegaraan = data['kewarganegaraan'],
#     tahun_lahir = data['tahun_lahir']
# 		)
#     db.session.add(p)
#     # db.session.commit()
#     return {
#      'nama_penulis' : p.nama_penulis,
#      'kewarganegaraan' : p.kewarganegaraan,
#      'tahun_lahir' : p.tahun_lahir
# 	}, 201

# #API put data Buku
# @app.route('/buku/<int:id>', methods=['PUT'])

# def update_buku(id):
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     data = request.get_json()
#     book = Buku.query.filter_by(id_buku=id).first()
#     book.judul_buku = data['judul_buku']
#     book.tahun_pencetakan = data['tahun_pencetakan']
#     book.jumlah_halaman = data['jumlah_halaman']
#     book.kategori_id = data['kategori_id']
#     book.daftar_penulis =  data['daftar_penulis']
#     db.session.commit()
#     return jsonify({
#      'judul_buku': book.judul_buku,
#      'tahun_pencetakan': book.tahun_pencetakan, 
#      'jumlah_halaman': book.jumlah_halaman,
#      'kategori' : book.kategori.kategori,
#      'nama_penulis' : [b.nama_penulis for b in book.daftar_penulis]
# 	})
    
# #API put data Kategori
# @app.route('/kategori/<int:id>', methods=['PUT'])
# def update_kategori(id):
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
#     data = request.get_json()
  
#     kategori = Kategori.query.filter(id_kategori=id).first()
#     kategori.id_kategori : data['id_kategori']
#     kategori.kategori : data['kategori']
#     kategori.deskripsi_kategori : data['deskripsi_kategori']
    
# #API put data Penulis
# @app.route('/penulis/<int:id>', methods=['PUT'])
# def update_penulis(id):
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
#     data = request.get_json()
#     penulis = Penulis.query.filter_by(id_penulis=id).first()
#     penulis.id_penulis = data['penulis_id']
#     penulis.nama_penulis = data['nama_penulis']
#     penulis.kewarganegaraan = data['kewarganegaraan']
#     penulis.tahun_lahir = data['tahun_lahir']
            
# #API delete data Buku
# @app.route('/buku/<int:id>', methods=['DELETE'])
# def hapus_buku(id):
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     book = Buku.query.filter_by(id_buku=id).first_or_404()
#     db.session.delete(book)
#     # db.session.commit()
#     return {'Success': 'Book deleted successfully'}

# #API delete data Kategori
# @app.route('/kategori/<int:id>', methods=['DELETE'])
# def hapus_kategori(id):
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
    
#     if users.admin == False:
#         return 'Only Admin is Allowed'
    
#     kategori = Kategori.query.filter_by(kategori_id=id).first_or_404()
#     db.session.delete(kategori)
#     # db.session.commit()
#     return {'Success': 'Category deleted successfully'}

# #API delete data Penulis
# @app.route('/penulis/<int:id>', methods=['DELETE'])
# def hapus_penulis(id):
#     users = auth()
#     if users is None:
#         return "Access Denied", 401
#     if users.admin == False:
#         return 'Only Admin is Allowed'
        
#     penulis = Penulis.query.filter_by(penulis_id=id).first_or_404()
#     db.session.delete(penulis)
#     # db.session.commit()
#     return {'Success': 'Author deleted successfully'}
    
# def main():
#     app.run(debug=True)

# main()