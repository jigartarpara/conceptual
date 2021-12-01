import frappe


@frappe.whitelist()
def get_maintenance_checklist(template):
    maintenance_checklist_template = frappe.get_doc(
        "Maintenance Checklist Template", template)
    checklist = []
    for row in maintenance_checklist_template:
        checklist.append({
            'checklist': row.checklist
        })
    return checklist
