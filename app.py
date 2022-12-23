from ast import dump
from flask import * 
from glob import glob 
import os
from io import BytesIO
from zipfile import ZipFile
from flask import after_this_request
import io




app = Flask(__name__) 

app.static_folder = 'static'

UPLOAD_FOLDER = r"D:\xamppnew\htdocs\cv-man\UPLOAD_FOLDER"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

keyword = []



@app.route('/')  
def index(): 
    return render_template("index.html")  

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files.getlist("file")
        for i in f:
            i.save(os.path.join(app.config['UPLOAD_FOLDER'], i.filename))  
        key = request.form['k']  
        return render_template("keywords.html", number = int(key))  



@app.route('/submitted', methods = ['POST']) 
def submitted():
    from main import mainf  
    if request.method == 'POST':
        keyword.append(request.form.getlist('kw'))
        mainf(keyword)
        re = r'D:\xamppnew\htdocs\cv-man\result\\'
        with ZipFile(r"D:\xamppnew\htdocs\cv-man\result\result.zip", 'w') as zip:
            for file in glob(os.path.join(re, '*.pdf')):
                zip.write(file, os.path.basename(file))
        return render_template("result.html")



@app.route('/result', methods = ['GET']) 
def result(): 
    zipfile = glob(r"D:\xamppnew\htdocs\cv-man\result\*")
    fname = glob(r"D:\xamppnew\htdocs\cv-man\UPLOAD_FOLDER\*.pdf")
    file_path = r"D:\xamppnew\htdocs\cv-man\result\result.zip"
    rd = io.BytesIO()
    if request.method == 'GET':
        with open(file_path, 'rb') as fo:
            rd.write(fo.read())
        rd.seek(0)
#for loops to remove ramining files
        os.remove(file_path)
        for i in fname: 
            if os.path.isfile(i):
                os.remove(i)
        for k in zipfile: 
            if os.path.isfile(k):
                os.remove(k)      
        #This sends the data stored in buffer to the user
        return send_file(rd, mimetype='application/zip',
                     download_name='result.zip')


if __name__ == '__main__':  
    app.run(host= 'localhost', debug = True) 


