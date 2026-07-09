from __future__ import annotations

import os
import re

import frappe

SITE = os.environ.get("SITE", "frontend")

FORMAT_TO_PT: dict[str, str] = {
	"{} Available": "{} Disponíveis",
	"{} Pending": "{} Pendentes",
	"{} To Bill": "{} A faturar",
	"{} To Receive": "{} A receber",
	"{} To Deliver": "{} A entregar",
	"{} Open": "{} Em aberto",
	"{} Overdue": "{} Atrasados",
	"{} Closed": "{} Fechados",
	"{} Draft": "{} Rascunho",
	"{} Ordered": "{} Pedidos",
	"{} Received": "{} Recebidos",
	"{} Partially Received": "{} Parcialmente recebidos",
	"{} Partially Ordered": "{} Parcialmente pedidos",
	"{} Submitted": "{} Enviados",
	"{} Cancelled": "{} Cancelados",
	"{} Active": "{} Ativos",
	"{} Inactive": "{} Inativos",
	"{} Completed": "{} Concluídos",
	"{} Stopped": "{} Parados",
	"{} Paid": "{} Pagos",
	"{} Unpaid": "{} Não pagos",
}

TRANSLATIONS: list[tuple[str, str]] = [
	*FORMAT_TO_PT.items(),
	*[("{}  " + k[3:], v) for k, v in FORMAT_TO_PT.items()],
	("To Receive", "A receber"),
	("To Bill", "A faturar"),
	("To Deliver", "A entregar"),
	("Pending", "Pendente"),
	("Available", "Disponível"),
	("Open", "Aberto"),
	("Overdue", "Atrasado"),
	("Closed", "Fechado"),
]

def _norm_format(fmt: str) -> str:
	if not fmt:
		return fmt
	fmt = fmt.strip()
	if fmt.startswith("{}"):
		fmt = re.sub(r"^\{\}\s+", "{} ", fmt)
	return fmt

def upsert_translation(src: str, tgt: str) -> str:
	rows = frappe.db.sql(
		"""
		select name, translated_text from tabTranslation
		where language=%s and source_text=%s and ifnull(context,'')=''
		limit 1
		""",
		("pt-BR", src),
		as_dict=True,
	)
	if rows:
		if rows[0].translated_text != tgt:
			frappe.db.set_value(
				"Translation", rows[0].name, "translated_text", tgt, update_modified=False
			)
			return "updated"
		return "ok"
	frappe.get_doc(
		{
			"doctype": "Translation",
			"language": "pt-BR",
			"source_text": src,
			"translated_text": tgt,
		}
	).insert(ignore_permissions=True)
	return "created"

def main():
	os.chdir("/home/frappe/frappe-bench/sites")
	frappe.init(site=SITE)
	frappe.connect()
	frappe.set_user("Administrator")

	tc = {"created": 0, "updated": 0, "ok": 0}
	for src, tgt in TRANSLATIONS:
		tc[upsert_translation(src, tgt)] += 1
	print("translations:", tc)

	fixed = 0
	for name in frappe.get_all("Workspace", filters={"public": 1}, pluck="name"):
		doc = frappe.get_doc("Workspace", name)
		changed = False
		for s in doc.shortcuts or []:
			if not s.format:
				continue
			norm = _norm_format(s.format)
			if s.format in FORMAT_TO_PT.values() or norm in FORMAT_TO_PT.values():
				if s.format != norm and norm in FORMAT_TO_PT.values():
					s.format = norm
					changed = True
					fixed += 1
				continue
			pt = FORMAT_TO_PT.get(norm)
			if pt and s.format != pt:
				print(f"  {name}: {s.label!r} format {s.format!r} -> {pt!r}")
				s.format = pt
				changed = True
				fixed += 1
			elif norm != s.format:
				print(f"  {name}: {s.label!r} normalize {s.format!r} -> {norm!r}")
				s.format = norm
				changed = True
				fixed += 1
		if changed:
			doc.save(ignore_permissions=True)

	frappe.db.commit()
	from frappe.translate import clear_cache

	clear_cache()
	frappe.clear_cache()
	print(f"workspace formats fixed: {fixed}")

	if frappe.db.exists("Workspace", "Buying"):
		doc = frappe.get_doc("Workspace", "Buying")
		for s in doc.shortcuts or []:
			if s.format:
				print("Buying:", s.label, "=>", repr(s.format))
	print("done")
	frappe.destroy()

if __name__ == "__main__":
	main()
