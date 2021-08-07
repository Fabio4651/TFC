from flask import Flask, render_template, request, session, make_response, redirect, url_for, jsonify 
from flask_qrcode import QRcode
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_modals import Modal, render_template_modal
from flask_session import Session 
from os.path import join, dirname, realpath
from flask_uploads import IMAGES, UploadSet, configure_uploads
import pandas as pd
from pathlib import Path
from werkzeug.utils import secure_filename
import json
import uuid
from datetime import datetime


app = Flask(__name__)
modal = Modal(app)

#The secret key shhh 
app.config['SECRET_KEY'] = '_1#y6G"F7Q2z\n\succ/'
app.config['APPLICATION_ROOT'] = "/"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/befit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

files = UploadSet('files', IMAGES)

app.config['UPLOADED_FILES_ALLOW'] = set(['png', 'jpg', 'jpeg', 'gif', 'csv'])
app.config['UPLOADED_FILES_DEST'] = 'static/upload'
configure_uploads(app, files)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))
    apelido = db.Column(db.String(25))
    data_nascimento = db.Column(db.Date)
    genero = db.Column(db.String(25))
    peso = db.Column(db.Float)
    altura = db.Column(db.Float)
    saude = db.Column(db.Text)
    estilo_vida = db.Column(db.Text)
    telefone = db.Column(db.Integer)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    cargo = db.Column(db.String(45))
    imgpath = db.Column(db.String(80))

    def __init__(self, nome, apelido, data_nascimento, genero, peso, altura, saude, estilo_vida, telefone, email, password, cargo, imgpath):
        self.nome=nome
        self.apelido=apelido
        self.data_nascimento=data_nascimento
        self.genero=genero
        self.peso=peso
        self.altura=altura
        self.saude=saude
        self.estilo_vida=estilo_vida
        self.telefone=telefone
        self.email=email
        self.password=password
        self.cargo=cargo
        self.imgpath=imgpath

    def __repr__(self):
        return repr(id)

class Trainers(db.Model):
    __tablename__ = 'trainers'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))
    apelido = db.Column(db.String(25))
    genero = db.Column(db.String(25))
    telefone = db.Column(db.Integer)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    cargo = db.Column(db.String(45))
    imgpath = db.Column(db.String(80))

    def __init__(self, nome, apelido, genero, telefone, email, password, imgpath, cargo):
        self.nome=nome
        self.apelido=apelido
        self.genero=genero
        self.telefone=telefone
        self.email=email
        self.password=password
        self.imgpath=imgpath
        self.cargo=cargo

    def __repr__(self):
        return repr(id)        


class Exercicios(db.Model):
    __tablename__ = 'exercicios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))
    descricao = db.Column(db.Text)
    gifpath = db.Column(db.String(80))

    def __init__(self, nome, descricao, gifpath):
        self.nome=nome
        self.descricao=descricao
        self.gifpath=gifpath

    def __repr__(self):
        return repr(id)

class Planos(db.Model):
    __tablename__ = 'planos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(25))
    descricao = db.Column(db.String(25))
    exercicios = db.Column(db.String(5000))

    def __init__(self, nome, descricao, exercicios):
        self.nome=nome
        self.descricao=descricao
        self.exercicios=exercicios
    def __repr__(self):
        return repr(id)          

class Body(db.Model):
    __tablename__ = 'body'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.String(25))
    date = db.Column(db.Date)
    weight = db.Column(db.String(25))
    height = db.Column(db.String(25))
    bmi = db.Column(db.String(25))
    fatRate = db.Column(db.String(25))
    bodyWaterRate = db.Column(db.String(25))
    boneMass = db.Column(db.String(25))
    metabolism = db.Column(db.String(25))
    muscleRate = db.Column(db.String(25))
    visceralFat = db.Column(db.String(25))
    impedance = db.Column(db.String(25))


    def __init__(self, user_id, timestamp, date, weight, height, bmi, fatRate, bodyWaterRate, boneMass, metabolism, muscleRate, visceralFat, impedance):
        self.user_id=user_id
        self.timestamp=timestamp
        self.date=date
        self.weight=weight
        self.height=height
        self.bmi=bmi
        self.fatRate=fatRate
        self.bodyWaterRate=bodyWaterRate
        self.boneMass=boneMass
        self.metabolism=metabolism
        self.muscleRate=muscleRate
        self.visceralFat=visceralFat
        self.impedance=impedance

    def __repr__(self):
        return repr(id)        


