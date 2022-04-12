from flask import Flask, url_for, redirect, render_template, url_for, session, logging, request
import pyrebase
import PyPDF2
import requests


URL = "https://api.meaningcloud.com/summarization-1.0"
app = Flask(__name__)


@app.route('/summarise')
def summarise_form():
    return render_template("summarise.html")


@app.route('/summarisePDF', methods = ['POST'])
def summrisePDF():
    if request.method == 'POST':
        f = request.files['file']  
        f.save(f.filename)
        pdfFileObj = open(f.filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print(pdfReader.numPages)
        pageObj = pdfReader.getPage(0)
        x=pageObj.extractText()
        txt=x
        key="73753b7cbc31fb6c4969cdd4f428d58d"
        sentences=3
        PARAMS = {"key":key,"txt":txt, "sentences":sentences}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        return render_template("summarise.html", name=data['summary'])

@app.route('/summarise', methods = ['POST'])
def summrise():
    if request.method == 'POST':
        int_features=[x for x in request.form.values()]
        print(int_features)
        txt=int_features[0]
        key="73753b7cbc31fb6c4969cdd4f428d58d"
        sentences=3
        PARAMS = {"key":key,"txt":txt, "sentences":sentences}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        return render_template("summarise.html", name=data['summary'])

firebaseConfig = {
    'apiKey': "AIzaSyDubGncgvqCMzWktTMOChPntjfgMITmTcc",
    'authDomain': "visara-5a513.firebaseapp.com",
    'projectId': "visara-5a513",
    'storageBucket': "visara-5a513.appspot.com",
    'messagingSenderId': "582687989459",
    'appId': "1:582687989459:web:7e005b599c09faa8a93e26",
    'measurementId': "G-0NY6VG8PBT",
    "databaseURL" : "https://visara-5a513-default-rtdb.asia-southeast1.firebasedatabase.app/"
    }
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db=firebase.database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/patient')
def patient():
    return render_template('patient.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/posebots')
def posebots():
    return render_template('posebots.html')

@app.route('/posebot')
def posebot():
    return render_template('posebot.html')


@app.route('/palming',methods=['POST','GET'])
def palming():
    url="https://teachablemachine.withgoogle.com/models/vKItIykyq/"
    return render_template('posebot.html', url=url)

@app.route('/trataka',methods=['POST','GET'])
def trataka():
    url="https://teachablemachine.withgoogle.com/models/YBbEKwztQ/"
    return render_template('posebot.html', url=url)

@app.route('/bhramamudra',methods=['POST','GET'])
def bhramamudra():
    url="https://teachablemachine.withgoogle.com/models/znvpEncRJ/"
    return render_template('posebot.html', url=url)

@app.route('/pranayama',methods=['POST','GET'])
def pranayama():
    url="https://teachablemachine.withgoogle.com/models/ZW47sepej/"
    return render_template('posebot.html', url=url)

@app.route('/parvatasana',methods=['POST','GET'])
def parvatasana():
    url="https://teachablemachine.withgoogle.com/models/JnfkxNVh3/"
    return render_template('posebot.html', url=url)

@app.route('/login/patient',methods=['POST','GET'])
def login_patient():
    flag=0
    flag2=0
    int_features=[x for x in request.form.values()]
    print(int_features)
    name=int_features[0]
    email=int_features[1]
    password=int_features[2]
    users = db.child("Patient").child(name).get()
    if(users.each()!=None):
        flag2=1
        for user in users.each():
            if(user.val()==email):
                print('found')
                flag=1
    if(flag==1 and flag2==1):
        try:
            auth.sign_in_with_email_and_password(email, password)
            print("Patient Succesfully SignedIn")
            return render_template('patient.html', name=name) 
        except:
            print("Invalid User Or Password")
    return render_template('login.html')

@app.route('/login/doctor',methods=['POST','GET'])
def login_doctor():
    flag=0
    flag2=0
    int_features=[x for x in request.form.values()]
    print(int_features)
    name=int_features[0]
    email=int_features[1]
    password=int_features[2]
    users = db.child("Doctors").child(name).get()
    if(users.each()!=None):
        flag2=1
        for user in users.each():
            if(user.val()==email):
                print('found')
                flag=1
    if(flag==1 and flag2==1):
        try:
            auth.sign_in_with_email_and_password(email, password)
            print("Doctor Succesfully SignedIn")
            return render_template('doctor.html', name=name) 
        except:
            print("Invalid User Or Password")
    return render_template('login.html')


@app.route('/signup/doctor',methods=['POST','GET'])
def signup_doctor():
    int_features=[x for x in request.form.values()]
    print(int_features)
    name=int_features[0]
    email=int_features[1]
    password=int_features[2]
    confirmpasswd=int_features[3]
    designation=int_features[4]
    hospital=int_features[5]
    if(password==confirmpasswd):
        try:
            auth.create_user_with_email_and_password(email,password)
            print("Doctor Created")
            data={"name":name, "email": email, "designation":designation, "hospital":hospital }
            print(email)
            db.child("Doctors").child(name).set(data)
            return render_template('doctor.html', name=name)
        except:
            print("Email already Exists")
    return render_template('signup.html')

@app.route('/signup/patient',methods=['POST','GET'])
def signup_patient():
    int_features=[x for x in request.form.values()]
    print(int_features)
    name=int_features[0]
    email=int_features[1]
    password=int_features[2]
    confirmpassword=int_features[3]
    height=int_features[4]
    weight=int_features[5]
    age=int_features[6]
    if(password==confirmpassword):
        try:
            auth.create_user_with_email_and_password(email,password)
            print("Patient Created")
            data={"name":name, "email": email, "age":age, "height":height, "weight":weight}
            print(email)
            db.child("Patient").child(name).set(data)
            return render_template('patient.html', name=name)
        except:
            print("Email already Exists")
    return render_template('signup.html')


@app.route('/view_patients', methods=['POST','GET'])
def view_patients():
    patients=[]
    users = db.child("Patient").get()
    for user in users.each():
        patients.append(user.val())
    print(patients)
    return render_template('patientlist.html', patients=patients)

@app.route('/report', methods=['POST','GET'])
def report():
    patients=[]
    users = db.child("Patient").get()
    for user in users.each():
        patients.append(user.val())
    int_features=[x for x in request.form.values()]
    print(int_features)
    name=int_features[0]
    report=int_features[1]
    db.child("Patient").child(name).update({"report":report})
    return redirect('/view_patients')

@app.route('/patientreport', methods=['POST','GET'])
def patientreport():
    int_features=[x for x in request.form.values()]
    print(int_features)
    name=int_features[0]
    details = db.child("Patient").child(name).get()
    patient=details.val()
    return render_template('report.html', name=name, x=patient)

@app.route('/recommend', methods=['POST','GET'])
def recommend():
    int_features=[x for x in request.form.values()]
    print(int_features)
    name=int_features[0]
    details = db.child("Patient").child(name).get()
    dr=(details.val()['dr'])
    return render_template('posebots.html', name=name, dr=dr)



if __name__ == '__main__':
    app.run(debug=True)


