from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import smtplib

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

import config as c


app = Flask(__name__)
app.secret_key = c.SECRET_KEY
app.config['UPLOAD_FOLDER'] = c.UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in c.ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template("index2.html")


@app.route('/submit')
def submit():
    return render_template("submit.html")


@app.route('/submit_confirm', methods=['POST'])
def submit_confirm():
    form = request.form
    if request.method == 'POST':
        uploaded_file = request.files['picture']
    else:
        send_mail_no_image(form)
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        send_email(os.path.join(app.config['UPLOAD_FOLDER'], filename), form)
    water_level = form['Water_Level']
    return render_template("submit_confirm.html", water_level=water_level,
                           station=form['marker'],
                           water_clarity=form['clarityRadios'])


def send_email(file_name, form):
    gmail_username = 'sviztsp'
    gmail_password = 'vizvizviz'
    email_subject = 'Data from '+form['marker']
    recipient = 'sviztsp@gmail.com'
    body_of_email = 'Marker: '+form['marker']+'\n'
    body_of_email += 'Water Level: '+form['Water_Level']+'\n'
    body_of_email += 'Water Clarity: '+form['clarityRadios']

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(gmail_username, gmail_password)

    msg = MIMEMultipart()
    msg['Subject'] = email_subject
    msg['From'] = gmail_username
    msg['To'] = recipient

    text = MIMEText(body_of_email)
    msg.attach(text)
    img_data = open(file_name, 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename(file_name))
    msg.attach(image)

    # body_of_email can be plaintext or html!
    #content = headers + "\r\n\r\n" + body_of_email
    session.sendmail(gmail_username, recipient, msg.as_string())


def send_mail_no_image(form):
    gmail_username = 'sviztsp'
    gmail_password = 'vizvizviz'
    email_subject = 'Data from '+form['marker']
    recipient = 'sviztsp@gmail.com'
    body_of_email = 'Marker: '+form['marker']+'\n'
    body_of_email += 'Water Level: '+form['Water_Level']+'\n'
    body_of_email += 'Water Clarity: '+form['clarityRadios']

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.ehlo()
    session.starttls()
    session.login(gmail_username, gmail_password)

    msg = MIMEMultipart()
    msg['Subject'] = email_subject
    msg['From'] = gmail_username
    msg['To'] = recipient

    text = MIMEText(body_of_email)
    msg.attach(text)

    # body_of_email can be plaintext or html!
    #content = headers + "\r\n\r\n" + body_of_email
    session.sendmail(gmail_username, recipient, msg.as_string())


@app.route('/view')
def view_map():
    return render_template("view.html")


@app.route('/help')
def help_view():
    return render_template("help.html")


@app.route('/data/<label_name>')
def show_results(label_name):
    return render_template("data.html", marker=label_name)

