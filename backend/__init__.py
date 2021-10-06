from flask import render_template, jsonify, request, url_for, flash, redirect
from flask_login import login_required, logout_user
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


# Результаты и сами данные в RabbitMQ не сохраняются
@app.route('/status/<task_id>', methods=['GET'])
@login_required
def task_status(task_id):
    try:
        # TODO: при смене статуса обновлять статус в БД
        task = send_task.AsyncResult(task_id)
        if task.state == 'PENDING':  # Цвет -> Желтый
            response = {
                'task_id': task_id,
                'state': task.state,  # status
                'task_result': task.result,  # None
                'info': str(task.info)
            }
        elif task.state != 'FAILURE':  # Цвет -> Зеленый/Оранжевый
            response = {
                'task_id': task_id,
                'state': task.state,
                'task_result': task.result,  # task.info.get('result', None)
                'info': str(task.info)
            }
            if task.state == 'SUCCESS':  # Цвет -> Зеленый
                # Запись в БД данных при успешно выполенной задаче
                # TODO: op.send_attr
                # op.send_success_result_task(uuid=task_id,
                #                             msisdn=response['task_result']['msisdn'],
                #                             radius=response['task_result']['radius'],
                #                             delta=response['task_result']['delta'])
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
