# from typing import List, Dict, Any
from backend.app import db
from backend.models import UserTasks, User
from flask_login import login_user


def session_commit() -> None:
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception('Не удалось совершить коммит - ', e.__class__)


def add_user_to_db(username: str, password: str) -> bool:
    user_check = User.query.filter_by(username=username).first()
    if user_check is not None:
        return False
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    session_commit()
    return True


def check_validate_user(username: str, password: str) -> bool:
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    return False


def check_login_user(username: str, remember: bool) -> None:
    user = User.query.filter_by(username=username).first()
    login_user(user, remember=remember)


def send_task_progress(uuid: str, username: str) -> None:
    user_id = User.query.filter_by(username=username).first().id
    task = UserTasks(uuid=uuid, user_id=user_id)
    db.session.add(task)
    session_commit()


# def serialize_query(query):
#     return {
#         'task_id': query.task_id,
#         'result': query.result.tobytes().decode('utf-8', errors='ignore').replace(
#             '\x05C\x00\x00\x00\x00\x00\x00\x00?', ''),
#         'status': query.status
#     }


def get_user_tasks(username: str) -> list:  # List[Dict[str, Any]]
    user_id = User.query.filter_by(username=username).first().id
    tasks = UserTasks.query.filter_by(user_id=user_id).all()
    tasks_id = [i.uuid for i in tasks]
    # query = [serialize_query(task) for task in db.engine.execute('select * from celery_taskmeta order by date_done')
    #          if task.task_id in tasks_id]
    # return query
    return tasks_id


def get_tasks_status(username: str) -> dict:
    user_id = User.query.filter_by(username=username).first().id
    tasks = UserTasks.query.filter_by(user_id=user_id).all()
    all_user_task = {task.uuid: task.status for task in tasks}
    # all_user_task = {}
    # for i in tasks:
    #     all_user_task[i.uuid] = db.engine.execute('select status from celery_taskmeta where task_id like %s',
    #                                               i.uuid).fetchone()[0]
    return all_user_task
