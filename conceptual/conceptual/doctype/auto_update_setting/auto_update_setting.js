// Copyright (c) 2021, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Auto Update Setting', {
    // refresh: function(frm) {

    // }
    update_dsr_surface: function (frm) {
        frappe.call({
            method: "conceptual.utility.dsr_utility.enque_update_dsr",
            callback: function (r) {
                frappe.msgprint("DSR Surface updated")
            }
        })
    },
    update_machine: function (frm) {
        frappe.call({
            method: "conceptual.utility.machine_utility.enque_update_machine",
            callback: function (r) {
                frappe.msgprint("Machine records updated")
            }
        })
    },
    update_dsr_surface_report: function (frm) {
        frappe.call({
            method: "conceptual.utility.dsr_surface_report_utility.enque_update_dsr_surface_report",
            callback: function (r) {
                frappe.msgprint("DSR Surface Report updated")
            }
        })
    }
});
