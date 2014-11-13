from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import smtplib

from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

from app import app

UPLOAD_FOLDER = '/Users/Dinsmoor/Developer/CS4760/app/server/app/static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.secret_key = 'F5W4sSeiSsbU4lB+SdXX1sBS4cgk6ZUs1gstMNiSgyMMzkvcF0+IGVZCOLAkJbzCYPZeItyGgfL0JPkpsxOY2+BysVWCGEKssqT4zu4gAXws1DsPH4v0F/LIie0kevAFuneFVbqM3CdFy/IRvffXUzD8nhvjEVKbwhLpUediUXE='
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# #Index for Application
@app.route('/')
def home():
    return render_template("index2.html")


##Submit Page
@app.route('/submit')
def submit():
    return render_template("submit.html")


##Submit COnfirm
@app.route('/submit_confirm', methods=['POST'])
def submit_confirm():
    form = request.form
    if request.method == 'POST':
        file = request.files['picture']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        SendMail(os.path.join(app.config['UPLOAD_FOLDER'], filename), form)
    else:
        SendMail_NoImage(form)

    waterLvl = form['Water_Level']
    return render_template("submit_confirm.html", water_level=waterLvl,
                           station=form['marker'],
                           water_clarity=form['clarityRadios'])


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
    waterLvl = "THIS IS WATERRR"
    return render_template("view.html", water_level=waterLvl)


@app.route('/help')
def help():
    waterLvl = "THIS IS WATERRR"
    return render_template("help.html")


@app.route('/data/<labelname>')
def show_results(labelname):
    return render_template("data.html", marker=labelname)
