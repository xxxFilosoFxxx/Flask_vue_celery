import os


class Config(object):
    DEBUG = False if os.getenv('PROJECT_ENV') == 'prod' else True
    SECRET_KEY = os.getenv('APP_SECRET', 'secret_key')
    TESTING = False
    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'dist')
    LOG_PATH = os.path.abspath(ROOT_DIR) + '/error.log'
    # LOG_PATH = os.path.abspath(os.path.dirname(__file__)) + '/error.log'
    CSRF_ENABLES = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://test:test@localhost/tasks_docs')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
    RESULT_BACKEND = os.environ.get('RESULT_BACKEND',
                                    'db+postgresql://test:test@localhost/tasks_docs')

    if not os.path.exists(DIST_DIR):
        raise Exception(f'DIST_DIR not found: {DIST_DIR}')
    # ВОЗМОЖНО -> db+postgresql+psycopg2://test:test@localhost/tasks_docs_meta
