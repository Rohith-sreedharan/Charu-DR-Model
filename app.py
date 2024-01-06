# Copyright (C) 2024-present by Rohith-Sreedharan@Springreen, < https://github.com/sprin-g-reen >.
#
# This file is part of < https://github.com/rohith-sreedharan/Charu-DR-Model > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/rohith-sreedharan/Charu-DR-Model >
#
# All rights reserved.

import numpy as np
import os, requests
from tensorflow.keras.models import load_model #type:ignore
from tensorflow.keras.preprocessing import image #type:ignore
from tensorflow.keras.applications.inception_v3 import preprocess_input #type:ignore
from flask import Flask, request, render_template, redirect, url_for
from cloudant.client import Cloudant

model = load_model(r"IBMDR.h5")
app = Flask(__name__)
client = Cloudant.iam('4c6ccfaa-30e7-4fc6-a2fd-ed34bce0f3b7-bluemix', '2nLEMJXpFx6zL2kst9dMKWWOkWA0CTi2CUDbjD0cIZUY', connect=True)
my_database = client.create_database ('my_database')

@app. route('/')
def index():
    """
Renders the index.html template.

Returns:
    str: The rendered index.html template.
"""
    return render_template('index.html')

@app.route('/register')
def register():
    """
Renders the 'register.html' template.

Returns:
    str: The rendered HTML template for the registration page.
"""
    return render_template('register.html')

@app.route('/afterreg', methods= ['POST'])
def afterreg() :
    """
This function is the route handler for the '/afterreg' endpoint. It is triggered when a POST request is made to this endpoint.

Returns:
    str: The rendered HTML template for the registration page with a success message if the registration is successful, or an error message if the user is already registered.
    """
    x = [x for x in request.form.values()]
    print (x)
    data = {
    '_id': x[1],
    ' name': x[0],
    'p5w' :x [2]
    }
    print (data)
    query = {'_id': {'$eq': data['_id']}}
    docs = my_database.get_query_result(query)
    print(len(docs.all()))
    if(len(docs.all())==0):
        url = my_database.create_document(data)
        return render_template('register.html', pred="Registration Successful, please logan using your details")
    else:
        return render_template('register.html', pred="You are already a member, please login using your, details")

@app.route('/login')
def login():
    """
This function is the route handler for the '/login' endpoint. It is triggered when a GET request is made to this endpoint.

Returns:
    str: The rendered HTML template for the login page.
"""
    return render_template('login.html')
                            
@app.route ('/afterlogin', methods=[' POST'])
def afterlogin():
    """
This function is the route handler for the '/afterlogin' endpoint. It is triggered when a POST request is made to this endpoint.

Returns:
    - If the username is not found in the database, it renders the login page with a message indicating that the username is not found.
    - If the username and password match the database records, it redirects to the 'prediction' endpoint.
    - If the username and password do not match the database records, it prints 'Invalid User' to the console.
"""
    user = request.form[' id']
    passw = request. form ['psw']
    print (user, passw)

    query = {'_id': {'$eq': user}}
    docs = my_database.get_query_result(query)
    # print(docs)

    # print(len(docs.all()))
    if (len (docs.all ())==0): 
        return render_template('login.html', pred="The username is not found.")
    else:
        if((user==docs[0][0]['_id'] and passw==docs[0][0]['psw'])):
            return redirect(url_for ('prediction'))
        else:
            print ('Invalid User')

@app.route('/logout')
def logout():
    """
Renders the logout.html template.

Returns:
    str: The rendered HTML template for the logout page.
"""
    return render_template('logout.html')

@app.route('/result', methods=["GET", "POST"])
def res():
    """
Handles the '/result' route for the Flask application.

This function is responsible for processing the uploaded image, making a prediction using the loaded model, and rendering the 'prediction.html' template with the predicted result.

Returns:
    str: The rendered 'prediction.html' template with the predicted result.
"""
    if request.method=="POST" :
        f = request.files['image']
        basepath=os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', f.filenane)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(299,299))
        x = image.ing_to_array(img)
        x = np.expand_dims(x, axis=0)

        img_data = preprocess_input(x)
        prediction = np.argmax(model.predict(img_data), axis=1)

        index = ['No Diabetic Retinopathy', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']
        result = str(index[prediction[0]])
        return render_template("prediction.html", prediction=result)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)