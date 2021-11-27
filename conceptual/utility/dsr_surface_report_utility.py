import frappe


@frappe.whitelist()
def enque_update_dsr_surface_report():
    all_dsr = frappe.db.get_all("DSR Surface Report", fields=['machine'])
    for dsr in all_dsr:
        update_dsr_surface_report(dsr.machine)


@frappe.whitelist()
def validate_dsr_surface_report(doc, method):
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
def update_dsr_surface_report(machine):
    doc = frappe.get_doc("DSR Surface Report", {'machine': machine})
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
        doc.drill_rate_with_marching = doc.total_drill_meterage/doc.total_working_hours
        doc.drill_rate_without_marching = doc.total_drill_meterage/doc.total_engine_hours
        doc.percussion_rate = doc.total_drill_meterage/doc.total_percussion_hours
        doc.fuel_consumption_per_hour = doc.total_hsd_consumption/doc.total_engine_hours
        doc.availability = (doc.total_scheduled_hours -
                            doc.total_idle_hours) / (doc.total_scheduled_hours*100)
    except ZeroDivisionError:
        doc.drill_rate_with_marching = 0
        doc.drill_rate_without_marching = 0
        doc.percussion_rate = 0
        doc.fuel_consumption_per_hour = 0
        doc.availability = 0


def set_working_hours(doc):
    shift_working_hours = frappe.db.get_all(
        "DSR Surface", {'machine': doc.name, 'date': ['between', [doc.from_date, doc.to_date]]}, 'total_working_hours')
    if shift_working_hours:
        total_working_hours = 0
        for data in shift_working_hours:
            print(data)
            total_working_hours += data.total_working_hours
        doc.total_working_hours = total_working_hours


def set_total_engine_hours(doc):
    shift_engine_hour = frappe.db.get_all(
        "DSR Surface", {'machine': doc.name, 'date': ['between', [doc.from_date, doc.to_date]]}, 'total_engine_hours')
    if shift_engine_hour:
        total_engine_hours = 0
        for data in shift_engine_hour:
            print(data)
            total_engine_hours += data.total_engine_hours
        doc.total_engine_hours = total_engine_hours


def set_total_percussion_hour(doc):
    shift_percussion_hour = frappe.db.get_all(
        "DSR Surface", {'machine': doc.name, 'date': ['between', [doc.from_date, doc.to_date]]}, 'total_percussion_hours')
    if shift_percussion_hour:
        total_percussion_hours = 0
        for data in shift_percussion_hour:
            total_percussion_hours += data.total_percussion_hours
        doc.total_percussion_hours = total_percussion_hours


def set_total_drill_meterage(doc):
    total_meterage = frappe.db.get_all(
        "DSR Surface", {'machine': doc.name, 'date': ['between', [doc.from_date, doc.to_date]]}, 'total_drill_meterage')
    if total_meterage:
        total_meterage_value = 0
        for data in total_meterage:
            total_meterage_value += data.total_drill_meterage
        doc.total_drill_meterage = total_meterage_value


def set_total_tramming(doc):
    all_tramming = frappe.db.get_all(
        "DSR Surface", {'machine': doc.name, 'date': ['between', [doc.from_date, doc.to_date]]}, 'total_tramming')
    if all_tramming:
        sum_of_tramming = 0
        for data in all_tramming:
            sum_of_tramming += data.total_tramming
        doc.total_trammingmarching = sum_of_tramming/60


def set_total_hsd_consumption(doc):
    total_hsd_consumption = frappe.db.get_all(
        "DSR Surface", {'machine': doc.name, 'date': ['between', [doc.from_date, doc.to_date]]}, 'total_hsd_consumption')
    if total_hsd_consumption:
        total_hsd_consumption_value = 0
        for data in total_hsd_consumption:
            total_hsd_consumption_value += data.total_hsd_consumption
        doc.total_hsd_consumption = total_hsd_consumption_value


def set_total_shift_hours(doc):
    total_shift_hour = frappe.db.get_all(
        "DSR Surface", {'machine': doc.name, 'date': ['between', [doc.from_date, doc.to_date]]}, 'total_scheduled_hours')
    if total_shift_hour:
        total_shift_hours = 0
        for data in total_shift_hour:
            total_shift_hours += data.total_scheduled_hours
        doc.total_scheduled_hours = total_shift_hours


def set_total_idle_time(doc):
    total_idle_time = frappe.db.get_all(
        "DSR Surface", {'machine': doc.name, 'date': ['between', [doc.from_date, doc.to_date]]}, 'total_idle_hours')
    if total_idle_time:
        total_idle_time_hours = 0
        for data in total_idle_time:
            total_idle_time_hours += data.total_idle_hours
        doc.total_idle_hours = total_idle_time_hours/60
