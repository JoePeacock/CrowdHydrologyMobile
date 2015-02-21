import arrow
from flask import Flask, jsonify, url_for, redirect, json

from flask import render_template
from flask import request
from flask.ext.login import LoginManager, login_required, logout_user, \
    login_user
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_, or_

from app.lib.distance import find_closest_station
from app.lib.water_color import WaterColor
import config as c


def humanize_arrow(stamp):
    t = arrow.get(stamp)
    return t.humanize()


def water_color(color):
    w = WaterColor(color)
    return w.get_color()


def get_station(id):
    return Station.query.get(id)


app = Flask(__name__)
app.secret_key = c.SECRET_KEY
app.config['UPLOAD_FOLDER'] = c.UPLOAD_FOLDER
app.jinja_env.filters['humanize'] = humanize_arrow
app.jinja_env.filters['water_color'] = water_color
app.jinja_env.filters['get_station'] = get_station
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./crowd_hydrology.db'
db = SQLAlchemy(app)
from app.models.station import Station
from app.models.data import Data
from app.models.user import User

db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in c.ALLOWED_EXTENSIONS


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        user = User.query.filter_by(email=form['email']).first()
        if user is None:
            return render_template("login.jinja",
                                   error="Email not found."), 400
        elif user.password == form['password']:
            login_user(user)
            return redirect(url_for("admin_home"))
        else:
            return render_template("login.jinja",
                                   error="Invalid Password."), 400
    return render_template("login.jinja")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/admin/user/new', methods=["GET", "POST"])
@login_required
def new_admin():
    if request.method == "POST":
        form = request.form
        if User.query.filter_by(email=form['email']).first() is not None:
            return render_template('new_admin.jinja',
                                   error="User already exists!")
        if form['password'] == form['password_check'] and form[
            'email'] is not None:
            u = User(email=form['email'], password=form['password'])
            db.session.add(u)
            db.session.commit()
            return render_template('new_admin.jinja',
                                   success="Admin succesfully added!")
        else:
            return render_template('new_admin.jinja',
                                   error="Either passwords do not match, or you did not enter a username!")
    return render_template('new_admin.jinja')


@app.route('/admin')
@login_required
def admin_home():
    active_stations = Station.query.filter_by(online=True).count()
    data_points_count = Data.query.count()
    most_active = Station.query.filter(or_(and_(func.length(Station.data_points) > 0))).first()
    data_points = Data.query.order_by(Data.created_at.desc()).limit(10)
    return render_template("admin_home.jinja", active_stations=active_stations,
                           total_data_count=data_points_count,
                           most_data=most_active.name,
                           data_points=data_points)


@app.route('/admin/data')
@login_required
def admin_data():
    limit = int(request.args.get('per_page', 25))
    page = int(request.args.get('page', 1))
    if page == -1:
        data = Data.query.order_by(Data.created_at.desc())
    else:
        data = Data.query.paginate(page, limit)
    return render_template("admin_data.jinja", data=data)


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


@app.route('/stations')
def show_stations():
    return render_template("stations.html")


@app.route('/api/stations')
def get_stations():
    results_per_page = int(request.args.get('per_page', 1000))
    online = bool(request.args.get('online', True))
    page = int(request.args.get('page', 1))

    latitude = float(request.args.get('lat', 0))
    longitude = float(request.args.get('long', 0))

    station = Station.query.filter_by(online=online). \
        paginate(page, results_per_page)

    if latitude != 0 and longitude != 0:
        s = find_closest_station(latitude, longitude, station)
        return jsonify({
            "station": s.serialize()
        })

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


@app.route('/api/data', methods=["POST"])
def get_data_query():
    """
    Endpoint that returns collective stations, and data points for generating a
    shapefile in ArcGIS. If both Timestamps and stations are included in the
    filter, the results will include the dataset's for each station within
    that time frame.

    :param  start_time=:    POSIX timestamp for time frame of data requested.
    :param  end_time=:      POSIX timestamp for time frame of data requested.
    :param  stations=:      A list of station_ids to include in the data set.
    :return:
    """

    input = request.json
    start_time = input.get("start_time", 0)
    end_time = input.get("end_time", arrow.now().timestamp)
    station_ids = input.get("stations", [])

    stations_list = []
    if len(station_ids) > 0:
        for station_id in station_ids:
            stations_list.append(db.sesssion.query(Station).join(Station.data_points).filter(Data.created_at >= arrow.get(start_time), Data.created_at <= arrow.get(end_time)))
        return jsonify({
            "data": stations_list,
            "number_results": len(station_ids),
            "query": {
                "start_time": start_time,
                "end_time": end_time,
                "station_ids": station_ids
            }
        })
    else:
        station = db.session.query(Station).join(Station.data_points).filter(Data.created_at >= arrow.get(start_time), Data.created_at <= arrow.get(end_time)).all()
        data = [s.serialize_data() for s in station]
        return jsonify({
            "data": data,
            "number_results": len(station),
            "query": {
                "start_time": start_time,
                "end_time": end_time,
                "station_ids": station_ids
            }
        })


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

    data_points = Data.query.filter_by(station_id=station.id).order_by(Data.created_at.desc()).paginate(page, results_per_page)

    data = [d.serialize() for d in data_points.items]
    response = {
        'station': {
            'id': station.name,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'name': station.long_name
        },
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
    print form
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




