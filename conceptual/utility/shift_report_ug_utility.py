import frappe


@frappe.whitelist()
def get_nrh_table(template):
    nrh_template = frappe.get_doc(
        "NRH Template", template)

    description = []

    for row in nrh_template.nrh_table:
        description.append({
            'description': row.description
        })
    return description
