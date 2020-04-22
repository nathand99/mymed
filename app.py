from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta
import sqlite3
import wikipedia
import requests

app = Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/index.html", methods=['POST', 'GET'])
def homeReroute():
	return render_template('index.html')

@app.route("/addReminder.html", methods=['POST', 'GET'])
def addReminder():
	if request.method== "POST":
        #if request.form["username"]
		date1 = request.form["date1"]
		date2 = request.form["date2"]

		date1_object = datetime.strptime(date1, '%d/%m/%Y')
		date2_object = datetime.strptime(date2, '%d/%m/%Y')
		date2_object += timedelta(days=1)

		while date1_object != date2_object:
			formatDate = date1_object.strftime('%Y-%m-%d')
			#while date1_object != (date2_object += datetime.timedelta(days=1)):

			with open('static/json/data.json') as json_file:
				data = json.load(json_file)
				temp = data['entities']
				y = dict()
				y["eventName"] = request.form["drug"]
				y["calendar"] = "Work"
				y["color"] = "orange"
				y["date"] = formatDate
			    # appending data to emp_details
				temp.append(y)
			with open('static/json/data.json','w') as f:
				json.dump(data, f, indent=4)
			date1_object += timedelta(days=1)

		return redirect(url_for('home'))
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
	showMFlag=False
	dFlag = False
	mTitle = "Alert"
	mContent = None
	mToPop = None
	drugF = False
	if request.method == 'POST':
		if request.form.get('submitDrug') != None:
			newName = request.form.get("drugInput").capitalize()
			newType = "Drug"
			drugF = True
			try:
				newDescription = wikipedia.summary(newName, sentences=1, auto_suggest=False).replace("'","")
			except wikipedia.exceptions.PageError:
				mTitle = "Error Finding Medication"
				mContent = "The medication you entered was: " + newName + ".\n Please correct any potential spelling mistakes and retry."
				showMFlag = True
			except wikipedia.exceptions.DisambiguationError as e:
				mTitle = "Please Specify Medication"
				mContent = "The medication you entered was: " + newName + ".\n Please click the specific entry."
				mToPop = e.options
				dFlag = True
				showMFlag = True
			else:
				c.execute("INSERT INTO medHis ('name', 'description', 'type') VALUES('{}', '{}', '{}')".format(newName, newDescription, newType))
		elif request.form.get('submitSymptom') != None:
			newName = request.form.get("symptomInput").capitalize()
			newType = "Symptom"
			try:
				newDescription = wikipedia.summary(newName, sentences=1, auto_suggest=False).replace("'","")
			except wikipedia.exceptions.PageError:
				mTitle = "Error Finding Symptom"
				mContent = "The symptom you entered was: " + newName + ".\n Please correct any potential spelling mistakes and retry."
				showMFlag = True
			except wikipedia.exceptions.DisambiguationError as e:
				mTitle = "Please Specify Symptom"
				mContent = "The symptom you entered was: " + newName + ".\n Please click the specific entry."
				mToPop = e.options
				dFlag = True
				showMFlag = True
			else:
				c.execute("INSERT INTO medHis ('name', 'description', 'type') VALUES('{}', '{}', '{}')".format(newName, newDescription, newType))
		elif request.form.get('mListingButton') != None:
			newName = request.form.get("mListingButton")
			if newName[-1] == "d":
				newType = "Drug"
			else:
				newType = "Symptom"
			newDescription = wikipedia.summary(newName[:-1], sentences=1, auto_suggest=False).replace("'","")
			c.execute("INSERT INTO medHis ('name', 'description', 'type') VALUES('{}', '{}', '{}')".format(newName[:-1], newDescription, newType))
		else:
			medHisId = request.form.get('deleteButton')
			c.execute("DELETE FROM medHis WHERE id={}".format(medHisId))

	c.execute('SELECT * FROM medHis')
	medH = c.fetchall()
	medH.sort(key=lambda x: x[4])
	conn.commit()
	conn.close()
	return render_template('medHistory.html', medHis=medH, showModal=showMFlag, modalTitle=mTitle, disambiguationFlag=dFlag, modalContent=mContent, modalToPopulate=mToPop, drugFlag=drugF)

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
