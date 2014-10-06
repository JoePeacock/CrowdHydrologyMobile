from flask import Flask
app = Flask(__name__)

from app import views
#app.config.from_object('config')

if __name__ == '__main__':
	app.run()