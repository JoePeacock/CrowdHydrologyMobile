from app import app
from flask import render_template
from flask import url_for
from flask import request, session, escape, redirect
from app import forms
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import smtplib
##from forms import RegistrationForm, EventForm, EditImage

import urllib2, urllib, json, httplib

UPLOAD_FOLDER = '/Users/Dinsmoor/Developer/CS4760/app/server/app/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.secret_key = 'F5W4sSeiSsbU4lB+SdXX1sBS4cgk6ZUs1gstMNiSgyMMzkvcF0+IGVZCOLAkJbzCYPZeItyGgfL0JPkpsxOY2+BysVWCGEKssqT4zu4gAXws1DsPH4v0F/LIie0kevAFuneFVbqM3CdFy/IRvffXUzD8nhvjEVKbwhLpUediUXE='
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

##Index for Application
@app.route('/')
def home():
	##return redirect(url_for('static', filename='index.html'))
	return render_template("index2.html")

##Submit Page
@app.route('/submit')
def submit():
	return render_template("submit.html")

##Submit COnfirm
@app.route('/submit_confirm', methods=['POST'])
def submit_confirm():
	form = request.form
	if(request.method == 'POST'):
		file = request.files['picture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            SendMail(os.path.join(app.config['UPLOAD_FOLDER'], filename),form)
        else:
			SendMail_NoImage(form)
	
	waterLvl=form['Water_Level']
	return render_template("submit_confirm.html", water_level = waterLvl, station=form['marker'], water_clarity=form['clarityRadios'])


def SendMail(ImgFileName, form):
	GMAIL_USERNAME = 'sviztsp'
	GMAIL_PASSWORD = 'vizvizviz'
	email_subject = 'Data from '+form['marker']
	recipient = 'sviztsp@gmail.com'
	body_of_email = 'Marker: '+form['marker']+'\n'
	body_of_email += 'Water Level: '+form['Water_Level']+'\n'
	body_of_email += 'Water Clarity: '+form['clarityRadios']

	session = smtplib.SMTP('smtp.gmail.com', 587)
	session.ehlo()
	session.starttls()
	session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

	msg = MIMEMultipart()
	msg['Subject'] = email_subject
	msg['From'] = GMAIL_USERNAME
	msg['To'] = recipient

	text = MIMEText(body_of_email)
	msg.attach(text)
	img_data = open(ImgFileName, 'rb').read()
	image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
	msg.attach(image)

	# body_of_email can be plaintext or html!                    
	#content = headers + "\r\n\r\n" + body_of_email
	session.sendmail(GMAIL_USERNAME, recipient, msg.as_string())

def SendMail_NoImage(form):
	GMAIL_USERNAME = 'sviztsp'
	GMAIL_PASSWORD = 'vizvizviz'
	email_subject = 'Data from '+form['marker']
	recipient = 'sviztsp@gmail.com'
	body_of_email = 'Marker: '+form['marker']+'\n'
	body_of_email += 'Water Level: '+form['Water_Level']+'\n'
	body_of_email += 'Water Clarity: '+form['clarityRadios']

	session = smtplib.SMTP('smtp.gmail.com', 587)
	session.ehlo()
	session.starttls()
	session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

	msg = MIMEMultipart()
	msg['Subject'] = email_subject
	msg['From'] = GMAIL_USERNAME
	msg['To'] = recipient

	text = MIMEText(body_of_email)
	msg.attach(text)

	# body_of_email can be plaintext or html!                    
	#content = headers + "\r\n\r\n" + body_of_email
	session.sendmail(GMAIL_USERNAME, recipient, msg.as_string())

@app.route('/view')
def view_map():
	waterLvl="THIS IS WATERRR"
	return render_template("view.html", water_level = waterLvl)

@app.route('/help')
def help():
	waterLvl="THIS IS WATERRR"
	return render_template("help.html")

@app.route('/data/<labelname>')
def show_results(labelname):
    return render_template("data.html", marker = labelname)

""""
headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                       "subject: " + email_subject,
                       "to: " + recipient,
                       "mime-version: 1.0",
                       "content-type: text/html"])
	img_data = open(ImgFileName, 'rb').read()
	image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
	headers.attach(image)


# The below code never changes, though obviously those variables need values.
GMAIL_USERNAME = 'sviztsp'
GMAIL_PASSWORD = 'vizvizviz'
email_subject = 'dicks'
recipient = 'dazztrazak@gmail.com'
body_of_email = 'slightly bigger dicks'

session = smtplib.SMTP('smtp.gmail.com', 587)
session.ehlo()
session.starttls()
session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                       "subject: " + email_subject,
                       "to: " + recipient,
                       "mime-version: 1.0",
                       "content-type: text/html"])

# body_of_email can be plaintext or html!                    
content = headers + "\r\n\r\n" + body_of_email
session.sendmail(GMAIL_USERNAME, recipient, content)
"""
##Begin Old Code

"""##Where the user is sent after logging in or making an account
@app.route('/index')
def index():
	if not(session.has_key("username")):
		return redirect(url_for("login"))
	info = session['user_information']
	if 'username' in session:
		return render_template("index.html", user = info)
	return 'You are not logged in'

##Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	if(session.has_key("username")):
		return redirect('/index')
	form = LoginForm(request.form)
	if(request.method == 'POST' and form.validate()):
		username = form.username.data
		password = form.password.data
		status = is_logged_in(username, password)
		if(status):
			session['username'] = username
			return redirect(url_for('index'))
		else:
			return("Something went wrong!  Your information must be wrong")

	if(request.method == 'GET'):
		return render_template('login_real.html', form=form)
	

##Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if(request.method =='POST' and form.validate()):
		first_name = form.first_name.data
		last_name = form.last_name.data
		username = form.username.data
		email = form.email.data
		password = form.password.data
		num_events_attended = 0
		num_events_created = 0
		picture_string = '../static/blizzard.jpg'

		data = {
			'first_name' : first_name,
			'last_name' : last_name,
			'username' : username,
			'email' : email,
			'password' : password,
			'num_events_created' : num_events_created,
			'num_evnets_attend' : num_events_attended,
			'rating' : 0,
			'points' : 0,
			'picture_string' : picture_string
		}

		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/classes/_User', json.dumps(data), headers)
		result = json.loads(connection.getresponse().read())
		print result

		status = is_logged_in(username, password)
		print(status)
		if(status):
			session['username'] = username
			session['first_name'] = first_name
			return redirect(url_for('index'))
		else:
			return("Something went wrong!")
	return render_template('register.html', form=form)


@app.route('/create', methods=['GET', 'POST'])
def create_event():
	info = session['user_information']
	form = EventForm(request.form)
	if(request.method == 'POST' and form.validate()):
		## creator, name, description, looking_for_people, time, date,
		creator = ("%s %s" % (session['user_information']['first_name'], session['user_information']['last_name']))
		event_name = form.event_name.data
		event_date = form.event_date.data
		event_start_time = form.event_start_time.data
		event_description = form.event_description.data
		event_number_of_people = form.event_number_of_people.data
		event_location_description = form.event_location_description.data
		event_geolocation = form.event_geolocation.data
		geolocation = event_geolocation.split(' ')
		event_geolocation = {
			"location" : {
				"__type" : "GeoPoint",
				"latitude" : float(geolocation[0]),
				"longitude" : float(geolocation[1])
			}
		}
		people = [creator]
		data = {
			'creator' : creator,
			'name' : event_name,
			'looking_for_people' : int(event_number_of_people),
			'date' : event_date,
			'time' : event_start_time,
			'description' : event_description,
			'location_string' : event_location_description,
			'location' : event_geolocation["location"],
			'people_attending' : people
		}

		connection = httplib.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		connection.request('POST', '/1/classes/Event', json.dumps(data), headers)
		result = json.loads(connection.getresponse().read())
		return render_template('successful.html', data = data, info = info)

	return render_template('createEvent.html', form = form, info = info)


@app.route('/logout')
def logout():
	for cur in session.keys():
		session.pop(cur)
	return redirect(url_for('login'))


@app.route('/view')
def view_events():
	info = session['user_information']
	if not(session.has_key("username")):
		return redirect('/login')
	return render_template('eventView.html', info = info)

@app.route('/event/<objectID>')
def specific_event(objectID):
	info = session['user_information']
	if not(session.has_key("username")):
		return redirect('/login')
	#Grab stuff from parse
	event_info = get_event(objectID)
	return render_template('specific_event.html', data = event_info, info = info)

@app.route('/profile/<username>')
def profile(username):
	form = EditImage(request.form)
	if not(session.has_key("username")):
		return redirect('/login')
	if(session['username'] == username):
		info = session['user_information']
		picture = form.image.data
		#get parse info, pass it with render
		return render_template('edit_profile.html', user = info, form=form)
	#get parse info, pass it with render
	if(session['username'] != username):
		return render_template('error_profile.html')
	return render_template('view_profile.html')

"""


