

def merge_list_of_dicts_on_key_assume_sorted_inplace(dict_list_1, dict_list_2, key="BID_ID"):
    assert len(dict_list_1) == len(dict_list_2), "lists should be equal length"
    for i in range(len(dict_list_1)):
        merge_dicts_on_key_inplace(dict_list_1[i], dict_list_2[i], key)


def merge_dicts_on_key_inplace(dict1, dict2, key):
    assert dict1[key] == dict2[key], "Dicts should have a common key-value pair"
    dict1.update(dict2)
