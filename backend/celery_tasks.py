from backend.app import celery
import time


@celery.task(bind=True)
def send_task(self, msisdn: float, radius: float, delta: float) -> dict:
    self.update_state(state='PROGRESS',
                      meta={'msisdn': msisdn, 'radius': radius, 'delta': delta})
    time.sleep(5)
    return {'msisdn': msisdn, 'radius': radius, 'delta': delta}
