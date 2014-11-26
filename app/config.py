import os

CSRF_ENABLED = True
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
SECRET_KEY = 'F5W4sSeiSsbU4lB+SdXX1sBS4cgk6ZUs1gstMNiSgyMMzkvcF0+IGVZCOLAkJbzCYPZeItyGgfL0JPkpsxOY2+BysVWCGEKssqT4zu4gAXws1DsPH4v0F/LIie0kevAFuneFVbqM3CdFy/IRvffXUzD8nhvjEVKbwhLpUediUXE='

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
