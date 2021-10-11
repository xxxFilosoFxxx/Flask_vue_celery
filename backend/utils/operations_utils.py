from backend.app import db
from backend.models import Result, User
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


def send_task_progress(uuid: str, status: str, username: str) -> None:
    user_id = User.query.filter_by(username=username).first().id
    task = Result(uuid=uuid, status=status, user_id=user_id)
    db.session.add(task)
    session_commit()


def task_update_attr(uuid: str, msisdn: float, radius: float, delta: float, status: str) -> None:
    task = Result.query.filter_by(uuid=uuid).first()
    if task.status != status:
        task.set_status(status)
        task.set_attr(msisdn, radius, delta)
        db.session.add(task)
        session_commit()


def task_update_status(uuid: str, status: str) -> None:
    task = Result.query.filter_by(uuid=uuid).first()
    if task.status != status:
        task.set_status(status)
        db.session.add(task)
        session_commit()


def get_user_tasks(username: str) -> dict:
    user_id = User.query.filter_by(username=username).first().id
    tasks = Result.query.filter_by(user_id=user_id).all()
    all_user_task = {task.uuid: task.status for task in tasks}
    return all_user_task


# def send_status_task(event, response, room):
#     emit(event, {'response': response}, namespace='/', room=room)


# TODO: дописать
def get_user_task():
    pass
