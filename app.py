from flask import Flask,render_template,request,url_for,flash,redirect,send_file
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import csv
import time
timestr = time.strftime("%Y%m%d-%H%M%S")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'the random string' 
db = SQLAlchemy(app)

# Model
class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(520), nullable=False)
    site_url = db.Column(db.String(520), nullable=False)
    site_password = db.Column(db.String(520), nullable=False)

    def __repr__(self):
        return '<PasswordManager %r>' % self.email

# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# with open("secret_key.txt","wb") as f:
#   f.write(key)

with open("secret_key.txt","rb") as f:
    key = f.read()


def encrypt_password(key,data):
    f = Fernet(key)
    encrypted_token = f.encrypt(str(data).encode())
    return encrypted_token




@app.route("/")
def index():
    passwordlist = PasswordManager.query.all()
    return render_template('index.html', passwordlist=passwordlist)    

@app.route("/add",methods=["GET","POST"])
def add_password():
    if request.method == 'POST':
        email = request.form['email']
        site_url = request.form['site_url']
        site_password = request.form['site_password']
        new_password_details = PasswordManager(email=email,site_url=site_url,site_password=site_password)
        db.session.add(new_password_details)
        db.session.commit()
        flash("Password Added")
        return redirect('/')
       

@app.route('/delete/<int:id>')
def delete(id):
    new_password_to_delete = PasswordManager.query.get_or_404(id)

    try:
        db.session.delete(new_password_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = PasswordManager.query.get_or_404(id)

    if request.method == 'POST':
        task.email = request.form['email']
        task.site_url = request.form['site_url']
        task.site_password = request.form['site_password']
        try:
            db.session.commit()
            flash("Password Updated")
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


@app.route('/export')
def export_data():
    with open('dump.csv', 'w') as f:
     out = csv.writer(f)
     out.writerow(['id', 'email','site_url','site_password'])
     for item in PasswordManager.query.all():
        out.writerow([item.id, item.email,item.site_url,item.site_password])
    return send_file('dump.csv',
        mimetype='text/csv',
        download_name=f"Export_Password_{timestr}.csv",
        as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)