import token as pytoken
import tokenize

import pandas as pd
from numpy.random import default_rng

rng = default_rng()

functions_list = []
python_file = 'task1/data/teste.py'

with open(python_file) as f:
    lines = []
    labels = []
    indent_count = 0
    indent_start_function_def = None
    indent_start_try_block = None

    current_line = None
    ignore_line = False
    token_buffer = []

    def clear_line_buffer(token_info: tokenize.TokenInfo):
        global ignore_line, current_line, token_buffer, indent_start_try_block, indent_count, lines, labels
        if len(token_buffer) != 0:
            lines.append(' '.join(token_buffer))
            labels.append(
                1 if indent_start_try_block is not None 
                and indent_start_try_block < indent_count else 0)
        token_buffer = []
        current_line = token_info.line
        ignore_line = False

    def end_of_function_def():
        global indent_start_function_def, functions_list, lines, labels
        
        indent_start_function_def = None
        functions_list.append({
            'id': len(functions_list),
            'hasCatch': 1 if sum(labels) != 0 else 0,
            'lines': lines,
            'labels': labels
        })
        lines = []
        labels = []

    for token_info in tokenize.generate_tokens(f.readline):

        if token_info.line != current_line:
            clear_line_buffer(token_info)

        if(token_info.type == pytoken.NAME and token_info.string == 'def'):
            indent_start_function_def = indent_count
        if indent_start_function_def is None: continue

        if(token_info.type == pytoken.COMMENT): continue
        if(token_info.type == pytoken.NEWLINE): continue
        if(token_info.type == pytoken.NL): continue

        if(token_info.type == pytoken.INDENT):
            indent_count += 1
            if indent_start_try_block is None:
                token_buffer.append(pytoken.tok_name[token_info.type])
            continue
        if(token_info.type == pytoken.DEDENT):
            indent_count -= 1
            assert indent_count >= 0, print('tokenize fail')
            token_buffer.append(pytoken.tok_name[token_info.type])
            if indent_start_try_block == indent_count:
                indent_start_try_block = None
                clear_line_buffer(token_info)
                end_of_function_def() # ignore except
            if indent_start_function_def == indent_count:
                clear_line_buffer(token_info)
                end_of_function_def()
            continue

        if(token_info.type == pytoken.ENDMARKER):
            end_of_function_def()
            continue
       
        if(token_info.type == pytoken.NAME and token_info.string == 'try'):
            ignore_line = True
            indent_start_try_block = indent_count

        if indent_start_function_def is not None and not ignore_line:
            token_buffer.append(token_info.string)

# debug print
# for fs in functions_list: 
#     for fdef in (zip(fs['labels'], fs['lines'])):
#         print(fdef)
#     print()

# split dataset
index_rnd = rng.choice(len(functions_list), size=len(functions_list), replace=False)
a, b, c = int((len(index_rnd)/4) * 1), int((len(index_rnd)/4) * 2), int((len(index_rnd)/4) * 3)

pd.DataFrame(
        [functions_list[i] for i in index_rnd[:a]]
    ).to_pickle('task1/data/train.pkl')
pd.DataFrame(
        [functions_list[i] for i in index_rnd[a:b]]
    ).to_pickle('task1/data/test.pkl')
pd.DataFrame(
        [functions_list[i] for i in index_rnd[b:]]
    ).to_pickle('task1/data/valid.pkl')

