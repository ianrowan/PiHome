from flask import Flask
from flask_ask import Ask, statement, question
import subprocess
import time

app = Flask(__name__)
ask = Ask(app, '/')


def roku_sequence(app):
    sequences = {"cnbc": ['right', 'right', 'up', 'up'],
                 'netflix': ['right'],
                 'amazon prime': ['right', 'right'],
                 'curiosity stream': ['right', 'right', 'right'],
                 'h.b.o': ['right', 'right', 'down'],
                 'showtime': ['right', 'down']
                 }
    for i in sequences[app.lower()]:
        print("irsend SEND_ONCE roku KEY_{}".format(i.upper()))
        subprocess.call(['irsend', 'SEND_ONCE', 'roku', 'KEY_{}'.format(i.upper())])
        time.sleep(0.3)
    subprocess.call(['irsend', 'SEND_ONCE', 'roku', 'KEY_ENTER'])

@ask.intent('TvControl')
def api_entry(val):
    print(val)
    print("irsend SEND_ONCE tv KEY_POWER")
    subprocess.call(['irsend', 'SEND_ONCE', 'tv', 'KEY_POWER'])
    if str(val) == "on":
        time.sleep(28)
        return question("Your tv is turning {}, What would you like to watch?".format(str(val)))
    else:
        return statement("Your tv is turning Off")


@ask.intent('VolumeControl')
def control_volume(direction, delta):
    print("Volume is turning {} {}".format(direction, delta))
    for i in range(int(delta)):
        print("irsend SEND_ONCE tv KEY_VOLUME{}".format(direction.upper()))
        subprocess.call(['irsend', 'SEND_ONCE', 'tv', 'KEY_VOLUME{}'.format(direction.upper())])
        time.sleep(0.75)
    return statement("Volume has been turned {} {}".format(direction, delta))


@ask.intent('Roku')
def control_roku(app):
    # first, go to home
    print("irsend SEND_ONCE roku KEY_HOME")
    subprocess.call(['irsend', 'SEND_ONCE', 'roku', 'KEY_HOME'])
    time.sleep(.5)
    # call function which takes input of sequence
    roku_sequence(app)

    yield statement("Opening" + app)

    if app.lower() == 'cnbc':
        time.sleep(5)
        subprocess.call(['irsend', 'SEND_ONCE', 'roku', 'KEY_BACK'])
        time.sleep(2)
        subprocess.call(['irsend', 'SEND_ONCE', 'roku', 'KEY_ENTER'])

@ask.intent('FireplaceOn')
def control_fire():

    for i in range(4):
        print("irsend SEND_ONCE fire KEY_POWER")
        subprocess.call(['irsend', 'SEND_ONCE', 'fire', 'KEY_POWER'])
        time.sleep(.85)
    return statement("Enjoy the fire!")

@ask.intent('FireplaceOff')
def control_fire_off():
    print("irsend SEND_ONCE fire KEY_POWER")
    subprocess.call(['irsend', 'SEND_ONCE', 'fire', 'KEY_POWER'])
    return statement("The fire has been put out")


if __name__ == "__main__":
    app.run()