db.create_all()        

QRcode(app)

@app.route('/')
def index():
    if 'email' in session:
        total_users = Users.query.filter_by(cargo="Utilizador").count()
        total_trainers = Trainers.query.count()
        total_Exercicios = Exercicios.query.count()
        return render_template('home.html', total_users=total_users, total_trainers=total_trainers, total_Exercicios=total_Exercicios)
    return redirect(url_for('loginPage')) 

@app.route('/uploadcsv')
def uploadcsv():
    if 'email' in session:
        return render_template('uploadcsv.html')   
    return redirect(url_for('loginPage'))    

@app.route('/csv', methods=['POST'])
def csv():
    if 'email' in session:
        body = request.files['body']
        
        #if request.method == 'POST' and body:
        filename = 'static/upload/' + files.save(request.files['body'])  

        print("bruh"+filename)
        # CVS Column Names
        col_names = ['timestamp', 'weight', 'height', 'bmi', 'fatRate', 'bodyWaterRate', 'boneMass', 'metabolism', 'muscleRate', 'visceralFat', 'impedance']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(filename, names=col_names, header=None, skiprows=1)

        csvData = csvData.fillna("Null")
        # Loop through the Rows
        for i, row in csvData.iterrows():
            #print(i, row['timestamp'], row['weight'], row['height'], row['bmi'], row['fatRate'], row['bodyWaterRate'], row['boneMass'], row['metabolism'], row['muscleRate'], row['visceralFat'], row['impedance'])    
            """df = pd.DataFrame(csvData, columns = ["timestamp", "weight", "height", "bmi", "fatRate", "bodyWaterRate", "boneMass", "metabolism", "muscleRate", "visceralFat", "impedance"])

            print(df.fillna("Null"))"""
            
            new_csv = Body(user_id = session['id'], timestamp = row['timestamp'], date = datetime.fromtimestamp(row['timestamp']).date(), weight = row['weight'], height = row['height'], bmi = row['bmi'], fatRate = row['fatRate'], bodyWaterRate = row['bodyWaterRate'], boneMass=row['boneMass'], metabolism=row['metabolism'], muscleRate = row['muscleRate'], visceralFat = row['visceralFat'], impedance=row['impedance'])


            db.session.add(new_csv)
            db.session.commit()
        

        print("============================================================")
        timestamp = 1624789573
        dt_object = datetime.fromtimestamp(timestamp)

        only_date = dt_object.date()

        print("data =", only_date)
        #print("type(dt_object) =", type(dt_object))

        return render_template('uploadcsv.html')    
    return redirect(url_for('loginPage'))  

@app.route('/consulta')
def consulta():
    if 'email' in session:
        return render_template('consulta.html', list=list)   

    return redirect(url_for('loginPage'))     

@app.route('/body')
def body():
    if 'email' in session:
        #list = Body.query.all().filter_by(user_id=session['id'])
        list = Body.query.filter_by(user_id=session['id'])

        labels = Body.query.with_entities(Body.date).filter_by(user_id=session['id'])
        values = Body.query.with_entities(Body.weight).filter_by(user_id=session['id'])
        bmi = Body.query.with_entities(Body.bmi).filter_by(user_id=session['id'])
        #labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
        #values = [10, 9, 8, 7, 6, 4, 7, 8]

        return render_template('body.html', list=list, labels=labels, values=values, bmi=bmi)   
    return redirect(url_for('loginPage'))     

@app.route('/loginPage')
def loginPage():
    return render_template('login.html')  


@app.route('/login', methods=['POST'])
def login():
    
    data = request.form
    email, password = data.get('email'), data.get('password')
    user = Users.query.filter_by(email=email, password=password).first()
    trainer = Trainers.query.filter_by(email=email, password=password).first()


    #print(user.cargo)
    if(user is None and trainer is None):
        return render_template('nologin.html')

    """if not user:
        return jsonify({'message' : 'Could not verify user!'})    """   

    print(user)    

    if (trainer is not None): # or user==None
        session['id'] = trainer.id
        session['nome'] = trainer.nome
        session['apelido'] = trainer.apelido
        session['email'] = trainer.email
        session['img'] = trainer.imgpath
        session['cargo'] = trainer.cargo  
    elif (user is not None):
        session['id'] = user.id
        session['nome'] = user.nome
        session['apelido'] = user.apelido
        session['email'] = user.email
        session['img'] = user.imgpath
        session['cargo'] = user.cargo

    return redirect(url_for('index')) 
    


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    check = {'check': 'true'}
    return redirect(url_for('loginPage'))    

