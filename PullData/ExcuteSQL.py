import pymysql.cursors
import json
from datetime import datetime
import pandas as pd

def try_parse_date(date_str):
    for fmt in ('%Y-%m', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f'No valid date format found for {date_str}')

# 连接到数据库
connection = pymysql.connect(host='rm-uf63lt4bf5e988476.mysql.rds.aliyuncs.com',
                             user='stapp',
                             password='',
                             database='sourcetracing',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # 执行sql查询
        sql = """
        select max(t2.work_list) work_list, max(t2.education_list) education_list,t2.platform_id,t4.boss_account,
t1.position_name,t3.phone,t2.out_user_id, t2.position_id,t2.clue_name, t2.birth,t3.create_time,t3.resume_id
FROM
	st_position t1
	INNER JOIN st_platform_clue_pool t2 ON t1.id = t2.position_id
	INNER JOIN st_platform_clue_result t3 ON t3.out_user_id = t2.out_user_id and t3.position_id = t2.position_id
	INNER JOIN t_rpa_account_config t4 ON t4.rpa_account = t1.rpa_account
WHERE t4.cust_code = 'Z000001'
   and t3.resume_id > 0
	AND t2.create_time > '2024-07-01  00:00:00'
	AND t2.create_time < '2024-07-15  00:00:00'
	group by t2.out_user_id, t2.position_id,t1.position_name,t3.phone"""
        cursor.execute(sql)

        formattedResults = []
        # 获取所有返回结果
        result = cursor.fetchall()
        for row in result:
            # if any(d.get('简历ID') == row['resume_id'] for d in formattedResults):
            #     continue
            work_list = ''
            if row['work_list']:
                work_list = json.loads(row['work_list'])
            education_list = ''
            if row['education_list']:
                education_list = json.loads(row['education_list'])
            corporationName = ''
            total_years =''
            if work_list:
                latest_work = max(
                    work_list,
                    key=lambda work: try_parse_date(work['endTime'])
                )
                corporationName = latest_work['corporationName']
                total_years = sum(float(work['workYearDesc'].replace('年','')) for work in work_list)
            edu_endTime =''
            schoolName = ''
            disciplineName = ''
            if education_list:
                latest_edu = max(
                    education_list,
                    key= lambda edu : try_parse_date(edu.get('endTime', '2024-07-15'))
                )
                edu_endTime = latest_edu.get('endTime', '2024-07-15')
                schoolName = latest_edu['schoolName']
                disciplineName = latest_edu['disciplineName']
            birthday = datetime.strptime(row['birth'], '%Y-%m')
            # 获取当前日期
            now = datetime.now()
            # 计算年龄
            age = now.year - birthday.year
            if now.month < birthday.month or (now.month == birthday.month and now.day < birthday.day):
                age -= 1
            platform = 'Boss'
            if row['platform_id'] == 2:
                platform = '智联'
            if row['platform_id'] == 3:
                platform = '猎聘'
            parsed_result = {'姓名': row['clue_name'],
                             '年龄': age,
                             '手机号': row['phone'],
                             '职位': row['position_name'],
                             '公司名称': corporationName,
                             '毕业时间': edu_endTime,
                             '学校': schoolName,
                             '专业': disciplineName,
                             '年限': total_years,
                             '简历ID': row['resume_id'],
                             '入库时间': row['create_time'],
                             '平台': platform,
                             '顾问': row['boss_account']
                            }
            formattedResults.append(parsed_result)
finally:
    connection.close()


df = pd.DataFrame(formattedResults)
df.to_excel('D:\\test\\output.xlsx', index=False)