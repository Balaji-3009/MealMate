import os
from flask import Flask,render_template,redirect,url_for,current_app,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,FileField,SubmitField,TimeField,PasswordField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileAllowed,FileField
from PIL import Image
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,LoginManager,login_user,current_user, logout_user, login_required
import email_validator

app = Flask(__name__)

app.config['SECRET_KEY']  = "mysecretkey"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class menu(db.Model):
    
    __tablename__ = "menu"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    price = db.Column(db.Integer)
    image = db.Column(db.Text, default='default.png')
    from_time = db.Column(db.Text)
    to_time = db.Column(db.Text)
    abs_from_time = db.Column(db.Time)
    abs_to_time = db.Column(db.Time)
    
    def __init__(self,name,price,image,from_time,to_time,abs_from_time,abs_to_time):
        self.name = name
        self.price = price
        self.image = image
        self.from_time = from_time
        self.to_time = to_time
        self.abs_from_time = abs_from_time
        self.abs_to_time = abs_to_time
        
        
@login_manager.user_loader
def load_user(id):
    return signup.query.get(id)

class signup(db.Model,UserMixin):
    
    __tablename__ = "signup"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    
    def __init__(self,email,password):
        self.email = email
        self.password_hash = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
            
class MenuForm(FlaskForm):
    
    item_name = StringField("Enter Item Name ")
    item_price = IntegerField("Enter Item Price ")
    image = FileField("Upload item image (if available)",validators=[FileAllowed(['jpg','png'])])
    from_time = TimeField("From",format="%H:%M")
    to_time = TimeField("To",format="%H:%M")
    submit = SubmitField("Add Item")
    
class UpdateTimeForm(FlaskForm):
    
    from_time = TimeField("From",format="%H:%M")
    to_time = TimeField("To",format="%H:%M")
    submit = SubmitField("Update Time")
    
class LoginForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
class SignupForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_pass',message='Password doesnot match')])
    confirm_pass = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("SignUp")
    
    def check_email(self,field):
        if signup.query.filter_by(email=field.data).first():
            raise ValidationError("Email is already registered")

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/signup',methods=['GET','POST'])
def Signup():
    
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = signup(email,password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        user = signup.query.filter_by(email = form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next==None or not next[0]=='/':
                    next = url_for('customer')
                return redirect(next)
    return render_template('login.html',form=form)
    
@app.route('/logout')
def logout():
    
    logout_user()
    return redirect(url_for('login'))


@app.route('/uploadMenu',methods=['GET','POST'])
def uploadMenu():
    
    form = MenuForm()
    Converted_from_time=0
    Converted_to_time=0
    if form.validate_on_submit():
        name = form.item_name.data
        price = form.item_price.data
        f_time = form.from_time.data
        t_time = form.to_time.data
        d_from_time = datetime.strptime(str(f_time), "%H:%M:%S")
        Converted_from_time = str(d_from_time.strftime("%I:%M %p"))
        d_to_time = datetime.strptime(str(t_time), "%H:%M:%S")
        Converted_to_time = str(d_to_time.strftime("%I:%M %p"))
        if form.image.data:
            item_name = name
            image = addimage(form.image.data,item_name)
            newItem = menu(name,price,image,Converted_from_time,Converted_to_time,f_time,t_time)
            db.session.add(newItem)
            db.session.commit()
        else:
            newItem = menu(name,price,'default.png',Converted_from_time,Converted_to_time,f_time,t_time)
            db.session.add(newItem)
            db.session.commit()
        return redirect(url_for('viewMenu'))
    return render_template('uploadMenu.html',form=form)

def addimage(uploaded_pic,item_name):
    
    filename = uploaded_pic.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(item_name)+'.'+ext_type
    filepath = os.path.join(current_app.root_path,'static/food_pics',storage_filename)
    output_size = (300,300)
    pic = Image.open(uploaded_pic)
    pic.thumbnail(output_size)
    pic.save(filepath)
    
    return storage_filename

@app.route('/deleteMenu/<id>')
def deleteMenu(id):
    delete_item = menu.query.get(id)
    print(delete_item)
    db.session.delete(delete_item)
    db.session.commit()
    
    return redirect(url_for('viewMenu'))

@app.route('/updateTime/<id>',methods=['GET','POST'])
def updateTime(id):
    form = UpdateTimeForm()
    if form.validate_on_submit():
        updtTime = menu.query.get(id)
        updateTime.abs_from_time = form.from_time.data
        updateTime.abs_to_time = form.to_time.data
        f_time = form.from_time.data
        t_time = form.to_time.data
        d_from_time = datetime.strptime(str(f_time), "%H:%M:%S")
        Converted_from_time = str(d_from_time.strftime("%I:%M %p"))
        d_to_time = datetime.strptime(str(t_time), "%H:%M:%S")
        Converted_to_time = str(d_to_time.strftime("%I:%M %p"))
        updtTime.from_time = Converted_from_time
        updtTime.to_time = Converted_to_time
        db.session.add(updtTime)
        db.session.commit()
        
        return redirect(url_for('viewMenu'))
    return render_template('updateTime.html',form = form)

@app.route('/viewMenu')
def viewMenu():
    compMenu = menu.query.all()
    return render_template('viewMenu.html', compMenu=compMenu)

@app.route('/customer')
@login_required
def customer():
    return render_template('customer.html')

if __name__=='__main__':
    app.run(debug=True)
