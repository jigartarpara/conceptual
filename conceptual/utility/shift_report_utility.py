import frappe
from datetime import datetime


def calculate_time_diff(name):
    doc = frappe.get_doc("Shift Report", name)
    for row in doc.breakdown_detail:
        if row.from_time and row.to_time:
            time_1 = datetime.strptime(row.from_time, "%H:%M:%S")
            time_2 = datetime.strptime(row.to_time, "%H:%M:%S")

            time_diff = time_2 - time_1
            time_diff_in_mins = time_diff.seconds / 60
            row.time_in_mins = time_diff_in_mins