@app.route('/registo')
def registo():
    return render_template('registo.html')  

@app.route('/detalhesUser', methods=['POST'])
def detalhesUser():
    if 'email' in session:
        data=request.args.get('id_user')
        if(session['cargo'] == "Treinador"):
            list = Trainers.query.filter_by(id=data)
        elif(session['cargo'] == "Utilizador" or session['cargo'] == "Administrador"):   
            list = Users.query.filter_by(id=data)

        return render_template('detalhes_user.html', list=list)   

    return redirect(url_for('loginPage')) 

@app.route('/adduser')
def adduser():
    if 'email' in session:
        u = Users.query.all()
        return render_template('adduser.html') 
    return redirect(url_for('loginPage')) 

@app.route('/inserirusers', methods=['POST'])
def inserirusers():
    if 'email' in session:
        email = request.form['email']  
        password = request.form['password'] 
        nome = request.form['nome']  
        apelido = request.form['apelido'] 
        telefone = request.form['telefone'] 
        peso = request.form['peso']  
        altura = request.form['altura']
        datadenascimento = request.form['datadenascimento']
        genero = request.form['genero']
        saude = request.form['saude']
        estilovida = request.form['estilovida']
        cargo = request.form['cargo']
        imgPerfil = request.files['imgPerfil']
        filename = 'static/img/user.png'
        if request.method == 'POST' and imgPerfil:
            filename = 'static/upload/' + files.save(request.files['imgPerfil'])
        new_user = Users(email=email, password=password, nome=nome, apelido=apelido, telefone=telefone, peso=peso, altura=altura, data_nascimento=datadenascimento, genero=genero, saude=saude, estilo_vida=estilovida, cargo=cargo, imgpath=filename)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('verusers'))
    return redirect(url_for('loginPage')) 

@app.route('/deleteuser', methods=['POST'])
def deleteusers():
    if 'email' in session:
        data=request.args.get('id_user')
        Users.query.filter_by(id=data).delete()
        db.session.commit()
        return redirect(url_for('verusers'))
    return redirect(url_for('loginPage'))    

@app.route('/verusers')
def verusers():
    if 'email' in session:
        data = Users.query.all()
        return render_template('verusers.html', data=data)  
    return redirect(url_for('loginPage'))

@app.route('/updateusers', methods=['POST'])
def updateusers():
    if 'email' in session:
        data=request.args.get('id_user')
        update = Users.query.filter_by(id=data)

        return render_template('edituser.html', update=update)
    return redirect(url_for('loginPage'))    

@app.route('/editusers', methods=['POST'])
def editusers():
    if 'email' in session:
        data = request.form['id']
        update = Users.query.filter_by(id=data).first()
        bd_img = update.imgpath
        imgPerfil = request.files['imgPerfil']

        if request.method == 'POST' and 'email' in request.form:
            update.email = request.form['email'] 

        if request.method == 'POST' and 'password' in request.form:
            if request.form['password'] == '':
                update.password = update.password
            else:
                update.password = request.form['password'] 

        if request.method == 'POST' and 'nome' in request.form:
            update.nome = request.form['nome'] 

        if request.method == 'POST' and 'apelido' in request.form:
            update.apelido = request.form['apelido'] 

        if request.method == 'POST' and 'telefone' in request.form:
            update.telefone = request.form['telefone']     

        if request.method == 'POST' and 'peso' in request.form:    
            update.peso = request.form['peso']

        if request.method == 'POST' and 'altura' in request.form:    
            update.altura = request.form['altura']

        if request.method == 'POST' and 'cargo' in request.form:    
            update.cargo = request.form['cargo']    
        
        if request.method == 'POST' and 'datadenascimento' in request.form:
                update.data_nascimento = request.form['datadenascimento']    

        if request.method == 'POST' and 'genero' in request.form:
                update.genero = request.form['genero']           

        if request.method == 'POST' and 'saude' in request.form:
                update.saude = request.form['saude']      

        if request.method == 'POST' and 'estilovida' in request.form:
                update.estilo_vida = request.form['estilovida']    

        update.imgPerfil = bd_img
        if request.method == 'POST' and imgPerfil:
            update.imgpath = 'static/upload/' + files.save(request.files['imgPerfil']) 

        db.session.commit()
        return redirect(url_for('verusers'))

    return redirect(url_for('loginPage')) 
    
    
