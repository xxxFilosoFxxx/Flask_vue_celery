from flask import render_template, jsonify, request
from flask_login import login_required, logout_user, current_user
from backend.app import app
from backend.utils import operations_utils as op
from backend.utils.common_utils import process_log_string
from backend.celery_tasks import send_task


@app.route('/')
@login_required
def index():
    try:
        return render_template('index.html')
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/', defaults={'path': ''})
@app.route('/<path>')
def catch_all(path):
    try:
        return render_template("index.html")
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Вы успешно вышли из системы', 'path': '/login'})
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/status_tasks', methods=['GET'])
@login_required
def status_tasks():
    try:
        # response = {
        #     'tasks': op.get_tasks_status(current_user.username)
        # }
        tasks_id = op.get_user_tasks(current_user.username)
        all_user_task = {}
        for uuid in tasks_id:
            all_user_task[uuid] = send_task.AsyncResult(uuid).state
        response = {
            'tasks': all_user_task
        }
        return jsonify(response), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/all_result_tasks', methods=['GET'])
@login_required
def all_result_tasks():
    try:
        # response = op.get_user_tasks(current_user.username)
        response = []
        tasks_id = op.get_user_tasks(current_user.username)
        for uuid in tasks_id:
            result = send_task.AsyncResult(uuid)
            if result.state == 'PENDING':
                task = {
                    'task_id': uuid,
                    'msisdn': None,
                    'radius': None,
                    'delta': None,
                    'status': result.state
                }
                response.append(task)
            elif result.state != 'FAILURE':
                task = {
                    'task_id': uuid,
                    'msisdn': result.result['msisdn'],
                    'radius': result.result['radius'],
                    'delta': result.result['delta'],
                    'status': result.state
                }
                response.append(task)
            else:
                response = {
                    'task_id': uuid,
                    'msisdn': None,
                    'radius': None,
                    'delta': None,
                    'status': result.state
                }
        return jsonify(response), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


@app.route('/result_task/<task_id>', methods=['GET'])
@login_required
def result_task(task_id):
    try:
        task = send_task.AsyncResult(task_id)
        if task.state == 'PENDING':  # Цвет -> Синий
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,  # None
                'info': str(task.info)  # Содержит task.result в формате json
            }
        elif task.state != 'FAILURE':  # Цвет -> Зеленый/Желтай
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,
                'info': str(task.info),
            }
            if task.state == 'SUCCESS':  # Цвет -> Зеленый
                # Здесь можно получить результат после выполнения
                response = {
                    'task_id': task_id,
                    'state': task.state,
                    'task_result': task.result,
                    'info': str(task.info),
                    'date_done': task.date_done.strftime('%H:%M | %d %B %Y')
                }
                pass
        else:
            # Ошибка на стороне сервера (или где-то еще)
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,
                'info': str(task.info)  # Цвет -> Красный
            }
        return jsonify(response), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise
