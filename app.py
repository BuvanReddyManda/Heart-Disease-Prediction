from flask import Flask, render_template, request, app, jsonify, url_for
import pickle
import numpy as np

app = Flask(__name__)

model1 = pickle.load(open("clfmodel.pkl","rb"))
model2 = pickle.load(open("insurance_prediction.pkl","rb"))

@app.route('/')
def home():
	return render_template('main.html')

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
        
        data1 = np.array([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        data2 = np.array([[age,sex,bmi,children,smoker,region]]).reshape(1,-1)
        my_prediction1 = model1.predict(data1)
        my_prediction2 = model2.predict(data2)[0]
        from twilio.rest import Client
  
        # Your Account Sid and Auth Token from twilio.com / console
        account_sid = 'ACab5818a9b3b8af6f717b6c4ee2e948f8'
        auth_token = '626472d5f5e4b4c50f97fd89360c4feb'
        if(my_prediction1==1):
  
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                                from_='+15077040615',
                                body ='You have chances of heart disease.Please consult a doctor at the earliest',
                                to =mobile
                            )
        return render_template('result.html', prediction1=my_prediction1,prediction_text = "The cost of health insurance per year is {}").format(my_prediction2)
        
        

if __name__ == '__main__':
	app.run(debug=True)