@app.route('/detalhesExercicio', methods=['POST'])
def detalhesExercicio():
    if 'email' in session:
        data=request.args.get('id_user')
        list = Exercicios.query.filter_by(id=data)

        return render_template('detalhes_exercicio.html', list=list)       
    return redirect(url_for('loginPage'))

@app.route('/addexercicio')
def addexercicio():
    if 'email' in session:
        e = Exercicios.query.all()
        return render_template('addexercicio.html')  
    return redirect(url_for('loginPage'))

@app.route('/inserirexercicio', methods=['POST'])
def inserirexercicio():
    if 'email' in session:
        nome = request.form['nome']  
        descricao = request.form['descricao']
        gif = request.files['gif']
        filename = 'static/img/user.png'
        if request.method == 'POST' and gif:
            filename = 'static/upload/' + files.save(request.files['gif'])
        new_exercicio = Exercicios(nome=nome, descricao=descricao, gifpath=filename)
        db.session.add(new_exercicio)
        db.session.commit()
        return redirect(url_for('verexercicio'))     
    return redirect(url_for('loginPage'))

@app.route('/verexercicio')
def verexercicio():
    if 'email' in session:
        data = Exercicios.query.all()
        return render_template('verexercicio.html', data=data)  
    return redirect(url_for('loginPage'))

@app.route('/deleteexercicio', methods=['POST'])
def deleteexercicio():
    if 'email' in session:
        data=request.args.get('id_exercicio')
        Exercicios.query.filter_by(id=data).delete()
        db.session.commit()
        return redirect(url_for('verexercicio'))  
    return redirect(url_for('loginPage'))

@app.route('/updateexercicio', methods=['POST'])
def updateexercicio():
    if 'email' in session:
        data=request.args.get('id_user')
        update = Exercicios.query.filter_by(id=data)

        return render_template('editexercicio.html', update=update)
    return redirect(url_for('loginPage'))

@app.route('/editexercicio', methods=['POST'])
def editexercicio():
    if 'email' in session:
        data = request.form['id']
        update = Exercicios.query.filter_by(id=data).first()
        bd_gif = update.gifpath
        gif = request.files['gif']

        if request.method == 'POST' and 'nome' in request.form:
            update.nome = request.form['nome']          

        if request.method == 'POST' and 'descricao' in request.form:
                update.descricao = request.form['descricao']        

        update.gifpath = bd_gif
        if request.method == 'POST' and gif:
            update.gifpath = 'static/upload/' + files.save(request.files['gif']) 

        db.session.commit()
        return redirect(url_for('verexercicio'))
    return redirect(url_for('loginPage'))

@app.route('/detalhesTrainer', methods=['POST'])
def detalhesTrainer():
    if 'email' in session:
        data=request.args.get('id_user')
        list = Trainers.query.filter_by(id=data)

        return render_template('detalhes_trainer.html', list=list)   
    return redirect(url_for('loginPage'))

@app.route('/addtrainer')
def addtrainer():
    if 'email' in session:
        t = Trainers.query.all()
        return render_template('addtrainer.html')  
    return redirect(url_for('loginPage'))

@app.route('/inserirtrainer', methods=['POST'])
def inserirtrainer():
    if 'email' in session:
        email = request.form['email']  
        password = request.form['password'] 
        nome = request.form['nome']  
        apelido = request.form['apelido'] 
        telefone = request.form['telefone'] 
        genero = request.form['genero']
        imgPerfil = request.files['imgPerfil']
        filename = 'static/img/user.png'
        if request.method == 'POST' and imgPerfil:
            filename = 'static/upload/' + files.save(request.files['imgPerfil'])
        new_trainer = Trainers(email=email, password=password, nome=nome, apelido=apelido, telefone=telefone, genero=genero, imgpath=filename)
        db.session.add(new_trainer)
        db.session.commit()
        return redirect(url_for('vertrainer'))    
    return redirect(url_for('loginPage'))

@app.route('/vertrainer')
def vertrainer():
    if 'email' in session:
        data = Trainers.query.all()
        return render_template('vertrainer.html', data=data) 
    return redirect(url_for('loginPage'))

@app.route('/deletetrainer', methods=['POST'])
def deletetrainer():
    if 'email' in session:
        data=request.args.get('id_trainer')
        Trainers.query.filter_by(id=data).delete()
        db.session.commit()
        return redirect(url_for('vertrainer')) 
    return redirect(url_for('loginPage'))

