import random
from argparse import ArgumentParser


class State:

    def __init__(self, token):
        self.token = token
        self.total = 0
        self.transitions = {}

    def has_transition(self, transition):
        return transition in self.transitions

    def add_transition(self, transition):
        self.transitions[transition] = 0

    def add_transition_count(self, transition):
        self.transitions[transition] += 1
        self.total += 1


def get_count_table(file):
    count_table = {}
    with open(file) as data_file:
        content = data_file.read().lower()

        # Strip most punctuation
        content = content.translate(str.maketrans(' ', ' ', r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~—’‘”“"""))

        # Some file specific normalisation
        tokens = content.replace('\n\n', ' ').replace('...', '').replace('…', '').split(' ')

        for index, token in enumerate(tokens[:-1]):

            token = token.rstrip()

            if token not in count_table:
                count_table[token] = State(token)

            next_token = tokens[index + 1]

            if not count_table[token].has_transition(next_token):
                count_table[token].add_transition(next_token)

            count_table[token].add_transition_count(next_token)

    return count_table


def get_transition_table(file):
    transition_table = {}

    count_table = get_count_table(file)

    for key, state in count_table.items():
        transition_table[key] = {}

        for token, count in state.transitions.items():
            # Assign probability between 0-1
            transition_table[key][token] = count / state.total

    return transition_table


def get_random_transition(transitions):
    x = random.random()

    for token, weight in transitions.items():
        if x <= weight:
            return token
        x -= weight

    raise Exception('Was not able to get random transition')


def get_args():
    parser = ArgumentParser()

    parser.add_argument('--file', type=str, help='The text file to read')
    parser.add_argument('--start', type=str, help='The word to start the chain')
    parser.add_argument('--count', type=int, help='The amount of words to generate')

    return parser.parse_args()


def main():
    args = get_args()
    transition_table = get_transition_table(args.file)

    output = []

    current = args.start.lower()
    for x in range(args.count):
        output.append(current)
        current = get_random_transition(transition_table[current])

    print(' '.join(output))


if __name__ == '__main__':
    main()
