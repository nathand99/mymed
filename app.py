from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/index.html")
def homeReroute():
	return render_template('index.html')

@app.route("/addReminder.html", methods=['POST', 'GET'])
def addReminder():
	return render_template('addReminder.html')

@app.route("/alert.html", methods=['POST', 'GET'])
def alert():
	return render_template('alert.html')

@app.route("/article.html", methods=['POST', 'GET'])
def article():
	return render_template('article.html')

@app.route("/encyclopedia.html", methods=['POST', 'GET'])
def encyclopedia():
	return render_template('encyclopedia.html')

@app.route("/medHistory.html", methods=['POST', 'GET'])
def medicalHistory():
	conn = sqlite3.connect('history.db')
	c = conn.cursor()
	if request.method == 'POST':
		if request.form.get('submitDrug') != None:
			newName = request.form.get("drugInput")
			newDescription = "Painkiller"
			newType = "Drug"
			c.execute("INSERT INTO medHis ('name', 'description', 'type') VALUES('{}', '{}', '{}')".format(newName, newDescription, newType))
		elif request.form.get('submitSymptom') != None:
			pass
		else:
			medHisId = request.form.get('deleteButton')
			c.execute("DELETE FROM medHis WHERE id={}".format(medHisId))

	c.execute('SELECT * FROM medHis')
	medH = c.fetchall()
	medH.sort(key=lambda x: x[4])
	conn.commit()
	conn.close()
	return render_template('medHistory.html', medHis=medH)

@app.route("/medicine.html", methods=['POST', 'GET'])
def medicine():
	return render_template('medicine.html')

@app.route("/news.html", methods=['POST', 'GET'])
def news():
	return render_template('news.html')

@app.route("/searchEncyclopaedia.html", methods=['POST', 'GET'])
def searchEncyclopedia():
	return render_template('searchEncyclopaedia.html')

@app.route("/searchName.html", methods=['POST', 'GET'])
def searchName():
	return render_template('searchName.html')

@app.route("/searchNews.html", methods=['POST', 'GET'])
def searchNews():
	return render_template('searchNews.html')

@app.route("/searchPriceCompare.html", methods=['POST', 'GET'])
def searchPriceCompare():
	return render_template('searchPriceCompare.html')

@app.route("/searchUDI.html", methods=['POST', 'GET'])
def searchUDI():
	return render_template('searchUDI.html')

@app.route("/zyrtec.html", methods=['POST', 'GET'])
def zyrtec():
	return render_template('zyrtec.html')