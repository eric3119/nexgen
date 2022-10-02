from tokenize import generate_tokens
import pandas as pd
import io

string_code = '''def delete(self, session_key=None):
    if session_key is None:
        if self.session_key is None:
            return
        session_key = self.session_key
        os.unlink(self._key_to_file(session_key))'''

lines = []
line = ''
curr_line = None
readline = io.StringIO(string_code).readline

for token in generate_tokens(readline):
    if curr_line is None: curr_line = token.line
    if token.line == curr_line:
        line += ' ' + token.string
    else:
        lines.append(line)
        line = ''
        curr_line = token.line

df = pd.DataFrame([{'hasCatch': 1, 'id': 0, 'labels': [0,0,0,0,0,1], 'lines': lines}])
df.to_pickle('task1/data/train.pkl')
df.to_pickle('task1/data/test.pkl')
df.to_pickle('task1/data/valid.pkl')