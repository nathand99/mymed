from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta
import sqlite3
#import wikipedia
#import requests

app = Flask(__name__)

'''
Dedicated page for "page not found"
'''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404


'''
 Home Start Page
'''
@app.route("/", methods=['POST', 'GET'])
def home():
	conn = sqlite3.connect('reminders.db')
	c = conn.cursor()
	c.execute('SELECT * from rem')
	result = c.fetchall()
	with open('static/json/data.json') as json_file:
		data = json.load(json_file)
		del data['entities']
		entities = []
		for row in result:
			eventName, date, time = row
			nameAndTime = eventName + " @ " + time
			y = dict()
			y["eventName"] = nameAndTime
			y["calendar"] = "Medicine"
			y["color"] = "green"
			y["date"] = date
		    # appending data to emp_details
			entities.append(y)
		data['entities'] = entities
	with open('static/json/data.json','w') as f:
		json.dump(data, f, indent=4)

		#print ("{} {} {}".format(eventName, date, time))
	conn.close()
	if request.method == 'POST':
		if 'add' in request.form:
			return redirect(url_for('addReminder'))
		if 'delete' in request.form:
			return redirect(url_for('delReminder'))
	return render_template('index.html')

@app.route("/index.html", methods=['POST', 'GET'])
def homeReroute():
	return render_template('index.html')

@app.route("/addReminder.html", methods=['POST', 'GET'])
def addReminder():
	conn = sqlite3.connect('reminders.db')
	c = conn.cursor()


	if request.method== "POST":
        #if request.form["username"]
		date1 = request.form["date1"]
		date2 = request.form["date2"]
		print (request.form["appt"])

		date1_object = datetime.strptime(date1, '%d/%m/%Y')
		date2_object = datetime.strptime(date2, '%d/%m/%Y')
		date2_object += timedelta(days=1)

		while date1_object != date2_object:
			formatDate = date1_object.strftime('%Y-%m-%d')
			c.execute("INSERT INTO rem ('eventName', 'date', 'time') VALUES('{}', '{}', '{}')".format(request.form["drug"], formatDate, request.form["appt"]))
			date1_object += timedelta(days=1)
			conn.commit()
			#conn.close()

		return redirect(url_for('home'))


		conn.close()
	return render_template('addReminder.html')

@app.route("/delReminder.html", methods=['POST', 'GET'])
def delReminder():
	conn = sqlite3.connect('reminders.db')
	c = conn.cursor()
	c.execute('select rowid, * from rem order by rowid asc')
	result = c.fetchall()

	if request.form.get('deleteButton') != None:
		eventId = request.form.get('deleteButton')
		c.execute("DELETE FROM rem WHERE rowid={}".format(eventId))
		conn.commit()

		return redirect(url_for('home'))


	conn.close()
	return render_template('delReminder.html', events=result)


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
	mContent = ""
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
				response = requests.get('https://api.fda.gov/drug/label.json?search=openfda.brand_name:"{}"'.format(newName))
				print(response.status_code)
				print(type(response.status_code))
				if response.status_code == 200:
					data = response.json().get("results")[0]
					print(data)
					if data.get('ask_a_doctor') != None:
						showMFlag = True
						mTitle = newName + " Warning"
						mContent = "Ask a Doctor or Pharmacist:\n" + data.get('ask_a_doctor')[0] + "\n\n"
					elif data.get('ask_a_doctor_or_pharmacist') != None:
						showMFlag = True
						mTitle = newName + " Warning"
						mContent = "Ask a Doctor or Pharmacist:\n" + data.get('ask_a_doctor_or_pharmacist')[0] + "\n\n"
					if data.get('do_not_use') != None:
						showMFlag = True
						mTitle = newName + " Warning"
						mContent = data.get('do_not_use')[0].replace("•","\n") + "\n\n"
						mContent.replace(".",".<br>").capitalize()

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
