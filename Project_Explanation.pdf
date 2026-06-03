"""
models/timetable.py — All timetable-related DB models
Subjects, Teachers, Classrooms, TimeSlots, Timetable, ActivityLog
"""

import sqlite3
from datetime import datetime


def get_db():
    from app import DATABASE
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ── Subjects ──────────────────────────────────

def get_all_subjects():
    db = get_db()
    rows = db.execute('SELECT * FROM subjects ORDER BY subject_name').fetchall()
    db.close()
    return [dict(r) for r in rows]

def add_subject(name, credits, hours_per_week):
    db = get_db()
    db.execute('INSERT INTO subjects (subject_name, credits, hours_per_week) VALUES (?,?,?)',
               (name, credits, hours_per_week))
    db.commit()
    db.close()

def delete_subject(sid):
    db = get_db()
    db.execute('DELETE FROM subjects WHERE id=?', (sid,))
    db.commit()
    db.close()

def update_subject(sid, name, credits, hours):
    db = get_db()
    db.execute('UPDATE subjects SET subject_name=?, credits=?, hours_per_week=? WHERE id=?',
               (name, credits, hours, sid))
    db.commit()
    db.close()


# ── Teachers ──────────────────────────────────

def get_all_teachers():
    db = get_db()
    rows = db.execute('SELECT * FROM teachers ORDER BY teacher_name').fetchall()
    db.close()
    return [dict(r) for r in rows]

def add_teacher(name, specialization):
    db = get_db()
    db.execute('INSERT INTO teachers (teacher_name, specialization) VALUES (?,?)',
               (name, specialization))
    db.commit()
    db.close()

def delete_teacher(tid):
    db = get_db()
    db.execute('DELETE FROM teachers WHERE id=?', (tid,))
    db.commit()
    db.close()

def update_teacher(tid, name, spec):
    db = get_db()
    db.execute('UPDATE teachers SET teacher_name=?, specialization=? WHERE id=?',
               (name, spec, tid))
    db.commit()
    db.close()


# ── Classrooms ────────────────────────────────

def get_all_classrooms():
    db = get_db()
    rows = db.execute('SELECT * FROM classrooms ORDER BY room_number').fetchall()
    db.close()
    return [dict(r) for r in rows]

def add_classroom(room_number, capacity):
    db = get_db()
    db.execute('INSERT INTO classrooms (room_number, capacity) VALUES (?,?)',
               (room_number, capacity))
    db.commit()
    db.close()

def delete_classroom(cid):
    db = get_db()
    db.execute('DELETE FROM classrooms WHERE id=?', (cid,))
    db.commit()
    db.close()

def update_classroom(cid, room_number, capacity):
    db = get_db()
    db.execute('UPDATE classrooms SET room_number=?, capacity=? WHERE id=?',
               (room_number, capacity, cid))
    db.commit()
    db.close()


# ── Time Slots ────────────────────────────────

def get_all_timeslots():
    db = get_db()
    rows = db.execute('SELECT * FROM timeslots ORDER BY day, start_time').fetchall()
    db.close()
    return [dict(r) for r in rows]

def add_timeslot(day, start_time, end_time):
    db = get_db()
    db.execute('INSERT INTO timeslots (day, start_time, end_time) VALUES (?,?,?)',
               (day, start_time, end_time))
    db.commit()
    db.close()

def delete_timeslot(tid):
    db = get_db()
    db.execute('DELETE FROM timeslots WHERE id=?', (tid,))
    db.commit()
    db.close()


# ── Timetable ─────────────────────────────────

def get_full_timetable():
    db = get_db()
    rows = db.execute('''
        SELECT tt.id,
               s.subject_name, s.credits,
               t.teacher_name, t.specialization,
               c.room_number, c.capacity,
               ts.day, ts.start_time, ts.end_time,
               tt.subject_id, tt.teacher_id, tt.classroom_id, tt.timeslot_id
        FROM timetable tt
        JOIN subjects s ON tt.subject_id = s.id
        JOIN teachers t ON tt.teacher_id = t.id
        JOIN classrooms c ON tt.classroom_id = c.id
        JOIN timeslots ts ON tt.timeslot_id = ts.id
        ORDER BY ts.day, ts.start_time
    ''').fetchall()
    db.close()
    return [dict(r) for r in rows]

