import csv
import os

import frappe
from frappe.translate import clear_cache, get_full_dict

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="osscesariolange.erpnext.com")
frappe.connect()
frappe.set_user("Administrator")

bad = frappe.db.get_value(
	"Translation",
	{"language": "pt-BR", "source_text": "Warehouse"},
	["name", "translated_text"],
	as_dict=True,
)
if bad and bad.translated_text == "Estoque":
	frappe.db.set_value("Translation", bad.name, "translated_text", "Armazém")
	print("Fixed Translation Warehouse -> Armazém")

path = "/home/frappe/frappe-bench/apps/bhcl_theme/bhcl_theme/translations/pt-BR.csv"
created = updated = skipped = 0

with open(path, encoding="utf-8") as f:
	for row in csv.reader(f):
		if not row or len(row) < 2:
			continue
		src, tgt = row[0], row[1]
		if not src or not tgt:
			continue
		if src == tgt:
			skipped += 1
			continue

		existing = frappe.db.sql(
			"""
			select name, translated_text from tabTranslation
			where language=%s and source_text=%s and ifnull(context,'')=''
			limit 1
			""",
			("pt-BR", src),
			as_dict=True,
		)
		existing = existing[0] if existing else None

		if existing:
			if existing["translated_text"] != tgt:
				frappe.db.set_value(
					"Translation",
					existing["name"],
					"translated_text",
					tgt,
					update_modified=False,
				)
				updated += 1
			else:
				skipped += 1
		else:
			doc = frappe.get_doc(
				{
					"doctype": "Translation",
					"language": "pt-BR",
					"source_text": src,
					"translated_text": tgt,
				}
			)
			doc.insert(ignore_permissions=True)
			created += 1

frappe.db.commit()
print(f"Translation upsert: created={created} updated={updated} skipped={skipped}")

clear_cache()
frappe.clear_cache()

full = get_full_dict("pt-BR")
checks = [
	"Warehouse",
	"Stock Entry",
	"Delivery Note",
	"Purchase Receipt",
	"Material Request",
	"Pick List",
	"Stock Ledger",
	"{} Available",
	"{} Pending",
	"{} To Bill",
	"Items Catalogue",
	"Unit of Measure (UOM)",
	"Total Stock Value",
	"Serial and Batch Bundle",
	"Putaway Rule",
	"Reserved Stock",
	"Stock Balance",
	"Shipment",
	"Inventory Dimension",
	"Stock Entry Type",
	"Landed Cost Voucher",
]
print("Final dictionary samples:")
for s in checks:
	print(" ", s, "->", full.get(s, "(missing)"))

frappe.destroy()
