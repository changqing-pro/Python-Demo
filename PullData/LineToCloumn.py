import pandas as pd

import pandas as pd


# 或者从Excel文件中读取数据
df = pd.read_excel('/Users/songzonglin/Downloads/FA/数据/0520 NIKE数据.xlsx')

# 将'time'字段的数据类型转为datetime
df['time'] = pd.to_datetime(df['time'])


# 将数据“融合”成一个类似于以“查看、招呼、简历”为行、日期为列的新表格
df_melted = pd.melt(df, id_vars="time", value_vars=["robot_num","look_num", "say_hi_num", "resume_num"])

# 将数据透视为我们需要的格式
df_pivot = df_melted.pivot(index="variable", columns="time", values="value")

# 更改行标签

# 输出结果
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

row_labels = {"robot_num":"机器数量","look_num": "查看", "say_hi_num": "招呼", "resume_num": "简历"}
df_pivot.rename(index=row_labels, inplace=True)
ordered_labels = ["机器数量","查看", "招呼", "简历"]
df_pivot = df_pivot.reindex(ordered_labels)

df_pivot = df_pivot.fillna(0)



# 打印 DataFrame
df_pivot.to_excel("/Users/songzonglin/Downloads/FA/数据/output.xlsx")
