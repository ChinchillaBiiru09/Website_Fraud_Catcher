from mysqlx import Result
from application import app, db, bcrypt, ma, api, Resource
from flask import render_template, request, redirect, url_for, session, flash, jsonify, make_response, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired
# from wtforms_sqlalchemy.fields import QuerySelectField
from functools import wraps
from sqlalchemy import func, or_
from .models import *
# from application import create
import pdfkit


## /*/* Library Chatbot
import os, numpy as np, json
from tensorflow.keras.models import load_model
from .chat import get_response


## /*/* Library Detection
import sys, cv2, dlib, logging, json, os, numpy as np


## /*/* Library API
import json
import sqlite3
from sqlite3 import Error



        ###  */*/*  ~@@@@@@~  *\*\*\*   LOGIC APPS START   */*/*/*/  ~@@@@@@~  *\*\*  ###



class Login(FlaskForm):
    username = StringField('', validators=[InputRequired()], render_kw={'autofocus':True, 'placeholder':'Username'})
    password = PasswordField('', validators=[InputRequired()], render_kw={'autofocus':True, 'placeholder':'Password'})
    level = SelectField('', validators=[InputRequired()], choices=[('Admin','Admin'), ('Petugas','Petugas'),('Peserta','Peserta')])


def Login_dulu(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else :
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    if session.get('login') == True:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


#### ** #### ** #### **  LOGIN START  ~ ~

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('login') == True:
        return redirect(url_for('dashboard'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data) and user.level_user == form.level.data:
                session['login'] = True
                session['id'] = user.id
                session['level'] = user.level_user
                session['user'] = user.username
                return redirect(url_for('dashboard'))
        pesan = "Username atau Password anda salah"
        return render_template("login.html", pesan=pesan, form=form)
    return render_template('login.html', form=form)
#### ** #### ** #### **  LOGIN START  ~ ~




#### *** #########   **** ADMIN AREA START ****   ######### *** ####

@app.route('/dashboard1')
@Login_dulu
def dashboard():
    data1 = db.session.query(Petugas).count()
    data2 = db.session.query(Peserta).count()
    data3 = db.session.query(User).count()
    data4 = db.session.query(MataUjian).count()
    # data4 = db.session.query(func.sum(Laporan.id_ujian)).filter(Laporan.keterangan == "Rusak").scalar()
    # data5 = db.session.query(func.sum(Hasil.ujian)).filter(Hasil.keterangan == "Baik").scalar()
    return render_template('dashboard.html',data1=data1,data2=data2,data3=data3,data4=data4)



#### ** #### ** #### **  KELOLA USER/ADMIN START  ~ ~

@app.route('/kelola_user')
@Login_dulu
def kelola_user():
    data = User.query.filter_by(level_user='Admin')
    return render_template('01-KelolaUser.html', data=data)

## ** ADD ADMIN
@app.route('/tambahuser', methods=['GET','POST'])
@Login_dulu
def tambahuser():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        level = request.form['level']
        db.session.add(User(username,password,level))
        db.session.commit()
        flash("Data Tersimpan !")
        return redirect(url_for('kelola_user'))

## ** EDIT ADMIN
@app.route('/edituser/<id>', methods=['GET','POST'])
@Login_dulu
def edituser(id):
    data = User.query.filter_by(id=id).first()
    if request.method == "POST":
        try:
            data.username = request.form['username']
            if data.password != '':
                data.password = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
            data.level = request.form['level']
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('kelola_user'))
        except:
            flash("Ada trouble")
            return redirect(request.referrer)

## ** DELETE ADMIN
@app.route('/hapususer/<id>', methods=['GET','POST'])
@Login_dulu
def hapususer(id):
    data = User.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('kelola_user'))
#### ** #### ** #### **  KELOLA ADMIN END  ~ ~



#### ** #### ** #### **  KELOLA PESERTA START  ~ ~

@app.route('/kelola_peserta')
@Login_dulu
def kelola_peserta():
    data = Peserta.query.all()
    return render_template('01-KelolaPeserta.html', data=data)

