import frappe


@frappe.whitelist()
def validate_dsr(doc, method):
    set_working_hours(doc)
    set_total_engine_hours(doc)
    set_total_percussion_hour(doc)
    set_total_drill_meterage(doc)
    set_total_tramming(doc)
    set_total_hsd_consumption(doc)
    set_total_shift_hours(doc)
    set_total_idle_time(doc)


@frappe.whitelist()
def update_dsr(dsr):
    doc = frappe.get_doc("DSR Surface", dsr)
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
    doc.drill_rate_with_marching = doc.total_drill_meterage/doc.total_working_hours
    doc.drill_rate_without_marching = doc.total_drill_meterage/doc.total_engine_hours
    doc.percussion_rate = doc.total_drill_meterage/doc.total_percussion_hours
    doc.fuel_consumption_per_hour = doc.total_hsd_consumption/doc.total_engine_hours
    doc.availability = (doc.total_scheduled_hours -
                        doc.total_idle_hours) / (doc.total_scheduled_hours*100)


def set_working_hours(doc):
    shift_working_hours = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'working_hours')
    if shift_working_hours:
        total_working_hours = 0
        for data in shift_working_hours:
            print(data)
            total_working_hours += data.working_hours
        doc.total_working_hours = total_working_hours


def set_total_engine_hours(doc):
    shift_engine_hour = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'total_engine_hour')
    if shift_engine_hour:
        total_engine_hours = 0
        for data in shift_engine_hour:
            print(data)
            total_engine_hours += data.total_engine_hour
        doc.total_engine_hours = total_engine_hours


def set_total_percussion_hour(doc):
    shift_percussion_hour = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'total_percussion_hour')
    if shift_percussion_hour:
        total_percussion_hours = 0
        for data in shift_percussion_hour:
            total_percussion_hours += data.total_percussion_hour
        doc.total_percussion_hours = total_percussion_hours


def set_total_drill_meterage(doc):
    total_meterage = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'total_meterage')
    if total_meterage:
        total_meterage_value = 0
        for data in total_meterage:
            total_meterage_value += data.total_meterage
        doc.total_drill_meterage = total_meterage_value


def set_total_tramming(doc):
    all_tramming = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'tramming')
    if all_tramming:
        sum_of_tramming = 0
        for data in all_tramming:
            sum_of_tramming += data.tramming
        doc.total_tramming = sum_of_tramming/60


def set_total_hsd_consumption(doc):
    total_hsd_consumption = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'hsd_consumption')
    if total_hsd_consumption:
        total_hsd_consumption_value = 0
        for data in total_hsd_consumption:
            total_hsd_consumption_value += data.hsd_consumption
        doc.total_hsd_consumption = total_hsd_consumption_value


def set_total_shift_hours(doc):
    total_shift_hour = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'shift_hours')
    if total_shift_hour:
        total_shift_hours = 0
        for data in total_shift_hour:
            total_shift_hours += data.shift_hours
        doc.total_scheduled_hours = total_shift_hours


def set_total_idle_time(doc):
    total_idle_time = frappe.db.get_all(
        "Shift Report", {'dsr_surface': doc.name}, 'idle_time')
    if total_idle_time:
        total_idle_time_mins = 0
        for data in total_idle_time:
            total_idle_time_mins += data.idle_time
        doc.total_idle_hours = total_idle_time_mins/60
