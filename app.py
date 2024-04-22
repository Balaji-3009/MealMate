import os
from flask import Flask,render_template,redirect,url_for,current_app,request,session,flash
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
import json

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
    role = db.Column(db.Text)
    
    def __init__(self,email,password,role):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role
        
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
 

class cart(db.Model):
    
    __tablename__ = "cart"
    sno = db.Column(db.Integer,primary_key=True)
    item_name = db.Column(db.Text)
    item_price = db.Column(db.Integer)
    quantity = db.Column(db.Integer,default=1)
    total_price = db.Column(db.Integer)
    image =  db.Column(db.Text, default='default.png')
    customer = db.Column(db.Text)
    
    def __init__(self,item_name,item_price,quantity,total_price,image,customer):
        self.item_name = item_name
        self.item_price = item_price
        self.quantity = quantity
        self.total_price = total_price
        self.image = image
        self.customer = customer


class orders(db.Model):
    
    __tablename__ = "orders"
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.Text)
    order = db.Column(db.Text)
    total_price = db.Column(db.Integer)
    time = db.Column(db.Text)
    
    def __init__(self,id,email,order,total_price,time):
        self.id = id
        self.email = email
        self.order = json.dumps(order)
        self.total_price = total_price
        self.time = time 
        

class orderId(db.Model):
    __tablename__ = "orderId"
    sno = db.Column(db.Integer,primary_key = True)
    id = db.Column(db.Integer)
    
    def __init__(self,id):
        self.id = id


class MenuForm(FlaskForm):
    
    item_name = StringField("Enter Item Name ")
    item_price = IntegerField("Enter Item Price ")
    image = FileField("Upload item image",validators=[FileAllowed(['jpg','png'])])
    from_time = TimeField("From",format="%H:%M")
    to_time = TimeField("To",format="%H:%M")
    submit = SubmitField("Add Item")
    
class UpdateTimeForm(FlaskForm):
    
    from_time = TimeField("From",format="%H:%M")
    to_time = TimeField("To",format="%H:%M")
    submit = SubmitField("Update Time")
    
class LoginForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(),Email()],render_kw={"autocomplete": "off"})
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
class SignupForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(),Email()],render_kw={"autocomplete": "off"})
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_pass',message='Password doesnot match')])
    confirm_pass = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("SignUp")
    
    def validate_email(self,field):
        if signup.query.filter_by(email=field.data).first():
            flash("This Email has already been registered")
            raise ValidationError("Email is already registered")
        
class emp_LoginForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(),Email()],render_kw={"autocomplete": "off"})
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
class emp_SignupForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(),Email()],render_kw={"autocomplete": "off"})
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_pass',message='Password doesnot match')])
    confirm_pass = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("SignUp")
    
    def validate_email(self,field):
        if signup.query.filter_by(email=field.data).first():
            raise ValidationError("Email is already registered")
        
class UpdateQuantity(FlaskForm):
    
    quantity = IntegerField("Quantity")
    submit = SubmitField("Update Quantity")


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/employee')
def employee():
    if current_user.is_authenticated and current_user.role == 'employee':
        return render_template('main.html')
    else:
        return render_template('emp_only.html')

@app.route('/signup',methods=['GET','POST'])
def Signup():
    
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = 'customer'
        user = signup(email,password,role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)

@app.route('/emp_signup',methods=['GET','POST'])
def emp_Signup():
    
    form = emp_SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = 'employee'
        user = signup(email,password,role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('emp_login'))
    return render_template('emp_signup.html',form=form)

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
            else:
                flash("Password is incorrect")
    return render_template('login.html',form=form)

