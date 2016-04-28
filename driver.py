from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import events
import os, time, requests, json

scheduler = BackgroundScheduler()

def keep_alive():
  url = os.getenv('HUBOT_URL')
  r = requests.post("{0}hubot/alive".format(url), data = json.dumps({"message":"Staying alive!","room":"{0}".format(os.getenv('HUBOT_ROOM'))}))

# listener to give visibility into job completetion
def error_listener(event):
  if event.exception:
    print("The job failed...{0}".format(event.exception))
    print("{0}".format(event.traceback))
  else:
    print("The job worked!")

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
