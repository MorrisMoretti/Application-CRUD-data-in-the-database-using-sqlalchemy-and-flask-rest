from config import Config
from web_courses import app

if __name__ == '__main__':
    app.config.from_object(Config)
    app.run()
