import streamlit as st
import tensorflow as tf
from random import randint
import pyrebase


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
st.title("Visara")
  
html_temp = """
    <div style="background:linear-gradient(to bottom, #66ccff 0%, #ff99cc 100%);padding:10px">
    <h1 style="color:white;text-align:center;"><em>EyeDR</em> </h1>
    </div>
    <br></br>
    """
st.markdown(html_temp,unsafe_allow_html=True)

st.set_option('deprecation.showfileUploaderEncoding',False)
@st.cache(allow_output_mutation=True)
def load_model():
  model=tf.keras.models.load_model('dr_weights.h5')
  return model
model=load_model()
st.write('''
Eye Classification
''')
name=st.text_input("Enter Name")  
file=st.file_uploader("Please Upload an image",type=["jpg","png","jpeg"])



from PIL import Image,ImageOps
import numpy as np
def import_and_predict(image_data,model):

  size=(224,224)
  image=ImageOps.fit(image_data,size,Image.ANTIALIAS)
  img=np.asarray(image)
  img_reshape=img[np.newaxis,...]
  prediction=model.predict(img_reshape)
  return prediction
if file is None:
  st.text("Please upload an image")
else:
  image=Image.open(file)
  st.image(image,use_column_width=True)
  prediction=import_and_predict(image,model)
  # print(prediction)
  n=0
  class_names=["NO DR","Mild Dr","Moderate Dr","Sever Dr","pro dr"]
  string=class_names[np.argmax(prediction)]
  db.child("Patient").child(name).update({"dr":string})

  st.success(string)