## ** ADD PARTICIPANT
@app.route('/tambahpeserta', methods=['GET','POST'])
@Login_dulu
def tambahpeserta():
    if request.method == "POST":
        kode = request.form['kode']
        nama = request.form['nama']
        jk = request.form['jk']  
        kelas = request.form['kelas']
        jurusan = request.form['jurusan']
        email = request.form['email']
        password = request.form['password']
        level = request.form['level']
        db.session.add(Peserta(kode,nama,jk,kelas,jurusan,email,password,level))
        db.session.add(User(kode,password,level))
        db.session.commit()
        return jsonify({'success':True})

## ** EDIT PARTICIPANT
@app.route('/editpeserta/<kode>', methods=['GET','POST'])
@Login_dulu
def editdaftar(kode):
    data = Peserta.query.filter_by(kode=kode).first()
    data1 = User.query.filter_by(username=kode).first()
    if request.method == "POST":
        try:
            data.kode = request.form['kode']
            data.nama = request.form['nama']
            data.jk = request.form['jk']  
            data.kelas = request.form['kelas']
            data.jurusan = request.form['jurusan']
            data.email = request.form['email']
            if data.password != '':
                    data.password = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
            data.level = request.form['level']
            data1.username = request.form['kode']
            if data1.password != '':
                    data1.password = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
            data1.level = request.form['level']
            db.session.add(data)
            db.session.add(data1)
            db.session.commit()
            return redirect(url_for('kelola_peserta'))
        except:
            flash("Ada trouble")
            return redirect(request.referrer)

## ** DELETE PARTICIPANT
@app.route('/hapuspeserta/<kode>', methods=['GET','POST'])
@Login_dulu
def hapuspeserta(kode):
    data = Peserta.query.filter_by(kode=kode).first()
    data1 = User.query.filter_by(username=kode).first()
    db.session.delete(data)
    db.session.delete(data1)
    db.session.commit()
    return redirect(url_for('kelola_peserta'))
#### ** #### ** #### **  KELOLA PESERTA END  ~ ~



#### ** #### ** #### **  KELOLA PETUGAS START  ~ ~

@app.route('/kelola_petugas')
@Login_dulu
def kelola_petugas():
    data = Petugas.query.all()
    return render_template('01-KelolaPetugas.html', data=data)

## ** ADD OFFICER
@app.route('/tambahpetugas', methods=['GET','POST'])
@Login_dulu
def tambahpetugas():
    if request.method == "POST":
        kode = request.form['kode']
        nama = request.form['nama']
        jk = request.form['jk']
        email = request.form['email']
        alamat = request.form['alamat']
        password = request.form['password']
        level = request.form['level']
        db.session.add(Petugas(kode,nama,jk,email,alamat,password,level))
        db.session.add(User(kode,password,level))
        db.session.commit()
        return jsonify({'success':True})

## ** EDIT OFFICER
@app.route('/editpetugas/<kode>', methods=['GET','POST'])
@Login_dulu
def editpetugas(kode):
    data = Petugas.query.filter_by(kode=kode).first()
    data1 = User.query.filter_by(username=kode).first()
    if request.method == "POST":
        data.kode = request.form['kode']
        data.nama = request.form['nama']
        data.jk = request.form['jk']
        data.email = request.form['email']
        data.alamat = request.form['alamat']
        if data.password != '':
            data.password = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
        data.level = request.form['level']

        data1.kode = request.form['kode']
        if data1.password != '':
            data1.password = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
        data1.level = request.form['level']

        db.session.add(data)
        db.session.add(data1)
        db.session.commit()
        return redirect(url_for('kelola_petugas'))

## ** DELETE OFFICER
@app.route('/hapuspetugas/<kode>', methods=['GET','POST'])
@Login_dulu
def hapuspetugas(kode):
    data = Petugas.query.filter_by(kode=kode).first()
    data1 = User.query.filter_by(username=kode).first()
    db.session.delete(data)
    db.session.delete(data1)
    db.session.commit()
    return redirect(request.referrer)
#### ** #### ** #### **  KELOLA PETUGAS END  ~ ~



#### ** #### ** #### **  KELOLA UJIAN START  ~ ~

@app.route('/kelola_ujian')
@Login_dulu
def kelola_ujian():
    data = MataUjian.query.all()
    data1 = Petugas.query.all()
    return render_template('01-KelolaUjian.html', data=data, data1=data1)

## ** ADD EXAM
@app.route('/tambahmataujian', methods=['GET','POST'])
@Login_dulu
def tambahmataujian():
    if request.method == 'POST':
        mataujian = request.form['mu']
        pengampu = request.form['pengampu']
        db.session.add(MataUjian(mataujian,pengampu))
        db.session.commit()
        return jsonify({'success':True})
    else:
        return redirect(request.referrer)

