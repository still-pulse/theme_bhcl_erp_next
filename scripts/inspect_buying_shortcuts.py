import os

import frappe
from frappe import _
from frappe.translate import clear_cache, get_full_dict

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="frontend")
frappe.connect()
frappe.local.lang = "pt-BR"
clear_cache()
full = get_full_dict("pt-BR")

samples = [
	"{} To Receive",
	"To Receive",
	"{} Pending",
	"{} Available",
	"{} To Bill",
	"{} To Deliver",
	"{} Open",
	"{} Overdue",
	"{} Closed",
	"{} Draft",
	"{} Ordered",
	"{} Partially Received",
	"{} Partially Ordered",
	"{} Received",
	"{} Stopped",
]
print("=== dict ===")
for s in samples:
	print(f"  {s!r} -> {full.get(s)!r} | _()={_(s)!r}")

print("\n=== workspaces with compra/buy ===")
for n in frappe.get_all("Workspace", pluck="name"):
	if any(x in n.lower() for x in ("buy", "compra", "purchase", "stock", "sell")):
		print(" ", n)

for name in ("Buying", "Compras", "Purchase"):
	if frappe.db.exists("Workspace", name):
		doc = frappe.get_doc("Workspace", name)
		print(f"\n=== Workspace {doc.name} title={doc.title!r} ===")
		for s in doc.shortcuts or []:
			print(f"  label={s.label!r} format={s.format!r} link={s.link_to!r} type={s.type}")

frappe.destroy()
