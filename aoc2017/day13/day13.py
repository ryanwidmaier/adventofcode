



def parse_layers():
    fp = open('input.txt')

    layers = []
    for line in fp:
        line = line.rstrip()
        depth, layer_range = line.split(': ')
        depth = int(depth)
        layer_range = int(layer_range)

        while len(layers) < depth:
            layers.append(0)

        layers.append(layer_range)

    return layers


def traverse(layers, delay=0, abort=False):
    score = 0

    for depth, layer_range in enumerate(layers):
        if layer_range == 0:
            continue

        security_pos = (depth + delay) % (layer_range * 2 - 2)
        if security_pos == 0:
            if abort:
                return 1

            score += depth * layer_range

    return score


layers_ = parse_layers()
result = traverse(layers_)

print result

score = 1
start = 171428 - 1
while score > 0:
    start += 1
    score = traverse(layers_, start, True)

    if start % 5000 == 0:
        print "{} iterations".format(start)

print "Safe pass: ", start
