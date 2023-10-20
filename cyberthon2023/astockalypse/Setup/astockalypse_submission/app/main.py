import os
import numpy as np
from flask import Flask, request, jsonify, flash, render_template, redirect, send_file, url_for
import pandas as pd
import uuid
import pickle
import csv
import io
import re
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		file = request.files['file']
		if '.pkl' not in file.filename:
			flash(f"File is not a .pkl file")
			return redirect(url_for('home'))

		filename = str(uuid.uuid4()) + '.pkl'
		file.save(os.path.join('uploads', filename))
		return redirect(url_for('predict', filename=filename))
	return render_template('index.html')

@app.route('/predict/<filename>')
def predict(filename):
	try:
		with open(os.path.join('uploads', filename), 'rb') as f:
			stolen_model = pickle.load(f)
			
		if not isinstance(stolen_model, LinearRegression):
		    flash("Model submitted is not an instance of scikit-learn LinearRegression.")
		    os.remove(os.path.join('uploads', filename))
		    return redirect(url_for('home'))
		   
		df = pd.read_csv('model_preds.csv')
		X = df.drop('price_return', axis=1)
		y = df['price_return']
		
		predictions = np.round(stolen_model.predict(X), 1)
		mse = mean_squared_error(y, predictions)
		if mse < 30:
			flash("Cyberthon{Ap0c4lypt1c_m4rk3t_cr45h!!!!!}")
		else:
			flash(f"Model is not accurate enough, with an mse of {mse}.")

		os.remove(os.path.join('uploads', filename))
		return redirect(url_for('home'))

	except Exception as e:
		flash(f"Error: {e}")
		os.remove(os.path.join('uploads', filename))
		return redirect(url_for('home'))


if __name__ == "__main__":
	app.run(debug=False, port=5001, host='0.0.0.0')
