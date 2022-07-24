# from re import U
from application import db, bcrypt



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id_usr',db.BigInteger, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.Text)
    level_user = db.Column(db.String(10))

    def __init__(self, username, password, level_user):
        self.username = username
        if password != '':
            self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.level_user = level_user

class Peserta(db.Model):
    __tablename__ = 'peserta'
    id = db.Column('id_peserta', db.BigInteger)
    kode = db.Column(db.BigInteger, nullable=False, primary_key=True)
    nama = db.Column(db.String(150), nullable=False)
    jk = db.Column(db.String(10))
    kelas = db.Column(db.String(10))
    jurusan = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.Text)
    level_user = db.Column(db.String(10))
    db.relationship('Laporan', backref=db.backref('peserta', lazy=True))
    db.relationship('Hasil', backref=db.backref('peserta', lazy=True))

    def __init__(self, kode, nama, jk, kelas, jurusan, email, password, level_user):
        self.kode = kode
        self.nama = nama
        self.jk = jk
        self.kelas = kelas
        self.jurusan = jurusan
        self.email = email
        if password != '':
            self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.level_user = level_user

class Petugas(db.Model):
    __tablename__ = 'petugas'
    id = db.Column('id_petugas', db.BigInteger, auto_increment=True)
    kode = db.Column(db.BigInteger, nullable=False, primary_key=True)
    nama = db.Column(db.String(150), nullable=False)
    jk = db.Column(db.String(10))
    email = db.Column(db.String(100))
    alamat = db.Column(db.Text)
    password = db.Column(db.Text)
    level_user = db.Column(db.String(10))

    def __init__(self, kode, nama, jk, email, alamat, password, level_user):
        self.kode = kode
        self.nama = nama
        self.jk = jk
        self.email = email
        self.alamat = alamat
        if password != '':
            self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.level_user = level_user

class MataUjian(db.Model):
    __tablename__ = 'mata_ujian'
    id = db.Column('id_mu', db.Integer, primary_key = True)
    mataUjian = db.Column(db.String(100), nullable=False)
    pengampu = db.Column(db.String(150), nullable=False)

    def __init__(self, mataUjian, pengampu):
        self.mataUjian = mataUjian
        self.pengampu = pengampu

class Ujian(db.Model):
    __tablename__ = 'ujian'
    id = db.Column('id_ujian', db.BigInteger, primary_key=True)
    ujian = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.String(15), nullable=False)
    waktu = db.Column(db.String(10), nullable=False)
    ruang = db.Column(db.String(15), nullable=False)
    petugas = db.Column(db.String(150), nullable=False)
    db.relationship('Laporan', backref=db.backref('ujian', lazy=True))
    db.relationship('Hasil', backref=db.backref('ujian', lazy=True))

    def __init__(self, ujian, tanggal, waktu, ruang, petugas):
        self.ujian = ujian
        self.tanggal = tanggal
        self.waktu = waktu
        self.ruang = ruang
        self.petugas = petugas

class Hasil(db.Model):
    __tablename__ = 'hasil'
    id = db.Column('id_hasil', db.BigInteger, primary_key=True)
    peserta = db.Column(db.BigInteger, db.ForeignKey('peserta.kode'))
    ujian = db.Column(db.BigInteger, db.ForeignKey('ujian.id_ujian'))
    time_stamp = db.Column(db.DateTime)
    jml_lirik = db.Column(db.BigInteger)
    jml_tengok = db.Column(db.BigInteger)
    jml_dongak = db.Column(db.BigInteger)
    jml_nunduk = db.Column(db.BigInteger)
    jml_naikalis = db.Column(db.BigInteger)
    jml_normal = db.Column(db.BigInteger)


    def __init__(self, peserta, ujian, time_stamp, jml_lirik, jml_tengok, jml_dongak, jml_nunduk, jml_naikalis, jml_normal):
        self.peserta = peserta
        self.ujian = ujian
        self.time_stamp = time_stamp
        self.jml_lirik = jml_lirik
        self.jml_tengok = jml_tengok
        self.jml_dongak = jml_dongak
        self.jml_nunduk = jml_nunduk
        self.jml_naikalis = jml_naikalis
        self.jml_normal = jml_normal

db.create_all()
