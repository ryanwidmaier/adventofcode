import re

class Bot(object):
    def __init__(self, id_):
        self.id = id_
        self.value = None
        self.low = None
        self.high = None

    def set_outputs(self, low, high):
        self.low = low
        self.high = high

    def accept(self, value):
        print "{} accepts {}".format(self.id, value)

        # First value, store, and stop
        if not self.value:
            self.value = value
            return

        # Second value, need to pass them along
        low_val, high_val = min(value, self.value), max(value, self.value)
        print "{} compared {} and {}".format(self.id, low_val, high_val)

        if not self.low or not self.high:
            raise ValueError("Bot {} doesn't have rule".format(self.id))

        print "{} sends {} to {}".format(self.id, low_val, self.low.id)
        print "{} sends {} to {}".format(self.id, high_val, self.high.id)

        # Pass values along
        self.value = None
        self.low.accept(low_val)
        self.high.accept(high_val)


class Output(object):
    def __init__(self, id_):
        self.id = id_
        self.values = []

    def accept(self, value):
        self.values.append(value)


class System(object):
    def __init__(self):
        self.actors = {}

    def program_bot(self, bot_id, low_dest, high_dest):
        bot = self.get_or_create_actor(bot_id)
        low = self.get_or_create_actor(low_dest)
        high = self.get_or_create_actor(high_dest)

        bot.set_outputs(low, high)

    def get_or_create_actor(self, actor_id):
        if actor_id in self.actors:
            return self.actors[actor_id]

        # else, need to create it
        actor = None
        if actor_id.startswith('bot'):
            actor = Bot(actor_id)
        else:
            actor = Output(actor_id)

        self.actors[actor_id] = actor
        return actor

    def send_input(self, dest, value):
        actor = self.actors[dest]
        actor.accept(value)


# Parsing RE's
give_re = re.compile(r'(bot \d+) gives low to (\w+ \d+) and high to (\w+ \d+)')
input_re = re.compile(r'value (\d+) goes to (bot \d+)')

system = System()

# First pass initializes all the bots programming
with open('input.txt') as infile:
    for line in infile:
        line = line.rstrip()

        match = give_re.match(line)
        if match:
            bot, low_dest, high_dest = match.group(1), match.group(2), match.group(3)
            system.program_bot(bot, low_dest, high_dest)

with open('input.txt') as infile:
    for line in infile:
        line = line.rstrip()

        match = input_re.match(line)
        if match:
            value, bot = int(match.group(1)), match.group(2)
            system.send_input(bot, value)


a = system.actors['output 0'].values[0]
b = system.actors['output 1'].values[0]
c = system.actors['output 2'].values[0]

print a*b*c