## ** EDIT EXAM
@app.route('/editmataujian/<id>', methods=['GET','POST'])
@Login_dulu
def editmataujian(id):
    data = MataUjian.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.nama = request.form['mu']
        data.jadwal = request.form['pengampu']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('kelola_ujian'))

## ** DELETE EXAM
@app.route('/hapusmataujian/<id>', methods=['GET','POST'])
@Login_dulu
def hapusmataujian(id):
    data = MataUjian.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(request.referrer)
#### ** #### ** #### **  KELOLA UJIAN END  ~ ~



#### ** #### ** #### **  KELOLA JADWAL START  ~ ~

@app.route('/kelola_jadwal')
@Login_dulu
def kelola_jadwal():
    data = Ujian.query.all()
    data1 = MataUjian.query.all()
    data2 = Petugas.query.all()
    return render_template('01-KelolaJadwal.html', data=data, data1=data1, data2=data2)

## ** Add Schedule Exam
@app.route('/tambahjadwal', methods=['GET','POST'])
@Login_dulu
def tambahjadwal():
    if request.method == 'POST':
        ujian = request.form['ujian']
        tanggal = request.form['tanggal']
        waktu = request.form['waktu']
        ruang = request.form['ruang']
        petugas = request.form['petugas']
        db.session.add(Ujian(ujian,tanggal,waktu,ruang,petugas))
        db.session.commit()
        return jsonify({'success':True})
    else:
        return redirect(request.referrer)

## ** Edit Schedule Exam
@app.route('/editjadwal/<id>', methods=['GET','POST'])
@Login_dulu
def editjadwal(id):
    data = Ujian.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.ujian = request.form['ujian']
        data.tanggal = request.form['tanggal']
        data.waktu = request.form['waktu']
        data.ruang = request.form['ruang']
        data.petugas = request.form['petugas']
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('kelola_jadwal'))

## ** Delete Schedule Exam
@app.route('/hapusjadwal/<id>', methods=['GET','POST'])
@Login_dulu
def hapusjadwal(id):
    data = Ujian.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(request.referrer)
#### ** #### ** #### **  KELOLA JADWAL END  ~ ~

#### ** #########   **** ADMIN END ****   ######### ** ####




#### ** #########   ****  OTHER USER START  ****   ######### ** ####

@app.route('/mata_ujian')
@Login_dulu
def mata_ujian():
    data = MataUjian.query.all()
    data1 = Petugas.query.all()
    return render_template('02-MataUjian.html', data=data, data1=data1)

@app.route('/jadwal_ujian')
@Login_dulu
def jadwal_ujian():
    data = Ujian.query.all()
    data1 = MataUjian.query.all()
    data2 = Petugas.query.all()
    return render_template('02-JadwalUjian.html', data=data, data1=data1, data2=data2)

@app.route('/daftar_peserta')
@Login_dulu
def daftar_peserta():
    data = Peserta.query.all()
    return render_template('02-DaftarPeserta.html', data=data)

#### ** #########   ****  OTHER USER END  ****   ######### ** ####

#### ** #### ** #### **  LAPORAN START  ~ ~

@app.route('/laporan', methods=['GET','POST'])
@Login_dulu
def laporan():
    data = Hasil.query.all()
    return render_template('laporan.html', data=data)

@app.route('/cari_data', methods=['GET','POST'])
@Login_dulu
def cari_data():
    if request.method == 'POST':
        keyword = request.form['q']
        formt = "%{0}%".format(keyword)
        datanya = Peserta.query.join(Hasil, Peserta.kode == Hasil.peserta).filter(or_(Peserta.kode.like(formt))).all()
        if datanya:
            flash("Data berhasil di temukan")
            tombol = "tombol"
        elif not datanya:
            pesan = "Data tidak berhasil di temukan"
            return render_template('pencarian.html',datanya=datanya,pesan=pesan)
        return render_template('pencarian.html',datanya=datanya,tombol=tombol,keyword=keyword)

@app.route('/cetak_pdf/<keyword>', methods=['GET','POST'])
@Login_dulu
def cetak_pdf(keyword):
    formt = "%{0}%".format(keyword)
    datanya = Peserta.query.join(User, Peserta.user_id == User.id).filter(or_(Peserta.tanggal.like(formt))).all()
    html = render_template("pdf.html",datanya=datanya)
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=laporan.pdf'
    return response
