from handle_spellcheck import handle_spellcheck
import add_noise
import string
import re


if __name__ == "__main__":

    # for char in string.punctuation:
    #     input = "I went to the park with my friend Kushagra" + char + " Vagisha joined us later" + char
    #     prompt = punctuation_spacing(input)
    name = "J. V. Ramana"
    input = add_noise.noisy(" How many votes did ", 0.15) + \
        add_noise.noisy(name, 0) + add_noise.noisy(",. have? ", 0.15)
    # print("Input: {x}".format(x=input))
    output = handle_spellcheck(input, transpositions=True)
    print("Input: {x}".format(x=input))
    print("Output: {y}\n".format(y=output))
