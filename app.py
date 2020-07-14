from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, current_app
#from data import Articles
from flask_mysqldb import MySQL
#import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, FileField
from passlib.hash import sha256_crypt
from functools import wraps
#import mysql.connector
#from mysql.connector import Error
import os
import cv2
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from PIL import Image
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sagar'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQLs
mysql = MySQL(app)

path = '//home//sagarms//Desktop//flaskapp//env//static//images//grabcut//grabcut.jpg'
model = load_model('//home//sagarms//Desktop//flaskapp//env//final_model_level1.h5')
model1 = load_model('//home//sagarms//Desktop//flaskapp//env//final_model_disease_level_2.h5')

# Index
@app.route('/')
def home():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')

# complient form
@app.route('/complient')
def complient():
    #flash("complaints registered here are also handled by experts. Updated at Discussion Board.","success")
    return render_template('suggestion_form.html')

#service-worker
@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

# FormerRegister Form Class
class RegisterForm1(Form):
    name = StringField('', [validators.DataRequired(),validators.Length(min=1, max=50)])
    phno = StringField('', [validators.DataRequired(),validators.Length(min=10, max=10)])
    email = StringField('', [validators.DataRequired(),validators.Length(min=6, max=50)])
    address=StringField('',[validators.DataRequired(),validators.Length(min=10,max=50)])
    username = StringField('', [validators.DataRequired(),validators.Length(min=4, max=25)])
    password = PasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('',[validators.DataRequired()])

