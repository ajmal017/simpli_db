def get_json_data_structure(data: dict):
    structure = {}
    list_data = {}
    dict_data = {}

    for key, val in data.items():
        val_type = type(val)
        if val_type == list:
            list_data[key] = val
        elif val_type == dict:
            dict_data[key] = val
        else:
            structure[key] = [val_type, len(val)] if val_type == str else val_type

    for key, val in list_data.items():
        list_data[key] = [type(val), len(val)]

    for key, val in dict_data.items():
        dict_data[key] = get_dict_full_structure(val)

    return {**structure, **list_data, **dict_data}


def get_dict_full_structure(data: dict):
    if type(data) != dict:
        return None

    done = False
    layer = [type(data)]
    curr = data

    while not done:
        for _, val in curr.items():
            if type(val) == dict:
                layer.append(type(val))
                curr = val
            else:
                key_type = []
                for k, v in curr.items():
                    v_type = type(v)
                    if v_type == str:
                        key_type.append([k, type(v), len(v)])
                    else:
                        key_type.append([k, type(v)])
                layer.append(key_type)
                done = True
            break
    return layer
                