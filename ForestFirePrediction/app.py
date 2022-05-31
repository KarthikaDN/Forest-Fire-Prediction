from flask import Flask,request, url_for, redirect, render_template,session
import pickle
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'

model=pickle.load(open('model.pkl','rb'))


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/check')
def check():
    return render_template("forest_fire.html")

@app.route("/Reasons-for-forest-fire")
def reasons():
    return render_template("reasons.html")

@app.route('/predict_redirect',methods=['POST','GET'])
def redirectForestFire():
    if(session.get("messages")!=None):
        msg = session['messages']
        session.clear()
    else:
        msg="Enter All The Values"

    
    
    return render_template('forest_fire.html',pred=msg)

@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        int_features=[int(x) for x in request.form.values()]
        final=[np.array(int_features)]
        print(int_features)
        print(final)
        prediction=model.predict_proba(final)
        output='{0:.{1}f}'.format(prediction[0][1], 2)

        if output>str(0.5):
            session['messages'] = 'Your Forest is in Danger.\nProbability of fire occuring is {}'.format(output)
            return redirect('/predict')
            #return render_template('forest_fire.html',pred='Your Forest is in Danger.\nProbability of fire occuring is {}'.format(output))
        else:
            session['messages'] = 'Your Forest is safe.\nProbability of fire occuring is {}'.format(output)
            return redirect('/predict')
            #return render_template('forest_fire.html',pred='Your Forest is safe.\n Probability of fire occuring is {}'.format(output))

    else:
        return redirect('/predict_redirect')


if __name__ == '__main__':
    app.run(debug=True)
