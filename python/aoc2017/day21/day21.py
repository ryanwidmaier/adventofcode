import numpy as np


def grid_from_pattern(pattern):
    rows = [[1 if ch == '#' else 0 for ch in row] for row in pattern.split('/')]
    return np.array(rows)


class Rule(object):
    def __init__(self, pattern, output):
        self.patterns = [grid_from_pattern(pattern)]
        self.patterns.append(np.rot90(self.patterns[-1]))
        self.patterns.append(np.rot90(self.patterns[-1]))
        self.patterns.append(np.rot90(self.patterns[-1]))
        self.patterns.append(np.fliplr(self.patterns[0]))
        self.patterns.append(np.rot90(self.patterns[-1]))
        self.patterns.append(np.rot90(self.patterns[-1]))
        self.patterns.append(np.rot90(self.patterns[-1]))

        self.output = grid_from_pattern(output)

    def is_match(self, grid):
        for p in self.patterns:
            if np.array_equal(p, grid):
                return True

        return False


class RuleSet(object):
    def __init__(self, input_file):
        # Parse the rules
        self.rules = []
        fin = open(input_file)
        for line in fin:
            line = line.rstrip()
            pattern, output = line.split(' => ')

            self.rules.append(Rule(pattern, output))

    def replace(self, in_grid):
        for rule in self.rules:
            if rule.is_match(in_grid):
                return rule.output

        raise ValueError("No matches!!!!")



rule_set = RuleSet('input.txt')

# Now run the simulation
image = grid_from_pattern('.#./..#/###')
print image

for i in xrange(18):
    size = image.shape[0]
    split_size = 2 if size % 2 == 0 else 3

    # Convert the sub images
    output = []
    for r in xrange(0, size, split_size):
        output.append([])
        for c in xrange(0, size, split_size):
            in_grid = image[r:r+split_size, c:c+split_size]
            output[-1].append(rule_set.replace(in_grid))

    # Put the image back together
    output_rows = [reduce(lambda left, right: np.concatenate((left, right), axis=1), row) for row in output]
    image = reduce(lambda top, bot: np.concatenate((top, bot), axis=0), output_rows)

    print ""
    print "Iteration {}".format(i+1)
    print image

print "Pixels On: ", np.count_nonzero(image)
print "size: ", image.shape[0] * image.shape[1]
