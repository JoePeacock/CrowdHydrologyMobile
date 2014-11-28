from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import smtplib

from flask import Flask
from flask import render_template
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy, Model

import config as c

app = Flask(__name__)
app.secret_key = c.SECRET_KEY
app.config['UPLOAD_FOLDER'] = c.UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./crowd_hydrology.db'

db = SQLAlchemy(app)
from app.models.station import Station
from app.models.data import Data

db.create_all()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in c.ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/submit')
def submit():
    return render_template("submit.html")


@app.route('/submit_confirm', methods=['POST'])
def submit_confirm():
    form = request.form
    marker = form["marker"].upper()
    station = Station.query.filter_by(name=marker).first()
    if station is not None and station.online:
        try:
            point = Data(water_level=float(form["water_level"]),
                         water_clarity=int(form["clarity_value"]))
            station.data_points.append(point)
            db.session.commit()
            return render_template("submit_confirm.html",
                                   water_level=form["water_level"],
                                   station=marker,
                                   water_clarity=form['clarity_value'])
        except ValueError:
            return render_template("submit.html",
                               error="The measurement entered was formatted incorrectly. Make sure you only use numbers."), 400
    else:
        return render_template("submit.html",
                               error="No location "+marker+". Please verify the marker ID and resubmit."), 400

        # if request.method == 'POST':
        # uploaded_file = request.files['picture']
        # else:
        # send_mail_no_image(form)
        # if uploaded_file and allowed_file(uploaded_file.filename):
        # filename = secure_filename(uploaded_file.filename)
        # uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # send_email(os.path.join(app.config['UPLOAD_FOLDER'], filename), form)
        # water_level = form['Water_Level']

@app.route('/view')
def view_map():
    return render_template("view.html")


@app.route('/help')
def help_view():
    return render_template("help.html")


@app.route('/data/<label_name>')
def show_results(label_name):
    return render_template("data.html", marker=label_name)

