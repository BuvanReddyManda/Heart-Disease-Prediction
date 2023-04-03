from flask import Flask, render_template, request, app, jsonify, url_for
import pickle
import numpy as np

app = Flask(__name__)

clf0 = pickle.load(open("lrclfmodel.pkl","rb"))
clf1 = pickle.load(open("nbclfmodel.pkl","rb"))
clf2 = pickle.load(open("svmclfmodel.pkl","rb"))
clf3 = pickle.load(open("knnclfmodel.pkl","rb"))
clf4 = pickle.load(open("dtclfmodel.pkl","rb"))
clf5 = pickle.load(open("rfclfmodel.pkl","rb"))

reg0 = pickle.load(open("life_insurance_predictionlr.pkl","rb"))
reg1 = pickle.load(open("life_insurance_predictionsvm.pkl","rb"))
reg2 = pickle.load(open("life_insurance_predictionrf.pkl","rb"))
reg3 = pickle.load(open("life_insurance_predictiongr.pkl","rb"))


@app.route('/')
def hello_world():
    return render_template("login.html")
database={'buvan':'buvan','sarath':'sarath','chaitanya':'chaitanya'}

@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
         return render_template('login.html',info='Invalid User')
    else:
         if database[name1]!=pwd:
              return render_template('login.html',info='Invalid Password')
         else:
              return render_template('main.html',name=name1)


@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':

        age = int(request.form['age'])
        sex = request.form.get('sex')
        cp = request.form.get('cp')
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = request.form.get('fbs')
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        exang = request.form.get('exang')
        oldpeak = float(request.form['oldpeak'])
        slope = request.form.get('slope')
        ca = int(request.form['ca'])
        thal = request.form.get('thal')
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = request.form.get('smoker')
        region = request.form.get('region')
        mobile = request.form.get('mobile')
        model1 = request.form.get('model1')
        model2 = request.form.get('model2')
        
        
        data1 = np.array([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        data2 = np.array([[age,sex,bmi,children,smoker,region]]).reshape(1,-1)
        m1 = np.int64(model1)
        m2 = np.int64(model2)

        if m1==0:
             my_prediction1 = clf0.predict(data1)
        elif m1==1:
             my_prediction1 = clf1.predict(data1)     
        elif m1==2:
             my_prediction1 = clf2.predict(data1)
        elif m1==3:
             my_prediction1 = clf3.predict(data1)
        elif m1==4:
             my_prediction1 = clf4.predict(data1)
        elif m1==5:
             my_prediction1 = clf5.predict(data1)

        if m2==0:
             my_prediction2 = reg0.predict(data2)[0]
             my_prediction3 = "(Accuarcy:78.3%)"
        elif m2==1:
             my_prediction2 = reg1.predict(data2)[0]
             my_prediction3 = "(Accuarcy:72.2%)"
        elif m2==2:
             my_prediction2 = reg2.predict(data2)[0]
             my_prediction3 = "(Accuarcy:86.1%)"
        elif m2==3:
             my_prediction2 = reg3.predict(data2)[0]
             my_prediction3 = "(Accuarcy:87.8%)"
             
        
        
        from twilio.rest import Client
  
        # Your Account Sid and Auth Token from twilio.com / console
        account_sid = '********************************'
        auth_token = '********************************'
        if(my_prediction1==1):
  
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                                from_='*********',
                                body ='You have chances of heart disease.Please consult a doctor at the earliest',
                                to =mobile
                            )
            
        elif(my_prediction1==0):
  
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                                from_='***********',
                                body ='Congratulations You do not have major chances of heart disease',
                                to =mobile
                            )
        return render_template('result.html', prediction1=my_prediction1,prediction3=my_prediction3,prediction_text = "The cost of health insurance per year is {}").format(my_prediction2)
        
        

if __name__ == '__main__':
	app.run(debug=True)