import frappe
from datetime import datetime, date


@frappe.whitelist()
def calculate_time_diff(from_time, to_time):
    time_1 = datetime.strptime(
        str(from_time), "%H:%M:%S").time() if from_time else '00:00:00'
    time_2 = datetime.strptime(
        str(to_time), "%H:%M:%S").time() if to_time else '00:00:00'

    time_diff = datetime.combine(
        date.today(), time_2) - datetime.combine(date.today(), time_1)

    time_diff_in_mins = time_diff.total_seconds() / 60
    return time_diff_in_mins
