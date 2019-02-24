from flask import Flask
from flask_ask import Ask, statement
import subprocess
import time

app = Flask(__name__)
ask = Ask(app, '/')


def roku_sequence(app):
    sequences = {"cnbc": ['right', 'right', 'up', 'up'],
                 'netflix': ['right'],
                 'amazon prime': ['right', 'right']}
    for i in sequences[app.lower()]:
        print("irsend SEND_ONCE roku KEY_{}".format(i.upper()))
        subprocess.call(['irsend', 'SEND_ONCE', 'tv', 'KEY_{}'.format(i.upper())])
        time.sleep(0.5)
    subprocess.call(['irsend', 'SEND_ONCE', 'roku', 'KEY_ENTER'])


@ask.intent('TvControl')
def api_entry(val):
    print(val)
    print("irsend SEND_ONCE tv KEY_POWER")
    subprocess.call(['irsend', 'SEND_ONCE', 'tv', 'KEY_POWER'])
    return statement("Your tv is turning {}".format(val))


@ask.intent('VolumeControl')
def control_volume(direction, delta):
    print("Volume is turning {} {}".format(direction, delta))
    for i in range(int(delta)):
        print("irsend SEND_ONCE tv KEY_VOLUME{}".format(direction.upper()))
        subprocess.call(['irsend', 'SEND_ONCE', 'tv', 'KEY_VOLUME{}'.format(direction.upper())])
        time.sleep(0.5)
    return statement("Volume has been turned {} {}".format(direction, delta))

@ask.intent('Roku')
def control_roku(app):
    # first, go to home
    print("irsend SEND_ONCE roku KEY_HOME")
    subprocess.call(['irsend', 'SEND_ONCE', 'roku', 'KEY_HOME'])
    # call function which takes input of sequence
    roku_sequence(app)
    return statement("Opening" + app)

if __name__ == "__main__":
    app.run()


