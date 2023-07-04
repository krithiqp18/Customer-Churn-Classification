from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('modelnew.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def predict():
    int_features = []
    for field in ['account_length', 'area_code', 'international_plan', 'vmail_plan',
                  'vmail_message', 'day_mins', 'day_calls', 'day_charge', 'eve_mins',
                  'eve_calls', 'eve_charge', 'night_mins', 'night_calls', 'night_charge',
                  'intl_mins', 'intl_calls', 'intl_charge', 'custserv_calls']:
        value = request.form.get(field)
        if field in ['international_plan', 'vmail_plan']:
            int_features.append(1 if value.lower() == 'yes' else 0)
        else:
            try:
                int_features.append(float(value))
            except ValueError:
                int_features.append(0)
    
    final_features = np.array([int_features])
    prediction = model.predict(final_features)
    
    churn_label = 'The Customer will Churn' if prediction[0] else 'The customer wont churn'
    
    return render_template('index.html', prediction_text=churn_label)

if __name__ == '__main__':
    app.run(debug=True)
