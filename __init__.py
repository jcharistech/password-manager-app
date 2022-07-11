from flask import Flask,render_template,url_for,redirect,request,flash
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
from .extensions import db,login_manager
from .models import PasswordManager,User
from flask_login import login_required


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data2.db'
    app.config['SECRET_KEY'] = 'the random string'

    db.init_app(app)
    # For managing sessions during login
    login_manager.init_app(app)


    from .auth import auth
    app.register_blueprint(auth)

    @login_manager.user_loader
    def load_user(user_id):
        # using the user id as primary key as id for session
        return User.query.get(int(user_id))

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

    @login_required
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

    return app