#### ** #### ** #### **  LAPORAN END  ~ ~



#### ** #### ** #### **  LOGOUT START  ~ ~

@app.route('/logout')
@Login_dulu
def logout():
    session.clear()
    return redirect(url_for('login'))
#### ** #### ** #### **  LOGOUT START  ~ ~

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ABOUT

@app.route('/aboutme')
@Login_dulu
def aboutme():
    return render_template('aboutme.html')




#### ** #########   **** DETECTION START ****   ######### ** ####


@app.route('/deteksi/<id>', methods=['GET','POST'])
@Login_dulu
def deteksi(id):
    # Logging for face detection
    def setup_custom_logger():
        LOG_DIR = os.getcwd() + '/application/' + 'logs'
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        
        formatter = logging.Formatter(json.dumps({'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}))
        handler = logging.FileHandler(LOG_DIR+'/log.json')
        handler.setFormatter(formatter)
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.addHandler(screen_handler)
        return logger
    
    # Detection
    kameraVideo = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(r'.\application\model\shape_predictor_68_face_landmarks.dat')
    model_F = load_model(r'.\application\model\model_motion01.h5')

    # Buat warnain labelnya
    labels_dict_F  = {0:'Mengangkat Kedua Alis', 1:'Lirik Kanan', 2:'Lirik Kiri',
                3:'Normal', 4:'Lihat Atas', 5:'Lihat Bawah', 6:'Lihat Kanan',
                7:'Lihat Kiri'}
    color_dict_F = {0:(255,200,250), 1:(0,0,128), 2:(211,85,186), 3:(0,255,0),
                4:(0,155,255), 5:(255,255,0), 6:(255,0,0), 7:(128,128,0)}

    # Deteksi
    index = 0
    logger = setup_custom_logger()

    # inisialisasi untuk get count tiap gerakan
    mengangkat_alis = 0
    lirik = 0
    normal = 0
    lihat_atas = 0
    lihat_bawah = 0
    tengok = 0
    no_face = 0
    miss = 0

    while (True):
        try:
            #ambil per KERANGKA UNTUK DIPROSES
            ret, kerangkaAsal = kameraVideo.read()

            #siap2 ngesave dgn judul berdasarkan counter index
            if not ret: 
                break

            dets = detector(kerangkaAsal)

            num_faces = len(dets)
            #print("banyaknya wajah:",num_faces)

            if num_faces == 0:
                print("Sorry, there were no faces found")
                logger.debug('Face Not Found')
                cv2.putText(kerangkaAsal, "NO FACES", (200,240), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 5)
                miss += 1

            # Find the 5 face landmarks we need to do the alignment.
            faces = dlib.full_object_detections()

            for detection in dets:
                faces.append(predictor(kerangkaAsal, detection))

            images = dlib.get_face_chips(kerangkaAsal, faces, size=320)

            for image in images:
                #konversi ke skala abu-abu
                kerangkaAbu = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            #bila index habis dibagi 5 (in case mau diambil tiap frame ke 5)
            if index%10==0:
                #isi dengan kode apa yg mau dilakukan saat mendeteksi frame ke 5
                
                resized_F = cv2.resize(kerangkaAbu,(100,100))
                normalized_F = resized_F/255.0
                reshaped_F = np.reshape(normalized_F,(1,100,100,1))
                result_F = model_F.predict(reshaped_F)
                                    
            index += 1
            label_F = np.argmax(result_F,axis=1)[0]
            logger.info(labels_dict_F[label_F])
            hasil = labels_dict_F[label_F]
            
            #untuk tampilan saja
            if (label_F != 0) & (label_F != 1):        
                cv2.rectangle(kerangkaAsal,(10,400),(200,450),color_dict_F[label_F],-1)
                cv2.putText(kerangkaAsal, labels_dict_F[label_F], (20,430),cv2.FONT_HERSHEY_SIMPLEX,0.8, (255,255,255),2)
            else: 
            #ukuran latar untuk mengangkat kedua alis
                cv2.rectangle(kerangkaAsal,(10,400),(350,450),color_dict_F[label_F],-1)
                cv2.putText(kerangkaAsal, labels_dict_F[label_F], (10,430),cv2.FONT_HERSHEY_SIMPLEX,0.8, (255,255,255),2)

            # untuk get count tiap label
            if(label_F == 0):
                mengangkat_alis +=1
            elif(label_F == 1 or label_F == 2):
                lirik += 1
            elif(label_F == 3):
                normal += 1
            elif(label_F == 4):
                lihat_atas += 1
            elif(label_F == 5):
                lihat_bawah += 1
            elif(label_F == 6 or label_F == 7):
                tengok += 1
            else :
                no_face += 1

        except RuntimeError as e:
            print (e)
        
        #Tampilkan
        cv2.imshow('Cheating Detection', kerangkaAsal)
        #cv2.imshow('Kerangka Asal', image)
            
        key=cv2.waitKey(1)

        if(key==27):
            print ("-------------------Program Selesai Digunakan--------------------")
            break
    
    cv2.destroyAllWindows()
    kameraVideo.release() 

    data = Ujian.query.filter_by(id=id).first()
    peserta = session['user']
    ujian = data.id
    time = func.now()
    jml_lirik = lirik
    jml_tengok = tengok
    jml_dongak = lihat_atas
    jml_nunduk = lihat_bawah
    jml_naikalis = mengangkat_alis
    jml_normal = normal
    db.session.add(Hasil(peserta,ujian,time,jml_lirik,jml_tengok,jml_dongak,jml_nunduk,jml_naikalis,jml_normal))
    db.session.commit()

    return render_template('laporan.html')

@app.route("/pengawasan/<id>", methods=['GET','POST'])
@Login_dulu
def pengawasan(id):
    data = Ujian.query.filter_by(id=id).first()
    return render_template('pengawasvirtual.html', data=data)





######################## CHABOT


@app.route("/cb", methods=['GET','POST'])
@Login_dulu
def cb():
    return render_template ("bot.html")

@app.route("/predict", methods=['GET','POST'])
@Login_dulu
def predict():
    text =  request.get_json().get('message')
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)




############################# REST API



class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")
        model = User

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

class PostListResource(Resource):
    def get(self):
        posts = User.query.all()
        return posts_schema.dump(posts)

    # new
    def post(self):
        new_post = User(
            username=request.json['username'],
            password=request.json['password']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

api.add_resource(PostListResource, '/posts')


class PostResource(Resource):
    def get(self, post_id):
        post = User.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = User.query.get_or_404(post_id)

        if 'username' in request.json:
            post.username = request.json['username']
        if 'password' in request.json:
            post.password = request.json['password']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = User.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

api.add_resource(PostResource, '/posts/<int:post_id>')




class PostResultSchema(ma.Schema):
    class Meta:
        fields = ("id", "peserta", "ujian", "time_stamp", "jml_lirik", "jml_tengok", "jml_dongak", "jml_nunduk", "jml_naik_alis", "jml_normal")
        model = Hasil

result_schema = PostResultSchema()
results_schema = PostResultSchema(many=True)

class ResultListResource(Resource):
    def get(self):
        results = Hasil.query.all()
        return results_schema.dump(results)

    # new
    def post(self):
        new_result = Hasil(
            peserta=request.json['peserta'],
            ujian=request.json['ujian'],
            time_stamp=request.json['time_stamp'],
            jml_lirik=request.json['jml_lirik'],
            jml_tengok=request.json['jml_tengok'],
            jml_dongak=request.json['jml_dongak'],
            jml_nunduk=request.json['jml_nunduk'],
            jml_naikalis=request.json['jml_naikalis'],
            jml_normal=request.json['jml_normal']
        )
        db.session.add(new_result)
        db.session.commit()
        return result_schema.dump(new_result)

api.add_resource(ResultListResource, '/results')


class ResultResource(Resource):
    def get(self, result_id):
        result = Hasil.query.get_or_404(result_id)
        return result_schema.dump(result)

    def patch(self, result_id):
        result = User.query.get_or_404(result_id)

        if 'peserta' in request.json:
            result.username = request.json['peserta']
        if 'ujian' in request.json:
            result.password = request.json['ujian']

        db.session.commit()
        return result_schema.dump(result)

    def delete(self, result_id):
        result = Hasil.query.get_or_404(result_id)
        db.session.delete(result)
        db.session.commit()
        return '', 204

api.add_resource(ResultResource, '/results/<int:result_id>')