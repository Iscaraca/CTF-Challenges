import os
import numpy as np
from flask import Flask, request, jsonify, flash, render_template, redirect, send_file, url_for
import pandas as pd
import uuid
import pickle
import csv
import io
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
global model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		file = request.files['file']

		filename = str(uuid.uuid4()) + '.csv'
		file.save(os.path.join('uploads', filename))
		return redirect(url_for('predict', filename=filename))
	return render_template('index.html')

@app.route('/predict/<filename>')
def predict(filename):
	proxy = io.StringIO()
	writer = csv.writer(proxy)

	err = 0

	with open(os.path.join('uploads', filename), 'r') as f:
		data = csv.reader(f, delimiter=',')
		
		for count, row in enumerate(data, 1):
			if count > 1000:
				err = 1
				break

			waf = r"^(?:1000|[1-9]\d{0,2})(?:\.\d)?,(?:1000|[1-9]\d{0,2})(?:\.\d)?,(?:1000|[1-9]\d{0,2})(?:\.\d)?$"
			if not re.match(waf, ','.join(row)):
				err = 2
				break

			prediction = round(model.predict(
				pd.DataFrame(np.array([float(row[0]), float(row[1]), float(row[2])]).reshape(1, -1), columns=['t1', 't2', 't3'])
			)[0], 1)
	
			writer.writerow([prediction])
	
	if err:
		if err == 1:
			flash("Too many lines. Maximum of 1000 queries allowed.")
			proxy.close()
			os.remove(os.path.join('uploads', filename))
			return redirect(url_for('home'))
		if err == 2:
			flash(f"Row {count} of invalid format. Numbers must be to 1dp between 1 and 1000 inclusive.")
			proxy.close()
			os.remove(os.path.join('uploads', filename))
			return redirect(url_for('home'))

	mem = io.BytesIO()
	mem.write(proxy.getvalue().encode())
	mem.seek(0)
	proxy.close()

	os.remove(os.path.join('uploads', filename))
	return send_file(
		mem,
		as_attachment=True,
		download_name='output.csv',
		mimetype='text/csv'
	)

if __name__ == "__main__":
	app.run(debug=False, port=5000, host='0.0.0.0')
