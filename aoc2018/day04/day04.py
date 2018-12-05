import re
from datetime import datetime
from collections import defaultdict
from util import argmax

# [1518-05-20 23:57] Guard #2207 begins shift
# [1518-05-19 00:20] falls asleep
# [1518-05-14 00:54] wakes up
ts_re = re.compile(r'\[(?P<ts>.*)\]')
start_re = re.compile(r'\[(?P<ts>.*)\] Guard #(?P<guard>\d+) begins shift')
sleep_re = re.compile(r'\[(?P<ts>.*)\] falls asleep')
wake_re = re.compile(r'\[(?P<ts>.*)\] wakes up')

# Read/sort lines
lines = sorted([l.rstrip() for l in open('input.txt')])

guards = defaultdict(lambda: defaultdict(lambda: []))
guard = None
asleep_start = None
total_asleep = defaultdict(lambda: 0)
min_count = defaultdict(lambda: [0] * 60)

for line in lines:
    print(line)

    # Parse datetime
    timestamp = ts_re.search(line)
    if not timestamp:
        raise ValueError("Invalid timestamp: " + line)

    dt = datetime.strptime(timestamp.group('ts'), "%Y-%m-%d %H:%M")

    # Parse rest of the line and update state
    match = start_re.search(line)
    if match:
        guard = match.group('guard')
        asleep_start = None  # ??
        continue

    match = sleep_re.search(line)
    if match:
        if asleep_start:
            raise ValueError("Guard already asleep!")

        asleep_start = dt
        continue

    match = wake_re.search(line)
    if match:
        if not asleep_start:
            raise ValueError("guard already awake!")

        guards[guard][dt.date()].append((asleep_start, dt))
        total_asleep[guard] += (dt - asleep_start).total_seconds() / 60

        for m in range(asleep_start.minute, dt.minute):
            min_count[guard][m] += 1

        asleep_start = None


# Find the guard that slept the most
record = max(total_asleep.items(), key=lambda x: x[1])
guard, slept = record
print("Guard slept the most: {}, {} mins".format(guard, slept))

# Find the minute he slept the most
minutes = [0] * 60
for intervals in guards[guard].values():
    for (start, stop) in intervals:
        for minute in range(start.minute, stop.minute):
            minutes[minute] += 1

# Print the max
sleepiest_min = max(list(enumerate(minutes)), key=lambda x: x[1])
print("Sleepiest at: minute {}, count={}".format(sleepiest_min[0], sleepiest_min[1]))

print("Part-1 Answer: {}".format(int(guard) * sleepiest_min[0]))

# Find the guard that spent the same minute asleep the most
aa = {g: max(minutes) for g, minutes in min_count.items()}
guard_max, min_max = max(aa.items(), key=lambda x: x[1])

print("Part 2 Answer: {}".format(int(guard_max) * argmax(min_count[guard_max])))
