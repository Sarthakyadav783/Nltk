import random
import string


def perform_operation(characters: str, add_transposition=False) -> str:
    """ randomly choose between add, replace, delete, (or transposition, if allowed) 
    for the given character, return resulting substring,
    all operations other than transposition are performed on first char,
    transposition will switch both of them
    """
    insert = "insert"
    replace = "replace"
    delete = "delete"
    choices = [insert, replace, delete]

    transposition = "transposition"
    if add_transposition:
        choices.append(transposition)

    choice = random.choice(choices)

    if choice == delete:
        return ""
    elif choice == transposition:
        assert len(characters) == 2
        return characters[1] + characters[0]
    else:
        new_char = random.choice(string.ascii_letters)
        if choice == replace:
            return new_char
        # choice is insert
        return new_char + characters[0]


def noisy(prompt: str, strength: float, transposition=False) -> str:
    """
    Given input string, add noise and return.
    Strength must be between 0 and 1, where 
    strength == 0 --> same prompt being returned
    strength == 1 --> will perform a change on every character

    transposition is an optional operation that could be applied in
    along with the other three (by default set to false)
    """

    noisy_prompt = ''
    prev_char_transposed = False
    n = len(prompt)
    for i in range(n):
        char = prompt[i]
        if prev_char_transposed:
            # previous character swapped with current character;
            # so char should refer to previous one
            char = prompt[i - 1]
            prev_char_transposed = False
            continue
        if char == " " or random.random() > strength:
            # no change
            noisy_prompt += char
        else:
            received_substring = ""
            if i + 1 == n:
                # last char; transposition NOT ALLOWED
                received_substring += perform_operation(
                    char, add_transposition=False)
            else:
                received_substring += perform_operation(
                    char + prompt[i + 1], add_transposition=transposition)

            noisy_prompt += received_substring
            if len(received_substring) == 2:
                prev_char_transposed = True

    return noisy_prompt
