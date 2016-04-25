from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import events
import os

scheduler = BackgroundScheduler()

def keep_alive():
  url = os.getenv('HUBOT_URL')
  r = requests.post(url, data = json.dumps({"Message":"Staying alive!"}))

if __name__ == '__main__':
  scheduler.add_job(keep_alive, 'interval', seconds=20)
  scheduler.add_listener(error_listener, events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR)
  scheduler.start()

  try:
    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
      time.sleep(2)
  except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
