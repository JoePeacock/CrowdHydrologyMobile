from wtforms import Form, TextField, PasswordField, validators


class RegistrationForm(Form):
    station_id = TextField('Station Identification Number:',
                           [validators.Required()])
    water_level = TextField('Water Level:', [validators.Required()])
    username = TextField('Username:', [validators.Required(),
                                       validators.Length(min=4, max=25)])
    email = TextField('Email:', [validators.Required(),
                                 validators.Length(min=6, max=45)])
    password = PasswordField('Password:', [validators.Required(),
                                           validators.EqualTo('confirm')])
    confirm = PasswordField('Confirm Password:', [validators.Required()])
    image = TextField('Profile Picture (URL):')


class EventForm(Form):
    event_name = TextField('Event Name:', [validators.Required(),
                                           validators.Length(min=1, max=25)])
    event_date = TextField('Event Date:', [validators.Required()])
    event_start_time = TextField('Start Time:', [validators.Required(),
                                                 validators.Length(min=4,
                                                                   max=5)])
    event_description = TextField('Description:', [validators.Required()])
    event_number_of_people = TextField('Number of People Needed: ',
                                       [validators.Required(),
                                        validators.Length(min=1, max=3)])
    event_location_description = TextField('Location Description:')
    event_geolocation = TextField('Event Geo-Location:',
                                  [validators.Required()])


class EditImage(Form):
    image = TextField('Profile Picture (URL):')


