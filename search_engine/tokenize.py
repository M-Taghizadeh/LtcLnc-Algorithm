def tokenizer(input_str:str):
    input_str.strip()
    split_list = input_str.split(" ")
    
    tokens_list = []
    for token in split_list:
        if len(list(token)) > 1:
            tokens_list.append(token)

    return tokens_list