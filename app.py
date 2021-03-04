from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(150))
    subject = db.Column(db.String(200))
    message = db.Column(db.String(255))

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        ad = request.form['fullname']
        email = request.form['email']
        movzu = request.form['movzu']
        mesaj = request.form['mesaj']
        gonderilecekMelumat = Message(fullname = ad, email = email, subject = movzu, message = mesaj)
        db.session.add(gonderilecekMelumat)
        db.session.commit()
        return redirect('/admin')
    return render_template('index.html')

@app.route('/change/<id>', methods = ['GET','POST'])
def change(id):
    deyisdirilecekMesaj = Message.query.get(id)
    if request.method == 'POST':
        ad = request.form['fullname']
        email = request.form['email']
        movzu = request.form['movzu']
        mesaj = request.form['mesaj']
        deyisdirilecekMesaj.fullname = ad
        deyisdirilecekMesaj.email = email
        deyisdirilecekMesaj.subject = movzu
        deyisdirilecekMesaj.message = mesaj
        db.session.commit()
        return redirect ('/admin')

    return render_template('change.html', mesaj = deyisdirilecekMesaj)


@app.route('/admin')
def admin():
    mesajlar = Message.query.all()
    return render_template('admin.html', data = mesajlar)

@app.route('/delete/<id>')
def delete(id):
    silinecekOlanMesaj = Message.query.get(id)
    db.session.delete(silinecekOlanMesaj)
    db.session.commit()
    return redirect('/admin')

@app.route('/show/<id>')
def show(id):
    gosterilecekOlanMesaj = Message.query.get(id)
    return render_template('show.html', mesaj = gosterilecekOlanMesaj)


if __name__ == '__main__':
    app.run(debug=True)

