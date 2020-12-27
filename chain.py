from argparse import ArgumentParser
from typing import List, Tuple, Dict

import numpy as np


def get_content(file: str) -> Tuple[List[str], List[str], dict]:
    with open(file) as data_file:
        content = data_file.read().lower()

        # Strip most punctuation
        content = content.translate(str.maketrans(' ', ' ', r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~—’‘”“"""))

        # Some file specific normalisation
        content = content.replace('\n\n', ' ').replace('\n', ' ').replace('...', '').replace('…', '').split(' ')

        words = list(set(content))

        word_index = {token: index for index, token in enumerate(words)}

        return content, words, word_index


def get_transition_matrix(content: List[str], word_index: Dict[str, int]) -> np.ndarray:
    matrix = np.zeros((len(word_index), len(word_index)))

    # Work out the transitioning counts for each token
    for index, word in enumerate(content[:-1]):
        matrix[word_index[word], word_index[content[index + 1]]] += 1

    # Convert to probabilities
    for index, row in enumerate(matrix):
        matrix[index] = row / row.sum()

    return matrix


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('--file', type=str, help='The text file to read')
    parser.add_argument('--start', type=str, help='The word to start the chain')
    parser.add_argument('--count', type=int, help='The amount of words to generate')

    return parser.parse_args()


def simulate(matrix: np.ndarray, words: List[str], word_index: Dict[str, int], start: str, count: int) -> str:
    output = [''] * count

    output[0] = start

    index = word_index[start]

    index_range = np.arange(matrix[0].size)

    # Start at 1 since we already have the starting word.
    for i in range(1, count):
        probabilities = matrix[index]

        # Take a random number in the range 0-size so we can get the
        # index for the transition matrix.
        index = np.random.choice(
            index_range,
            p=probabilities,
            replace=False
        )

        output[i] = words[index]

    return ' '.join(output)


def main():
    args = parse_args()

    start = args.start.lower()

    content, words, words_index = get_content(args.file)

    if start not in words:
        print(f'Unable to start on {start}')
        exit(1)

    matrix = get_transition_matrix(content, words_index)

    print(simulate(matrix, words, words_index, start, args.count))


if __name__ == '__main__':
    main()
