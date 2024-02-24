from flask import Flask,render_template,redirect,url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/uploadMenu')
def uploadMenu():
    return render_template('uploadMenu.html')

if __name__=='__main__':
    app.run(debug=True)
