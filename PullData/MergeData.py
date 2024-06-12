import pandas as pd

# 定义一个函数来加载 excel 文件中的工作表(sheet)
def load_sheet(file, sheet_idx):
    return pd.read_excel(file, sheet_name=sheet_idx, engine='openpyxl')

# 文件名
excel_file = "/Users/songzonglin/Downloads/FA/数据/1800813521977946113-AI+Sourcing%E8%BF%90%E8%A1%8C%E6%95%B0%E6%8D%AE%E6%83%85%E5%86%B5.xlsx"

 # 加载你的 excel 文件中的工作表(sheet)
df1 = load_sheet(excel_file, 0)  # 第一个工作表(sheet)
df2 = load_sheet(excel_file, 1)  # 第二个工作表(sheet)

# 按照职位名称列合并两个数据框
merged_df = pd.merge(df1, df2, on='职位名称', suffixes=('_df1', '_df2'))

# 计算数量相关列的和
col_to_sum = ['AI总计查看人数', 'AI主动打招呼数', 'AI总计获取简历数', '时长']

for col in col_to_sum:
    merged_df[col] = merged_df[col + '_df1'] + merged_df[col + '_df2']

# 删除合并后不再需要的列
merged_df.drop(columns=[col + suffix for col in col_to_sum for suffix in ['_df1', '_df2']], inplace=True)

# 打印列 "时长"，"AI总计查看人数"，"AI主动打招呼数"和"AI总计获取简历数"
merged_df.fillna(0, inplace=True)

# 打印列 "职位名称"，"时长"，"AI总计查看人数"，"AI主动打招呼数"和"AI总计获取简历数"
merged_df = merged_df[['职位名称', '时长', 'AI总计查看人数', 'AI主动打招呼数', 'AI总计获取简历数']]
print(merged_df.to_markdown())