@app.route('/emp_login',methods=['GET','POST'])
def emp_login():
    
    form = emp_LoginForm()
    if form.validate_on_submit():
        user = signup.query.filter_by(email = form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next==None or not next[0]=='/':
                    next = url_for('employee')
                return redirect(next)
    return render_template('emp_login.html',form=form)
    
@app.route('/logout')
def logout():
    
    logout_user()
    return redirect(url_for('index'))


@app.route('/deleteUser/<id>')
def deleteUser(id):
    
    user = signup.query.get(id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for('login'))


@app.route('/uploadMenu',methods=['GET','POST'])
@login_required
def uploadMenu():
    if current_user.role == 'employee':
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
    else:
        return render_template('emp_only.html')

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
@login_required
def deleteMenu(id):
    if current_user.is_authenticated and current_user.role == 'employee':
        delete_item = menu.query.get(id)
        db.session.delete(delete_item)
        db.session.commit()
        
        return redirect(url_for('viewMenu'))
    else:
        return render_template('emp_only.html')

@app.route('/updateTime/<id>',methods=['GET','POST'])
@login_required
def updateTime(id):
    session['update_id'] = id
    return redirect(url_for('final_updateTime'))
    
@app.route('/final_updateTime',methods=['GET','POST'])
@login_required
def final_updateTime():
    if current_user.is_authenticated and current_user.role == 'employee':
        op=1
        id = session.get('update_id')
        compMenu = menu.query.all()
        form = UpdateTimeForm()
        if form.validate_on_submit():
            updtTime = menu.query.get(id)
            updtTime.abs_from_time = form.from_time.data
            updtTime.abs_to_time = form.to_time.data
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
            op=0
            
            return redirect(url_for('viewMenu'))
        return render_template('viewMenu.html', form = form,op=op,compMenu = compMenu,id=id)
    else:
        return render_template('emp_only.html')

@app.route('/viewMenu')
@login_required
def viewMenu():
    if current_user.is_authenticated and current_user.role == 'employee':
        compMenu = menu.query.all()
        op=0
        return render_template('viewMenu.html', compMenu=compMenu,op=op)
    else:
        return render_template('emp_only.html')


@app.route('/customer')
@login_required
def customer():
    if current_user.is_authenticated and current_user.role == 'customer':
        return render_template('customer_main.html')
    else:
        return render_template('cust_only.html')


@app.route('/customer_menu')
@login_required
def customer_menu():
    if current_user.is_authenticated and current_user.role == 'customer':
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        compMenu = menu.query.filter(menu.abs_from_time<=current_time,menu.abs_to_time>=current_time).all()
        return render_template('customer_menu.html',compMenu=compMenu)
    else:
        return render_template('cust_only.html')
    
    
@app.route('/add_to_cart/<id>')
def add_to_cart(id):
    item = menu.query.get(id)
    item_name = item.name
    item_price = item.price
    quantity = 1
    total_price = item_price*quantity
    image = item.image
    customer = current_user.email
    add_cart = cart(item_name,item_price,quantity,total_price,image,customer)
    db.session.add(add_cart)
    db.session.commit()
    return redirect(url_for('Cart'))


@app.route('/cart')
def Cart():
    
    if current_user.is_authenticated and current_user.role == 'customer':
        email = current_user.email
        items = cart.query.filter_by(customer=email)
        count = 0
        opp = 0
        for i in items:
            count+=1
        if count>0:
            return render_template('cart.html',items=items,opp=opp)
        else:
            return render_template('empty_cart.html')
    else:
        return render_template('cust_only.html')
    
    
@app.route('/updateQuantity/<sno>',methods=['GET','POST'])
@login_required
def updateQuantity(sno):
    session['update_sno'] = sno
    return redirect(url_for('final_updateQuantity'))


@app.route('/final_updateQuantity',methods=['GET','POST'])
@login_required
def final_updateQuantity():
    if current_user.is_authenticated and current_user.role == 'customer':
        opp=1
        sno = session.get('update_sno')
        email = current_user.email
        items = cart.query.filter_by(customer = email)
        form = UpdateQuantity()
        if form.validate_on_submit():
            item = cart.query.get(sno)
            item.quantity = form.quantity.data
            item.total_price = form.quantity.data * item.item_price
            db.session.add(item)
            db.session.commit()
            op=0
            
            return redirect(url_for('Cart'))
        return render_template('cart.html', form = form,opp=opp,items = items,sno=sno)
    else:
        return render_template('cust_only.html')


@app.route('/deleteCart/<sno>')
@login_required
def deleteCart(sno):
    if current_user.is_authenticated and current_user.role == 'customer':
        delete_item = cart.query.get(sno)
        db.session.delete(delete_item)
        db.session.commit()
        
        return redirect(url_for('Cart'))
    else:
        return render_template('cust_only.html')
    
    
@app.route('/bill')
@login_required
def bill():
    if current_user.is_authenticated and current_user.role == 'customer':
        email = current_user.email
        items = cart.query.filter_by(customer=email)
        final_price = 0
        for item in items:
            final_price += item.total_price
        return render_template('bill.html',items = items,email=email,final_price=final_price)
        
    else:
        return render_template('cust_only.html')


@app.route('/placeOrder')
@login_required
def placeOrder():
    if current_user.is_authenticated and current_user.role == 'customer':
        email = current_user.email
        items = cart.query.filter_by(customer=email)
        final_price = 0
        order=[]
        for item in items:
            final_price += item.total_price
            order.append([item.item_name,item.quantity])
        
        ordId = orderId.query.get(1)
        id = ordId.id + 1
        
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        
        new_order = orders(id,email,order,final_price,current_time)
        db.session.add(new_order)
        db.session.commit()
        for item in items:
            db.session.delete(item)
            db.session.commit()
            
        ordId.id = id
        db.session.add(ordId)
        db.session.commit()
        
        return render_template('payment_success.html')
        
    else:
        return render_template('cust_only.html')


@app.route('/viewOrders')
@login_required
def viewOrders():
    if current_user.is_authenticated and current_user.role == 'employee':
        orders_ = orders.query.all()
        count = 0
        for i in orders_:
            count+=1
        if count>0:
            list_of_orders = []
            all_orders = orders.query.all()
            
            for order_ in all_orders:
                id = order_.id
                email = order_.email
                items = json.loads(order_.order)
                price = order_.total_price
                time = order_.time
                list_of_orders.append([id,email,items,price,time])
            return render_template('viewOrders.html',list_of_orders = list_of_orders)
        else:
            return 'NO Orders'
        
    else:
        return render_template('emp_only.html')


@app.route('/pendingOrders')
@login_required
def pendingOrders():
    if current_user.is_authenticated and current_user.role == 'customer':
        list_of_orders = []
        email = current_user.email
        all_orders = orders.query.filter_by(email=email)
        for order_ in all_orders:
            email = order_.email
            items = json.loads(order_.order)
            price = order_.total_price
            id = order_.id
            time = order_.time
            list_of_orders.append([email,items,price,id,time])
        return render_template('pendingOrders.html',list_of_orders = list_of_orders)
    else:
        return render_template('cust_only.html')


@app.route('/deleteOrder/<id>')
@login_required
def deleteOrder(id):
    if current_user.is_authenticated and current_user.role == 'employee':
        delete_order = orders.query.get(id)
        db.session.delete(delete_order)
        db.session.commit()
        return redirect(url_for('viewOrders'))
    else:
        return render_template('emp_only.html')


@app.route('/initOrderId')
def initOrderId():
    id = 1
    ordId = orderId(id)
    db.session.add(ordId)
    db.session.commit()
    return "order id initialized"

if __name__=='__main__':
    app.run(debug=True)