@app.route('/updatetrainer', methods=['POST'])
def updatetrainer():
    if 'email' in session:
        data=request.args.get('id_user')
        update = Trainers.query.filter_by(id=data)

        return render_template('edittrainer.html', update=update)
    return redirect(url_for('loginPage'))

@app.route('/edittrainer', methods=['POST'])
def edittrainer():
    if 'email' in session:
        data = request.form['id']
        update = Trainers.query.filter_by(id=data).first()
        bd_img = update.imgpath
        imgPerfil = request.files['imgPerfil']

        if request.method == 'POST' and 'nome' in request.form:
            update.nome = request.form['nome'] 

        if request.method == 'POST' and 'apelido' in request.form:
            update.apelido = request.form['apelido']  

        if request.method == 'POST' and 'genero' in request.form:
            update.genero = request.form['genero']  

        if request.method == 'POST' and 'email' in request.form:
            update.email = request.form['email']      

        if request.method == 'POST' and 'telefone' in request.form:
            update.telefone = request.form['telefone']  

        if request.method == 'POST' and 'password' in request.form:
            if request.form['password'] == '':
                update.password = update.password
            else:
                update.password = request.form['password']                               

        update.imgpath = bd_img
        if request.method == 'POST' and imgPerfil:
            update.imgpath = 'static/upload/' + files.save(request.files['imgPerfil']) 

        db.session.commit()
        return redirect(url_for('vertrainer'))           
    return redirect(url_for('loginPage'))

@app.route('/addplano')
def addplano():
    if 'email' in session:

        data = Exercicios.query.all()
        return render_template('addplano.html', data=data)  
    return redirect(url_for('loginPage'))

@app.route('/inserirplano', methods=['POST'])
def inserirplano():
    if 'email' in session:  

        nome = request.form['nome']
        descricao = request.form['descricao']
        count = int(request.form['count'])

        if nome is None or descricao is None or nome == '' or descricao == '':
            return {'message' : 'please choose a client'}, 400, {'dataType':'application/json'} 

        """try:
            results = (
                db.session.query(Marking, Cars, User)
                .filter(Marking.date==date, Marking.hour==hour, Marking.car2id==Cars.id, Marking.client2id==User.id,)
                .first()
                )
        except:
            return {'message' : 'Database Error'}, 400, {'dataType':'application/json'}"""

        """user = [results.User.nome, results.User.email, results.User.telefone, 'data']

        car = [results.Cars.marca, results.Cars.cor, results.Cars.matricula, date]
        """
        teste = 0
        #print(count)
        output = []
        for exercicio, rep, repet in zip(request.form.getlist('exercicio'),request.form.getlist('rep'),request.form.getlist('repet')):
            if not all((exercicio, rep, repet)):
                return {'message' : 'List item Empty'}, 400, {'dataType':'application/json'}
            data = {}
            data['exercicio'] = exercicio
            data['rep'] = rep
            data['repet'] = repet
            output.append(data)

            thisdict =	{
                "brand": "Ford",
                "model": "Mustang",
                "year": 1964
            }

        #print(output)
        exercicio2 = "exercicio"+str(teste)
        rep2 = "rep"+str(teste)
        repet2 = "repet"+str(teste)
        
        for exercicio, rep, repet in zip(request.form.getlist('exercicio'+str(teste)),request.form.getlist('rep'+str(teste)),request.form.getlist('repet'+str(teste))):
            if not all((exercicio, rep, repet)):
                return {'message' : 'List item Empty'}, 400, {'dataType':'application/json'}
            data2 = {}
            data2['exercicio'+str(teste)] = exercicio
            data2['rep'+str(teste)] = rep
            data2['repet'+str(teste)] = repet
            output.append(data2)

            thisdict =	{
                "brand": "Ford",
                "model": "Mustang",
                "year": 1964
            }
        #print(str(teste))
        print(output)
        teste=teste+1
        """novo_plano = Planos(nome=nome, descricao=descricao, exercicios=apelido, telefone=telefone, genero=genero, imgpath=filename)
            db.session.add(new_trainer)
            db.session.commit()"""

        #rendered = render_template('pdftemplate1.html',exercicio=exercicio, rep=rep, soma=repet, plist=output)


        return "hi welcome to chilli's"
    return redirect(url_for('loginPage'))

@app.route('/verplano')
def verplano():
    if 'email' in session:
        return render_template('verplano.html')  
    return redirect(url_for('loginPage'))     
          