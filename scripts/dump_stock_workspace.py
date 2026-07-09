import json
import os

import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="osscesariolange.erpnext.com")
frappe.connect()

doc = frappe.get_doc("Workspace", "Stock")
print("name:", doc.name)
print("title:", doc.title)
print("module:", doc.module)
print("public:", doc.public)
print("content length:", len(doc.content or ""))

if doc.content:
	try:
		blocks = json.loads(doc.content)
		print("blocks:", len(blocks) if isinstance(blocks, list) else type(blocks))
		if isinstance(blocks, list):
			for i, b in enumerate(blocks[:80]):
				print(i, b.get("type"), json.dumps(b.get("data", {}), ensure_ascii=False)[:180])
	except Exception as e:
		print("content parse error", e)
		print((doc.content or "")[:500])

print("\n--- shortcuts ---")
for s in doc.shortcuts or []:
	print(s.as_dict())

print("\n--- links ---")
for l in doc.links or []:
	d = l.as_dict()
	print({k: d.get(k) for k in ("type", "label", "link_to", "link_type", "hidden", "is_query_report", "onboard", "dependencies", "only_for")})

print("\n--- number_cards ---")
for c in doc.number_cards or []:
	print(c.as_dict())

print("\n--- charts ---")
for c in doc.charts or []:
	print(c.as_dict())

frappe.destroy()
