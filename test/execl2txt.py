import pandas as pd

# 读取Excel文件
df = pd.read_excel('example.xlsx')

# 将数据输出到文本文件中
with open('output.txt', 'w') as f:
    for index, row in df.iterrows():
        # 将单元格之间用#分割，并添加换行符
        line = '??'.join([str(cell) for cell in row]) + '\n'
        f.write(line)