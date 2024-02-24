import os
from flask import Flask,render_template,redirect,url_for,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,FileField,SubmitField
from flask_wtf.file import FileAllowed,FileField
from PIL import Image

app = Flask(__name__)

app.config['SECRET_KEY']  = "mysecretkey"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Menu(db.Model):
    
    __tablename__ = "menu"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    price = db.Column(db.Integer)
    image = db.Column(db.Text, default='default.png')
    
    def __init__(self,name,price,image):
        self.name = name
        self.price = price
        self.image = image
        
class MenuForm(FlaskForm):
    
    item_name = StringField("Enter Item Name ")
    item_price = IntegerField("Enter Item Price ")
    image = FileField("Upload item image")
    submit = SubmitField("Add Item")

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/uploadMenu',methods=['GET','POST'])
def uploadMenu():
    
    form = MenuForm()
    if form.validate_on_submit():
        name = form.item_name.data
        price = form.item_price.data
        
        if form.image.data:
            print("recieved image")
            item_name = name
            image = addimage(form.image.data,item_name)
            newItem = Menu(name,price,image)
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

@app.route('/viewMenu')
def viewMenu():
    
    return render_template('viewMenu.html')

if __name__=='__main__':
    app.run(debug=True)
