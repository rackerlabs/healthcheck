import os
from healthcheck import create_app
from flask_script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

if __name__ == '__main__':
    app.run(port=5000)
