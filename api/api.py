from flask import blueprints, request, jsonify

from db.db_session import create_db_session
from db.models import Registration, Course, Record, Association

api_bp = blueprints.Blueprint('api', __name__)


@api_bp.route('/reg')
def api_regs():
    db_session = create_db_session()
    ids = sorted([r.id for r in filter(lambda c: len(c.courses) < 3, db_session.query(Registration).all())])
    if not ids:
        return jsonify(
            {'nodata': True}
        )
    reg_id = request.args.get('reg_id')
    if reg_id:
        reg_id = int(reg_id)
        if reg_id not in ids:
            return jsonify(
                {'nodata': True}
            )
        current = db_session.query(Registration).get(reg_id).to_dict()
    else:
        current = next(filter(lambda c: len(c.courses) < 3, db_session.query(Registration).all())).to_dict()
    try:
        if ids.index(current['id']) - 1 < 0:
            raise IndexError
        prev = db_session.query(Registration).get(ids[ids.index(current['id']) - 1]).to_dict()
    except IndexError:
        prev = None
    try:
        next_ = db_session.query(Registration).get(ids[ids.index(current['id']) + 1]).to_dict()
    except IndexError:
        next_ = None
    db_session.close()
    return jsonify({
        'prev': prev,
        'current': current,
        'next': next_
    })


@api_bp.route('/courses')
def api_courses():
    db_session = create_db_session()
    courses = db_session.query(Course).all()
    db_session.close()
    return jsonify([c.to_dict(rules=('-records',)) for c in courses])


@api_bp.route('/update', methods=['POST'])
def api_update():
    reg_id = request.json.get('reg_id')
    records = request.json.get('records')
    if not records:
        return {'status': 'empty data'}

    db_session = create_db_session()
    reg = db_session.query(Registration).get(reg_id)
    rec = Record()
    rec.child_name = reg.child_name
    rec.child_surname = reg.child_surname
    rec.child_patronymic = reg.child_patronymic
    rec.child_birthday = reg.child_birthday
    rec.educational_institution = reg.educational_institution
    rec.edu_class = reg.edu_class
    rec.health = reg.health
    rec.child_phone = reg.child_phone
    rec.child_email = reg.child_email
    rec.child_residence = reg.child_residence
    rec.parent_name = reg.parent_name
    rec.parent_surname = reg.parent_surname
    rec.parent_patronymic = reg.parent_patronymic
    rec.parent_birthday = reg.parent_birthday
    rec.parent_residence = reg.parent_residence
    rec.parent_work = reg.parent_work
    rec.parent_phone = reg.parent_phone
    rec.parent_email = reg.parent_email
    rec.full_family = reg.full_family
    rec.large_family = reg.large_family
    rec.without_parents = reg.without_parents
    rec.police_record = reg.police_record
    rec.resident = reg.resident
    rec.second_parent_fio = reg.second_parent_fio
    rec.second_parent_phone = reg.second_parent_phone
    db_session.add(rec)
    for c, g in records:
        assoc = Association()
        assoc.group = g
        course = db_session.query(Course).get(c)
        assoc.course = course
        assoc.record = rec
        db_session.add(assoc)
    db_session.delete(reg)
    db_session.commit()
    db_session.close()
    return {'status': 'ok'}
