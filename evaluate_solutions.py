# import pandas as pd
from transformers import pipeline
from nltk.metrics import edit_distance
from handler_helper import ask_spellcheck_pipeline
from nltk_correct_txt import did_you_mean


if __name__ == "__main__":
    eng_spell_pipeline = pipeline(
        "text2text-generation", model="oliverguhr/spelling-correction-english-base")

    file_name = "typo_dataset.txt"
    # print(df)
    results = {"pipeline": 0, "nltk_correction": 0}
    n = 100
    i = -1
    with open(file_name, "r") as file:
        for row in file:
            i += 1
            if not i:
                continue
            elif i == n:
                break

            split_values = row.split(",")
            if len(split_values) != 2:
                continue

            improvement, typo = split_values
            # print(improvement)
            pipeline_suggestion = ask_spellcheck_pipeline(
                eng_spell_pipeline, typo)
            pipeline_dist = edit_distance(improvement, pipeline_suggestion)

            nltk_suggestion = did_you_mean(typo)
            nltk_dist = edit_distance(improvement, nltk_suggestion)

            print(pipeline_suggestion)
            print(nltk_suggestion)

            if pipeline_dist == nltk_dist:
                # print("equal")
                continue
            elif pipeline_dist < nltk_dist:
                results["pipeline"] += 1
            else:
                results["nltk_correction"] += 1

    print(results)
