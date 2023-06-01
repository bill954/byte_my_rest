from celery import shared_task
from time import sleep

# function made to make a first test with celery
@shared_task
def sleep_message():
    sleep(5)
    return 'after sleeeeep'