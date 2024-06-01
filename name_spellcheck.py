from nltk.metrics import edit_distance
import pandas as pd


# try edlib library; supposed to be super fast. should implement and compare to this.
def edit_dist_suggestion(original_name: str, include_transpositions=False) -> str:
    """
    take in all candidate names, compare edit_distance with
    given name, return closest one.
    """

    df = pd.read_excel("other_py_files/ELECTION_2024.xlsx")
    candidate_names = df["CANDINAME"]
    if original_name in candidate_names:
        return original_name

    smallest_dist = len(original_name)
    closest_names = []
    for candidate in candidate_names:
        distance = edit_distance(
            original_name, candidate, transpositions=include_transpositions)
        if distance < smallest_dist:
            smallest_dist = distance
            closest_names = [candidate]
        elif distance == smallest_dist:
            closest_names.append(candidate)

    n = len(closest_names)
    if n == 1:
        return closest_names[0]

    # sort alphabetically and pick closest one
    n += 1
    closest_names.append(original_name)
    closest_names.sort()
    index = closest_names.index(original_name)
    if index == n - 1:
        return closest_names[index - 1]
    return closest_names[index + 1]
