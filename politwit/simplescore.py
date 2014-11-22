"""A dummy module for scoring users."""

import random

def score():
	score = random.randint(0, 100)
	print score
	return score


if __name__ == "__main__":
	score()