#former_reg
@app.route('/former_register', methods=['GET', 'POST'])
def former_register():
    form = RegisterForm1(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        phno=form.phno.data
        email = form.email.data
        address=form.address.data
        username = form.username.data
        password=form.password.data
        #password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO former(name, phno, email, address, uname, password) VALUES(%s, %s, %s, %s,%s,%s)", (name,phno, email,address, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        #flash('You are now registered and can log in', 'success')

        return redirect(url_for('former_login'))
    return render_template('former_register.html', form=form)

# Former login
@app.route('/former_login', methods=['GET', 'POST'])
def former_login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM former WHERE uname = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            #if sha256_crypt.verify(password_candidate, password):
            if(password_candidate==password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                #flash("hello",'success')
                #flash('You are now logged in', 'success')
                #return redirect(url_for('former_dashboard'))
                return render_template('home_former.html')
            else:
                error = 'Invalid Password'
                #flash('Invalid Password','danger')
                return render_template('former_login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'username doesnt exists !! Please register and try again'
            #flash('username doesnt exists !! Please register and try again','danger')
            return render_template('former_login.html', error=error)

    return render_template('former_login.html')


# expertRegister Form Class
class RegisterForm2(Form):
    name = StringField('', [validators.DataRequired(),validators.Length(min=1, max=50)])
    phno = StringField('', [validators.DataRequired(),validators.Length(min=10, max=10)])
    email = StringField('', [validators.DataRequired(),validators.Length(min=6, max=50)])
    address=StringField('',[validators.DataRequired(),validators.Length(min=10,max=50)])
    username = StringField('', [validators.DataRequired(),validators.Length(min=4, max=25)])
    password = PasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('',[validators.DataRequired()])

#expert_reg
@app.route('/expert_register', methods=['GET', 'POST'])
def expert_register():
    form = RegisterForm2(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        phno=form.phno.data
        email = form.email.data
        address=form.address.data
        username = form.username.data
        password=form.password.data
        #password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO expert(name, phno, email, address, uname, password) VALUES(%s, %s, %s, %s,%s,%s)", (name,phno, email,address, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        #flash('You are now registered and can log in', 'success')

        return redirect(url_for('expert_login'))
    return render_template('expert_register.html', form=form)

# expert login
@app.route('/expert_login', methods=['GET', 'POST'])
def expert_login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM expert WHERE uname = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            #if sha256_crypt.verify(password_candidate, password):
            if(password_candidate==password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                #flash('You are now logged in', 'success')
                return redirect(url_for('display_all_img'))
                #return render_template('home_expert.html')
            else:
                error = 'Invalid login'
                return render_template('expert_login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('expert_login.html', error=error)

    return render_template('expert_login.html')


#insert img into db class
#APP_IMAGES = os.path.join(APP_ROOT, 'images/test_img/')
class insertimg(Form):
    name = StringField('desc')
    file = FileField('file')

#insert img to table
@app.route('/insert_img_db', methods=['GET', 'POST'])
def insert_img_db():
    desc=request.form['desc']
    file=request.files['file']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO description(descri,test_img) VALUES(%s, %s)", (desc,file))
    mysql.connection.commit()
    cur.close()
    #flash('You are now registered and can log in', 'success')
    return render_template('home_expert.html')
      



# Dashboard former
@app.route('/former_dashboard')
def former_dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM former")
    data = cur.fetchall()
    cur.close()
    return render_template('former_dashboard.html', former=data )

# Dashboard expert
@app.route('/expert_dashboard')
def expert_dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM expert")
    data = cur.fetchall()
    cur.close()
    return render_template('expert_dashboard.html', expert=data )

#notification
@app.route('/notification')
def notification():
    cur = mysql.connection.cursor()
    pics = os.listdir('//home//sagarms//Desktop//flaskapp//env//static//images//upload')  
    #return render_template("home_expert.html", pics=pics)
    cur.execute("SELECT  descri FROM description")
    data = cur.fetchall()
    cur.close()
    return render_template('former_notification.html', description=data,pics=pics )

#update former details
@app.route('/update',methods=['POST','GET'])
def update_f():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phno']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE former
               SET name=%s, phno=%s, address=%s
               WHERE email=%s
            """, (name,phone,address, email))
        #flash("Data Updated Successfully",'success')
        mysql.connection.commit()
        return redirect(url_for('former_dashboard'))

#delete former
@app.route('/delete_f/<string:email>', methods = ['GET'])
def delete_f(email):
    flash("Record Has Been Deleted Successfully",'success')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM former WHERE email=%s", (email,))
    mysql.connection.commit()
    return redirect(url_for('former_dashboard'))


#update expert details
@app.route('/update',methods=['POST','GET'])
def update_e():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phno']
        address = request.form['address']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE expert
               SET name=%s, phno=%s, address=%s
               WHERE email=%s
            """, (name,phone,address, email))
        #flash("Data Updated Successfully",'success')
        mysql.connection.commit()
        return redirect(url_for('expert_dashboard'))

#delete expert
@app.route('/delete_e/<string:email>', methods = ['GET'])
def delete_e(email):
    flash("Record Has Been Deleted Successfully",'success')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM expert WHERE email=%s", (email,))
    mysql.connection.commit()
    return redirect(url_for('expert_dashboard'))

#selected img name
app.config["IMAGE_UPLOADS"] = "//home//sagarms//Desktop//flaskapp//env//static//images//upload"
@app.route("/upload-image", methods=["GET", "POST"])
def upload_image(): 
    try:
        #flash("Image saved Successfully",'success')
        if request.method == "POST":
            if request.files:
                image = request.files["file"]
            #image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
           # basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                   app.config["IMAGE_UPLOADS"], secure_filename(image.filename))
           
            image.save(file_path)
            crop(file_path)
            res = run_example()
            if res > 0.3:
                a ="unhealthy"
                res1 = run_example1()
                if res1 > 0.3:
                    #b = "sigatoka"
                    b="The Prediction Status is:unhealthy"
                    dtype="SIGATOKA"
                    remedy="Management mainly involves chemical control using fungicides like copper oxychloride, mancozeb, chlorothalonil or carbendazim at the prescribed dosage. Fungicide spraying on the foliage and pseudostem should be commenced with the initial appearance and repeated at two weeks"
                    #flash("predicted as SIGATOKA",'danger')
                    #flash("REMEDY :  Management mainly involves chemical control using fungicides like copper oxychloride, mancozeb, chlorothalonil or carbendazim at the prescribed dosage. Fungicide spraying on the foliage and pseudostem should be commenced with the initial appearance and repeated at two weeks",'success')
                else:
                    #b = "panama"
                    dtype="Bacterial Wilt"
                    remedy="Severely affected plants should be uprooted and burnt. Highly infected soil should not be replanted with banana at least for 3-4 years. Use of disease-free planting material and resistant cultivar are recommended. Growing of paddy followed by banana for 3-5 years once or twice, use of quick lime near the base of the plant and soaking with water and avoiding sunflower or sugarcane in crop rotation helps to reduce the disease incidence. Dipping of suckers in Carbendazim (10g/10 litres of water) followed by bimonthly drenching starting from 6 months after planting is also recommended. Application of bioagents, such as, Trichoderma viride or Pseudomonas fluorescence in the soil is effective."
            #         flash("predicted as PANAMA",'danger')
            #         flash("REMEDY : Severely affected plants should be uprooted and burnt. Highly infected soil should not be replanted with banana at least for 3-4 years. Use of disease-free planting material and resistant cultivar are recommended. Growing of paddy followed by banana for 3-5 years once or twice, use of quick lime near the base of the plant and soaking with water and avoiding sunflower or sugarcane in crop rotation helps to reduce the disease incidence. Dipping of suckers in Carbendazim (10g/10 litres of water) followed by bimonthly drenching starting from 6 months after planting is also recommended. Application of bioagents, such as, Trichoderma viride or Pseudomonas fluorescence in the soil is effective.",'success')
            else:
                a ="healthy"
                dtype="Their is no disease to this plant"
                remedy="No need"
    except:
        flash("Please upload a proper image","danger")
        return render_template('suggestion_form.html')

        # return redirect(request.url)
    #return render_template("suggestion_form.html")
    return render_template('suggestion_form.html', prediction_text1='The Prediction Status is: {}'.format(a),dtype='Name of disease is: {}'.format(dtype),remedy='Remedy for disease is: {}'.format(remedy))

def crop(image):
    y1 = 161
    y2 = 1050
    x1 = 166
    x2 = 706

    #img = cv2.imread('D://minor project 4th sem/flaskapp/env/static/images/upload/s7.jpeg')
    img = cv2.imread(image)
    crop_img = img[y1:y2 , x1:x2]
    mask = np.zeros(crop_img.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    rect = (90,90,1200,860)
    cv2.grabCut(crop_img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img1 = crop_img*mask2[:,:,np.newaxis]

#new_img1 = Image.fromarray(img1)
    cv2.imwrite(path,img1)

 
# load and prepare the image
def load_image(filename):
	# load the image
	img = load_img(filename, target_size=(224, 224))
	# convert to array
	img = img_to_array(img)
	# reshape into a single sample with 3 channels
	img = img.reshape(1, 224, 224, 3)
	# center pixel data
	img = img.astype('float32')
	img = img - [123.68, 116.779, 103.939]
	return img

# load an image and predict the class
def run_example():
    img = load_image(path)
    #model = load_model('final_model.h5')
    result = model.predict(img)
    #print('Accuracy: \n', accuracy_score(img,result.round(),normalize=False))
    return (result[0])
    #if result[0] > 0.3:
     #   print('unhealthy')
        #run_example1()
    #else:
     #       print('healthy')

def run_example1():
    img = load_image(path)
    #model = load_model('final_model_disease.h5')
    result = model1.predict(img)
    return (result[0])
    #if result[0] > 0.5:
     #   print('sigatoka')
      #  print("REMEDY : Management mainly involves chemical control using fungicides like copper oxychloride, mancozeb, chlorothalonil or carbendazim at the prescribed dosage. Fungicide spraying on the foliage and pseudostem should be commenced with the initial appearance and repeated at two weeks")
    #else:
     #       print('panama wilt')
      #      print('REMEDY : Severely affected plants should be uprooted and burnt. Highly infected soil should not be replanted with banana at least for 3-4 years. Use of disease-free planting material and resistant cultivar are recommended. Growing of paddy followed by banana for 3-5 years once or twice, use of quick lime near the base of the plant and soaking with water and avoiding sunflower or sugarcane in crop rotation helps to reduce the disease incidence. Dipping of suckers in Carbendazim (10g/10 litres of water) followed by bimonthly drenching starting from 6 months after planting is also recommended. Application of bioagents, such as, Trichoderma viride or Pseudomonas fluorescence in the soil is effective.')



#Retrive img from folder
@app.route('/display_all_img')  
def display_all_img():  
    pics = os.listdir('//home//sagarms//Desktop//flaskapp//env//static//images//upload')  
    return render_template("home_expert.html", pics=pics)

#test the selected img
app.config["IMAGE_UPLOADS"] ="//home//sagarms//Desktop//flaskapp//env//static//images//upload"
@app.route("/testing_img", methods=["GET", "POST"])
def testing_img():
    flash("Image saved Successfully",'success')
    if request.method == "POST":
        if request.files:
            desc=request.form['desc']
            image = request.files["file"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO description(descri,test_img) VALUES(%s, %s)", (desc,image))
            mysql.connection.commit()
            cur.close()
            flash('You are uploded your result', 'success')
        return render_template('home_expert.html')
            # image = request.files["file"]
            # image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
        # return redirect(request.url)
   # return render_template("home_expert.html")


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
	
	
# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out successfully..Thank you for using our website', 'success')
    #return redirect(url_for('home'))
    return render_template('home.html')


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)