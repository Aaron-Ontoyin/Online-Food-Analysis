import time


def gen_sequence(sequence: str):
    """
    Generate a sequence of characters from a given string.

    Args:
        sequence (str): The input string.

    Yields:
        str: The next character in the sequence.

    """
    for char in sequence.split():
        yield char + " "
        time.sleep(0.05)
