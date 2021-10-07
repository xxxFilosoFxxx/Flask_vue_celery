from backend.app import celery
import time
# from backend.utils.operations_utils import send_status_task


# В конце обработки задачи закидывает данные в БД
@celery.task(bind=True)
def send_task(self, msisdn: float, radius: float, delta: float, room) -> dict:
    self.update_state(state='PROGRESS',
                      meta={'msisdn': msisdn, 'radius': radius, 'delta': delta})
    # send_status_task('status', 'PROGRESS', room)
    time.sleep(5)
    return {'msisdn': msisdn, 'radius': radius, 'delta': delta}
