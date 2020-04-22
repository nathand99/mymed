from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

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
		print (request.form["drug"])
		print (request.form["date1"])
		random = request.form["date1"]
		date_object = datetime.strptime(random, '%d/%m/%Y')
		formatDate = date_object.strftime('%Y-%m-%d')
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
	return render_template('medHistory.html')

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
