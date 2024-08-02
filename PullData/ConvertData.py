import pandas as pd

# 使用你的实际Excel文件路径
file_path = "/Users/songzonglin/Downloads/FA/GS/7.5-7.9无效原因.xlsx"

# 读取 Excel 文件
data = pd.read_excel(file_path)

# 对比第2列和第15列，以及第3列和第16列fo

# 将第17列、第18列、第19列的数据放到第20列、第21列、第22列
data.loc[matched_rows.index, "T"] = matched_rows.iloc[:, 16]
data.loc[matched_rows.index, "U"] = matched_rows.iloc[:, 17]
data.loc[matched_rows.index, "V"] = matched_rows.iloc[:, 18]

# 保存结果到原 Excel 文件
data.to_excel(file_path, index=False)