import pandas as pd
import json
df = pd.read_excel('/Users/jinrubin/Downloads/schoolhub/qu1.xlsx')
qu_info = []
mbti_opt_map = []

title = []
options = []
values = []
for i, r in df.iterrows():
    if not pd.isna(r[0]):
        title.append(r[0][r[0].index('.')+1:])
    if not pd.isna(r[1]):
        options.append(r[1])
    for j in range(2, 10):
        if not pd.isna(r[j]):
            values.append(df.columns[j])
            break

for i in range(len(title)):
    qu_info.append({"type": "单选", "title": title[i], "options": [options[2*i], options[2*i+1]]})
    mbti_opt_map.append([values[2*i], values[2*i+1]])

print(title)
print(options)
print(values)
qu_info = json.dumps(qu_info, ensure_ascii=False)
mbti_opt_map = json.dumps(mbti_opt_map)
print(qu_info)
print(mbti_opt_map)
