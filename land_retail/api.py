import frappe
from frappe import _


@frappe.whitelist()
def notification_email(payment_entry, method):
    if payment_entry.payment_type == "Receive":
        for ref in payment_entry.references:
            if(ref.reference_doctype == "Sales Invoice"):
                invoice = frappe.get_doc("Sales Invoice", ref.reference_name)
                if ((invoice.total - invoice.outstanding_amount) >= (invoice.total * 0.2)) & ((invoice.total - invoice.outstanding_amount) < (invoice.total * 0.5)):
                    frappe.sendmail(
                        recipients="duncan@thebantoo.com",
                        sender="erp@thebantoo.com",
                        subject="20" + "%" + " Email Test",
                        message="Running Email Test"
                    )
                    frappe.msgprint(_("Hello World!"))
                elif ((invoice.total - invoice.outstanding_amount) >= (invoice.total * 0.5)) & ((invoice.total - invoice.outstanding_amount) < invoice.total):
                    frappe.sendmail(
                        recipients="duncan@thebantoo.com",
                        sender="erp@thebantoo.com",
                        subject="50" + "%" + " Email Test",
                        message="Running Email Test"
                    )
                    frappe.msgprint(_("Hello Space!"))
                elif (invoice.outstanding_amount == 0):
                    frappe.sendmail(
                        recipients="duncan@thebantoo.com",
                        sender="erp@thebantoo.com",
                        subject="100" + "%" + " Email Test",
                        message="Running Email Test"
                    )
                    frappe.msgprint(_("Hello Universe!"))

def create_item(plot, method):
    settings = frappe.get_doc('Land Settings')
    plot_item = frappe.get_doc({
        "doctype": "Item",
        "item_group": settings.land_for_sale_group,
        "default_warehouse": settings.sales_land_warehouse,
        "item_code": "Plot " + str(plot.plot_id),
        "land": 1,
        "is_stock_item": 1,
        "stock_uom": "Nos",
        "opening_stock": 1,
        "standard_rate": plot.plot_price,
        "is_purchase_item": 0,
        "is_sales_item": 1,
        "valuation_rate": plot.plot_price,
        "include_item_in_manufacturing": 0,
        "description": "Project: " + str(plot.project) + "<br>" + "Subdivision: " + str(plot.subdivision) + "<br>" + "Plot ID: " + str(plot.plot_id) + "<br>" + "Dimensions: " + str(plot.dimensions) + "<br>" + "Area: " + str(plot.area) + "sqm",
    })
    plot_item.flags.ignore_permission = True
    plot_item.insert()

    plot.plot_item = "Plot " + str(plot.plot_id)
    plot.save()


def calculate_plot_details(plot, method):
    if not plot.area or int(plot.area) <= 0:
        plot.area = int(plot.width) * int(plot.length)

    plot.dimensions = str(plot.width) + " x " + str(plot.length) + "m"


def project_item(project, method):
    settings = frappe.get_doc('Land Settings')
    project_item = frappe.get_doc({
        "doctype": "Item",
        "item_name": project.project_name,
        "item_group": settings.land_in_bulk_group,
        "land": 1,
        "item_code": project.project_name,
        "is_stock_item": 1,
        "stock_uom": "Square Meter",
        "include_item_in_manufacturing": 0,
    })
    project_item.flags.ignore_permission = True
    project_item.insert()
