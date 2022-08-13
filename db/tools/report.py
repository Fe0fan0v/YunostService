import datetime

from db.db_session import engine
import pandas as pd


def get_report(filename):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    query_all = '''
    SELECT records.id, name, focus, direction, area, teachers, age_from, age_to, free, code, child_name, child_surname, child_patronymic, child_birthday, educational_institution, edu_class, health, child_phone, child_email, child_residence, parent_name, parent_surname, parent_patronymic, parent_birthday, parent_residence, parent_work, parent_phone, parent_email, full_family, large_family, without_parents, police_record, resident, second_parent_fio, second_parent_phone
    FROM courses INNER JOIN records_courses ON courses.id = records_courses.course_id
    INNER JOIN records ON records.id = records_courses.record_id
    '''

    query_doubles = '''SELECT * FROM "registration 22/23"
    ORDER BY id ASC 
    '''


    df_main = pd.read_sql_query(query_all, con=engine)
    df_double = pd.read_sql_query(query_doubles, con=engine)

    df_main['teachers'] = df_main['teachers'].apply(lambda lst: ', '.join(lst))
    df_main['code'] = df_main['code'].apply(lambda code: {1: 'КУБ', 2: 'УСПЕХ', 3: 3, -1: 'ЮНОСТЬ'}[code])
    df_main['free'] = df_main['free'].apply(lambda code: {0: 'ПЛАТНО', 1: 'БЮДЖЕТ'}[code])
    df_main.to_excel(writer, 'общая')
    df_main.groupby(['focus', 'code'])['id'].count().to_excel(writer, 'по направленности')
    df_main.groupby(['direction', 'code'])['id'].count().to_excel(writer, 'по направлению')
    df_main.groupby('name')['id'].count().to_excel(writer, 'по программе')
    df_main.groupby('area')['id'].count().to_excel(writer, 'по площадке')
    df_main.groupby('code')['id'].count().to_excel(writer, 'по шифру')
    df_main.groupby('teachers')['id'].count().to_excel(writer, 'по педагогу')
    df_main.groupby('free')['id'].count().to_excel(writer, 'по бюджету')
    df_main.groupby('health')['id'].count().to_excel(writer, 'по здоровью')
    df_main.groupby(['age_from', 'age_to'])['id'].count().to_excel(writer, 'по возрасту')
    now = datetime.datetime.now()
    df_main['age'] = df_main['child_birthday'].apply(lambda dt: (now.date() - dt).days // 365)
    df_main.groupby('age')['child_birthday'].count().to_excel(writer, 'по возрасту2')
    df_double.to_excel(writer, 'дубликаты')

    writer.save()
