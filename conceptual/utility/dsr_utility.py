import frappe


def validate_dsr(doc):
    set_working_hours(doc)
    set_total_engine_hours(doc)


def set_working_hours(doc, method):
    shift_working_hours = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'working_hours')
    total_working_hours = 0
    for data in shift_working_hours:
        total_working_hours += data.working_hours
    doc.total_working_hours = total_working_hours


def set_total_engine_hours(doc, method):
    total_engine_hour = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'total_engine_hour')
    total_engine_hours = 0
    for data in total_engine_hour:
        total_engine_hours += data.total_engine_hour
    doc.total_engine_hours = total_engine_hours
