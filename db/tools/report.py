from db.db_session import engine
import pandas as pd


def get_report(filename):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    query_all = '''
    SELECT records.id, name, "group", focus, direction, area, teachers, age_from, age_to, free, code, child_name, child_surname, child_patronymic, child_birthday, educational_institution, edu_class, health, child_phone, child_email, child_residence, parent_name, parent_surname, parent_patronymic, parent_birthday, parent_residence, parent_work, parent_phone, parent_email, full_family, large_family, without_parents, police_record, resident, second_parent_fio, second_parent_phone
    FROM courses INNER JOIN records_courses ON courses.id = records_courses.course_id
    INNER JOIN records ON records.id = records_courses.record_id
    '''

    query_doubles = '''SELECT * FROM "registration 22/23"
    ORDER BY id ASC 
    '''

    query_count_by_groups = '''SELECT course_id, "name", area, courses.age_from, courses.age_to, "group", COUNT(record_id) FROM records_courses
INNER JOIN courses ON course_id = "id"
GROUP BY course_id, "group", courses."name", area, courses.age_from, courses.age_to
ORDER BY course_id ASC
    '''

    df_main = pd.read_sql_query(query_all, con=engine)
    df_triples = pd.read_sql_query(query_doubles, con=engine)
    df_count = pd.read_sql_query(query_count_by_groups, con=engine)

    df_main['teachers'] = df_main['teachers'].apply(lambda lst: ', '.join(lst))
    df_main['code'] = df_main['code'].apply(lambda code: {1: 'КУБ', 2: 'УСПЕХ', 3: 3, -1: 'ЮНОСТЬ'}[code])
    df_main['free'] = df_main['free'].apply(lambda code: {0: 'ПЛАТНО', 1: 'БЮДЖЕТ'}[code])
    df_main.to_excel(writer, 'общая')
    df_main.loc[df_main.duplicated(subset=['child_name', 'child_surname', 'child_patronymic'], keep=False)].to_excel(writer, 'дубликаты')
    df_triples.to_excel(writer, '3+ направлний')
    df_count.to_excel(writer, 'кол-во по группам')

    writer.save()