def clear_timetable():
    db = get_db()
    db.execute('DELETE FROM timetable')
    db.commit()
    db.close()

def insert_timetable_entry(subject_id, teacher_id, classroom_id, timeslot_id):
    db = get_db()
    db.execute(
        'INSERT INTO timetable (subject_id, teacher_id, classroom_id, timeslot_id) VALUES (?,?,?,?)',
        (subject_id, teacher_id, classroom_id, timeslot_id)
    )
    db.commit()
    db.close()

def delete_timetable_entry(entry_id):
    db = get_db()
    db.execute('DELETE FROM timetable WHERE id=?', (entry_id,))
    db.commit()
    db.close()

def detect_conflicts():
    """Detect all hard constraint violations in current timetable."""
    entries = get_full_timetable()
    conflicts = []
    for i, e1 in enumerate(entries):
        for e2 in entries[i+1:]:
            if e1['day'] == e2['day'] and e1['start_time'] == e2['start_time']:
                if e1['teacher_id'] == e2['teacher_id']:
                    conflicts.append({
                        'type': 'Teacher Clash',
                        'detail': f"{e1['teacher_name']} is double-booked on {e1['day']} at {e1['start_time']}",
                        'entries': [e1['id'], e2['id']]
                    })
                if e1['classroom_id'] == e2['classroom_id']:
                    conflicts.append({
                        'type': 'Room Clash',
                        'detail': f"Room {e1['room_number']} double-booked on {e1['day']} at {e1['start_time']}",
                        'entries': [e1['id'], e2['id']]
                    })
    return conflicts


# ── Activity Log ──────────────────────────────

def log_activity(user_id, action, detail=''):
    db = get_db()
    db.execute(
        'INSERT INTO activity_log (user_id, action, detail, timestamp) VALUES (?,?,?,?)',
        (user_id, action, detail, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    db.commit()
    db.close()

def get_recent_activities(limit=20):
    db = get_db()
    rows = db.execute('''
        SELECT al.*, u.fullname, u.role
        FROM activity_log al
        JOIN users u ON al.user_id = u.id
        ORDER BY al.timestamp DESC
        LIMIT ?
    ''', (limit,)).fetchall()
    db.close()
    return [dict(r) for r in rows]


# ── Analytics ─────────────────────────────────

def get_dashboard_stats():
    db = get_db()
    stats = {
        'total_subjects': db.execute('SELECT COUNT(*) FROM subjects').fetchone()[0],
        'total_teachers': db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
        'total_classrooms': db.execute('SELECT COUNT(*) FROM classrooms').fetchone()[0],
        'total_timetable_entries': db.execute('SELECT COUNT(*) FROM timetable').fetchone()[0],
        'total_timeslots': db.execute('SELECT COUNT(*) FROM timeslots').fetchone()[0],
    }
    db.close()
    return stats

def get_teacher_workload():
    db = get_db()
    rows = db.execute('''
        SELECT t.teacher_name, COUNT(tt.id) as classes
        FROM teachers t
        LEFT JOIN timetable tt ON t.id = tt.teacher_id
        GROUP BY t.id
        ORDER BY classes DESC
    ''').fetchall()
    db.close()
    return [dict(r) for r in rows]

def get_classroom_utilization():
    db = get_db()
    total_slots = db.execute('SELECT COUNT(*) FROM timeslots').fetchone()[0]
    rows = db.execute('''
        SELECT c.room_number, COUNT(tt.id) as used
        FROM classrooms c
        LEFT JOIN timetable tt ON c.id = tt.classroom_id
        GROUP BY c.id
        ORDER BY used DESC
    ''').fetchall()
    db.close()
    result = []
    for r in rows:
        pct = round((r['used'] / total_slots * 100), 1) if total_slots > 0 else 0
        result.append({'room_number': r['room_number'], 'used': r['used'], 'utilization': pct})
    return result

def get_weekly_distribution():
    db = get_db()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    result = []
    for day in days:
        count = db.execute('''
            SELECT COUNT(*) FROM timetable tt
            JOIN timeslots ts ON tt.timeslot_id = ts.id
            WHERE ts.day=?
        ''', (day,)).fetchone()[0]
        result.append({'day': day, 'count': count})
    db.close()
    return result
