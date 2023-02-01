import frappe


@frappe.whitelist()
def enque_update_machine():
    all_machine = frappe.db.get_all("Machine")
    for machine in all_machine:
        update_machine(machine.name)


@frappe.whitelist()
def validate_machine(doc, method):
    if not doc.is_new():
        set_working_hours(doc)
        set_total_engine_hours(doc)
        set_total_percussion_hour(doc)
        set_total_drill_meterage(doc)
        set_total_tramming(doc)
        set_total_hsd_consumption(doc)
        set_total_shift_hours(doc)
        set_total_idle_time(doc)
        set_totals(doc)


@frappe.whitelist()
def update_machine(machine):
    doc = frappe.get_doc("Machine", machine)
    set_working_hours(doc)
    set_total_engine_hours(doc)
    set_total_percussion_hour(doc)
    set_total_drill_meterage(doc)
    set_total_tramming(doc)
    set_total_hsd_consumption(doc)
    set_total_shift_hours(doc)
    set_total_idle_time(doc)
    set_totals(doc)
    doc.save()


def set_totals(doc):
    try:
        doc.drill_rate_with_marching = doc.total_drill_meterage / \
            doc.working_hours if (
                doc.total_drill_meterage and doc.working_hours) else 0
        doc.drill_rate_without_marching = doc.total_drill_meterage / \
            doc.total_engine_hour if (
                doc.total_drill_meterage and doc.total_engine_hour) else 0
        doc.percussion_rate = doc.total_drill_meterage / \
            doc.total_percussion_hours if (
                doc.total_drill_meterage and doc.total_percussion_hours) else 0
        doc.fuel_consumption_per_hour = doc.total_hsd_consumption / \
            doc.total_engine_hour if (
                doc.total_hsd_consumption and doc.total_engine_hour) else 0
        if doc.total_scheduled_hours and doc.total_idle_hours:
            doc.availability = (doc.total_scheduled_hours -
                                doc.total_idle_hours) / doc.total_scheduled_hours*100
    except ZeroDivisionError:
        doc.drill_rate_with_marching = 0
        doc.drill_rate_without_marching = 0
        doc.percussion_rate = 0
        doc.fuel_consumption_per_hour = 0
        doc.availability = 0


def set_working_hours(doc):
    shift_working_hours = frappe.db.get_all(
        "Shift Report", {'machine': doc.name}, 'working_hours')
    if shift_working_hours:
        working_hours = 0
        for data in shift_working_hours:
            print(data)
            working_hours += data.working_hours
        doc.working_hours = working_hours


def set_total_engine_hours(doc):
    shift_engine_hour = frappe.db.get_all(
        "Shift Report", {'machine': doc.name}, 'total_engine_hour')
    if shift_engine_hour:
        total_engine_hour = 0
        for data in shift_engine_hour:
            print(data)
            total_engine_hour += data.total_engine_hour
        doc.total_engine_hour = total_engine_hour


def set_total_percussion_hour(doc):
    shift_percussion_hour = frappe.db.get_all(
        "Shift Report", {'machine': doc.name}, 'total_percussion_hours')
    if shift_percussion_hour:
        total_percussion_hours = 0
        for data in shift_percussion_hour:
            total_percussion_hours += data.total_percussion_hours
        doc.total_percussion_hours = total_percussion_hours


def set_total_drill_meterage(doc):
    total_meterage = frappe.db.get_all(
        "Shift Report", {'machine': doc.name}, 'total_drill_meterage')
    if total_meterage:
        total_meterage_value = 0
        for data in total_meterage:
            total_meterage_value += data.total_drill_meterage
        doc.total_drill_meterage = total_meterage_value
