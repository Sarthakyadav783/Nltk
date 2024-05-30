import random, string


def perform_operation(character: str) -> str:
    """ randomly choose between add, replace, or delete for the given character,
    return resulting substring
    """

    insert = "insert"
    replace = "replace"
    delete = "delete"
    choice = random.choice([insert, replace, delete])

    if choice == delete:
        return ""
    else:
        new_char = random.choice(string.ascii_letters)
        if choice == replace:
            return new_char
        # choice is insert
        return new_char + character


def noisy(prompt: str, strength: float) -> str:
    """
    Given input string, add noise and return.
    Strength must be between 0 and 1, where 
    strength == 0 --> same prompt being returned
    strength == 1 --> will perform a change on every character
    """

    noisy_prompt = ''

    for char in prompt:
        if char == " " or random.random() > strength:
            noisy_prompt += char
        else:
            # perform change
            noisy_prompt += perform_operation(char)
    return noisy_prompt