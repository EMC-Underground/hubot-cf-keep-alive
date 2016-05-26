from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import events
from flask import Flask, request, jsonify
import os, time, requests, json

app = Flask(__name__)
scheduler = BackgroundScheduler()
port = int(os.getenv('VCAP_APP_PORT', 8080))

def keep_alive():
  url = os.getenv('HUBOT_URL')
  r = requests.post('{0}hubot/alive'.format(url), data = json.dumps({'message':'Staying alive!','room':'{0}'.format(os.getenv('HUBOT_ROOM'))}))

# listener to give visibility into job completetion
def error_listener(event):
  if event.exception:
    print("The job failed...{0}".format(event.exception))
    print("{0}".format(event.traceback))
  else:
    print("The job worked!")

# Routes
@app.route('/')
def hello_world():
  return 'Hello World!'


if __name__ == '__main__':
  scheduler.add_job(keep_alive, 'interval', hours=8)
  scheduler.add_listener(error_listener, events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR)
  scheduler.start()

  try:
    app.run(host='0.0.0.0', port=port)

  except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
