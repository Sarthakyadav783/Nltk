from handler import handle_spellcheck
from add_noise import noisy
import string
import re


if __name__ == "__main__":

    # for char in string.punctuation:
    #     input = "I went to the park with my friend Kushagra" + char + " Vagisha joined us later" + char
    #     prompt = punctuation_spacing(input)

    # name = "J. V. Ramana"
    # input = add_noise.noisy(" How many votes did ", 0.15) + \
    #     add_noise.noisy(name, 0) + add_noise.noisy(",. have? ", 0.15)
    prompts = ["What is the status of the election? Did Ashok win",
               "What is status of election?",
               "Give election status?",
               "Give me election status?",
               "Who are all the candidates from this constitutency?"]
    for prompt in prompts:
        input = noisy(prompt, 0.13, True)
        output = handle_spellcheck(input, transpositions=True)
        print("Input: {x}".format(x=input))
        print("Output: {y}\n".format(y=output))
