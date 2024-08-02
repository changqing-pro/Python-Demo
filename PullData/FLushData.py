import pandas as pd

# 读取excel表格
df = pd.read_excel('/Users/songzonglin/Downloads/欧莱雅不合适候选人分析.xlsx')

# 对 suitable_reason 列中的每个元素转换为字符串
df['suitable_reason'] = df['suitable_reason'].astype(str)


for index, row in df.iterrows():
    df.loc[index, 'type'] = '列表' if row["type"] == 1 else '详情'
    if row['suitable_reason'] != 'nan':
        if ":" in row['suitable_reason']:
            df.loc[index, 'suitable_reason'] = row['suitable_reason'].split(":")[1]

result = df.groupby(['position_name', 'type', 'suitable_reason'])['num'].sum().reset_index()

df['type'] = df['type'].map({1: '列表', 0: '详情'})

# 新的Excel文件路径
new_file_path = '/Users/songzonglin/Downloads/欧莱雅不合适候选人分析_new.xlsx'

# 将result数据写入该Excel文件，即创建Excel文件的“新的sheet名”表单
with pd.ExcelWriter(new_file_path, engine='openpyxl') as writer:
    result.to_excel(writer, index=False, sheet_name='新的sheet名')