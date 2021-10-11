from flask import render_template, jsonify, request, session
from flask_login import login_required, logout_user, current_user
# from flask_socketio import join_room, leave_room, close_room, emit
from backend.app import app  #, socketio
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
        # leave_room(room=current_user.username, sid=request.sid, namespace='/')
        # close_room(room=current_user.username, namespace='/')
        logout_user()
        return jsonify({'message': 'Вы успешно вышли из системы', 'path': '/login'})
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


# @socketio.on('join_room')
# @login_required
# def socket_connect():
#     print(f'Отправка сообщения на сервер от пользователя {current_user.username}!')
#     join_room(current_user.username)
#     emit('confirm', {'msg': 'Соединение от сервера'}, room=current_user.username)
#
#
# @socketio.on('status')
# @login_required
# def socket_send_tasks(data):
#     print(data['message'])
#     emit('tasks', {'tasks_user': op.get_user_tasks(current_user.username)}, room=current_user.username)


@app.route('/status_tasks', methods=['GET'])
# @login_required
def tasks_status():
    try:
        # response = {
        #     'tasks': op.get_user_tasks(current_user.username)
        # }
        # return jsonify(response), 200
        if current_user.is_authenticated:
            response = {
                'tasks': op.get_user_tasks(current_user.username)
            }
            return jsonify(response), 200
        else:
            response = {
                'tasks': {
                    'wfageshrdw': 'OK',
                    'fwfga24214': 'OK',
                    'fwafgafwaa': 'OK'
                }
            }
            return jsonify(response)
    except Exception:
        app.logger.exception(process_log_string(request))
        raise


# Результаты и сами данные в RabbitMQ не сохраняются
@app.route('/status/<task_id>', methods=['GET'])
@login_required
def task_status(task_id):
    try:
        task = send_task.AsyncResult(task_id)
        if task.state == 'PENDING':  # Цвет -> Желтый
            # Запись в БД статуса о начале выполнения задачи
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,  # None
                'info': str(task.info)  # Содержит task.result в формате json
            }
            op.task_update_status(task_id, task.state)
        elif task.state != 'FAILURE':  # Цвет -> Зеленый/Оранжевый
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,
                'info': str(task.info),
                'date_done': task.date_done.strftime('%H:%M | %d %B %Y')
            }
            if task.state == 'SUCCESS':  # Цвет -> Зеленый
                # Запись в БД данных при успешно выполенной задаче
                # op.task_update_attr(uuid=task_id,
                #                     msisdn=response['task_result']['msisdn'],  # TODO
                #                     radius=response['task_result']['radius'],
                #                     delta=response['task_result']['delta'],
                #                     status=task.state)
                pass
        else:
            # Ошибка на стороне сервера (или где-то еще)
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,
                'info': str(task.info)  # Цвет -> Красный
            }
            # Запись в БД провального статуса задачи
            # op.task_update_status(task_id, task.state)
        return jsonify(response), 200
    except Exception:
        app.logger.exception(process_log_string(request))
        raise
