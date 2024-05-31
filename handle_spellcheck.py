

def give_suggestion(original: str, list_of_dicts: list) -> str:
    """
    Take in the list of dictionaries given by model
    spell check name, whole sentence
    return suggestion
    """
    # example = [{'span': 'John', 'label': 'PERSON', 'score': 0.9854856729507446, 'char_start_index': 6, 'char_end_index': 10}, 
    #            {'span': '15', 'label': 'DATE', 'score': 0.9371686577796936, 'char_start_index': 22, 'char_end_index': 24}]


    # # ================ SOLUTION 1 ========================
    # # extract name strings, call the spell check on them,
    # # THEN call the spell check on the whole string with the corrected names
    # # problem
    # #   - not sure if the names will interfere when checking rest of sentence

    # # currently incomplete solution
    # names_corrected_prompt = ""
    # index = 0
    # for dict in list_of_dicts:
    #     if dict['label'] == 'PERSON':
    #         names_corrected_prompt += original[index:dict['char_start_index']]
    #         names_corrected_prompt += name_spell_checking(dict['span'])
    #         index = dict['char_end_index'] + 1

    # # ================ SOLUTION 2 ========================
    # # extract name strings, call the spell check on them,
    # # call spell check on the remaining sentence
    # # with placeholder values for the name.


    # # If time, implement multithreading? 


    no_name_prompt = ""
    str_index, num_ppl = 0, 0
    names = []
    for dict in list_of_dicts:
        if dict['label'] == 'PERSON':
            names.append(dict['span'])
            no_name_prompt += original[str_index:dict['char_start_index']] + "Person_{num}".format(num = num_ppl)
            str_index = dict['char_end_index'] + 1
    no_name_prompt += original[str_index:]
    
    # make this concurrent somehow?

    # # spell check name
    # # spell check rest of sentence?

    suggestion = ""
    return suggestion