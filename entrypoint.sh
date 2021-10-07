sudo service rabbitmq-server start
sudo rabbitmq-plugins enable rabbitmq_management

[Если БД не установлена и нет базы]
#  (Установить psql)
  sudo apt install postgresql postgresql-contrib
#  (Создание базы)
  sudo -u postgres psql
  create database tasks_docs;
  create user test;
  alter database task_docs owner to test;
  alter user test with encrypted password 'test';
#  (migrate БД)
  python3 manage.py db init
  python3 manage.py db migrate
  python3 manage.py db upgrade

export APP_SETTINGS="backend.config.Config"
export APP_SECRET="Super secret key"
export DATABASE_URL="postgresql://test:test@localhost/tasks_docs" # Ваш url

export PROJECT_ENV="prod"

[Для запуска celery]
celery -A backend.app.celery worker -l info


[Если другой адрес для очереди задач]
  export CELERY_BROKER_URL="amqp://guest:guest@localhost:5672//" # Ваш url
  export RESULT_BACKEND="db+postgresql+psycopg2://test:test@localhost/tasks_docs" # Ваш url
