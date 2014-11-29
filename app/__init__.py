from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import smtplib

from flask import Flask, jsonify
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


@app.route('/help')
def help_view():
    return render_template("help.html")


@app.route('/view')
def view_map():
    return render_template("view.html")


@app.route('/view/<label_name>')
def show_results(label_name):
    label_name = label_name.upper()
    return render_template("data.html", marker=label_name)


@app.route('/api/stations')
def get_stations():

    results_per_page = int(request.args.get('per_page', 1000))
    page = int(request.args.get('page', 1))

    station = Station.query.paginate(page, results_per_page)

    data = [s.serialize() for s in station.items]
    response = {
        'pagination': {
            'has_next': station.has_next,
            'has_prev': station.has_prev,
            'next_num': station.next_num,
            'current_page': station.page,
            'total_pages': station.pages,
            'per_page': station.per_page,
            'prev_num': station.prev_num,
            'total_results': station.total
        },
        'data': data
    }
    return jsonify(response)


@app.route('/api/data/<label_name>')
def get_data(label_name):
    """
    The default number of data points per page is 100. This may be adjusted at
    some point. If start_date and end_date are given, all data points between
    them will be returned. If they are equal, all data points for that day will
    be returned.

    :param label_name:   The name of the station ie: NY1007
    :param page=:        The page number that you are trying to reach.
    :param start_date=:  The start date in POSIX to get all data after this date.
    :param end_date=:    The end date in POSIX to get all data before this date.
    :param per_page=:    Number of results you want to return per page.

    :return: A paginated list of data points in lists of 25 max
    """

    label_name = label_name.upper()
    results_per_page = int(request.args.get('per_page', 1000))
    page = int(request.args.get('page', 1))

    station = Station.query.filter_by(name=label_name).first()
    data_points = Data.query.filter_by(station_id=station.id). \
        paginate(page, results_per_page)

    data = [d.serialize() for d in data_points.items]
    response = {
        'station_id': station.name,
        'pagination': {
            'has_next': data_points.has_next,
            'has_prev': data_points.has_prev,
            'next_num': data_points.next_num,
            'current_page': data_points.page,
            'total_pages': data_points.pages,
            'per_page': data_points.per_page,
            'prev_num': data_points.prev_num,
            'total_results': data_points.total
        },
        'data': data
    }
    return jsonify(response)


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
                                   error='The measurement entered was formatted incorrectly. Make sure you only use numbers.'), 400
    else:
        return render_template("submit.html",
                               error="No location "+marker+". Please verify the marker ID and resubmit."), 400

        # TODO: Upload image and store url in the database.
        # if request.method == 'POST':
        # uploaded_file = request.files['picture']
        # else:
        # send_mail_no_image(form)
        # if uploaded_file and allowed_file(uploaded_file.filename):
        # filename = secure_filename(uploaded_file.filename)
        # uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # send_email(os.path.join(app.config['UPLOAD_FOLDER'], filename), form)
        # water_level = form['Water_Level']




