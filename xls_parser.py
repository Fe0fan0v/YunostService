import datetime

from openpyxl import load_workbook
from db.db_session import global_init, create_session
from db.models import Course

FILENAME = 'courses.xlsx'

keys = ['name', 'age', 'direction', 'description', 'teachers', 'area', 'free',
        *(str(i) for i in range(1, 11))]


def clear(s):
    if s is None:
        return
    return ' '.join(s.split())


global_init()
db_session = create_session()
wb = load_workbook(FILENAME)
ws = wb.active
for row in filter(lambda r: r[0].value, ws.iter_rows(min_row=5)):
    if len(list(filter(lambda c: c.value, row))) <= 1:
        continue
    data = dict(zip(keys, (cell.value for cell in row[:6])))
    if not all(data.values()):
        continue
    if isinstance(data['age'], datetime.datetime):
        data['age'] = f"{data['age'].day}-{data['age'].month}"
    data['teachers'] = data['teachers'].split(',')
    data['direction'] = data['direction'].upper()
    course = Course(**data)
    course.free = row[6].value is None or row[6].value.strip().lower() == 'бюджет'
    schedule = dict(filter(lambda pair: pair[1], zip(keys[7:], (clear(cell.value) for cell in row[7:]))))
    if not any(schedule.values()):
        continue
    course.schedule = schedule
    course.cube = row[0].fill.bgColor.rgb == 'FF00FFFF'
    db_session.add(course)
db_session.commit()
