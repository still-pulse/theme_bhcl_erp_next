from __future__ import annotations

import json
import os

import frappe

SITE = os.environ.get("SITE", "frontend")

TRANSLATIONS: dict[str, str] = {
	"Accounting": "Contabilidade",
	"Financial Reports": "Relatórios financeiros",
	"Payables": "Contas a pagar",
	"Receivables": "Contas a receber",
	"Learn Accounting": "Aprenda contabilidade",
	"Reports & Masters": "Relatórios e cadastros",
	"Reports &amp; Masters": "Relatórios e cadastros",
	"Shortcuts": "Atalhos",
	"Tax Masters": "Cadastros de impostos",
	"Bank Reconciliation Tool": "Ferramenta de conciliação bancária",
	"Dunning": "Cobrança",
	"Ledgers": "Razões / ledgers",
	"Share Ledger": "Livro de ações",
	"UAE VAT 201": "UAE VAT 201",  # nome de relatório regional
	"Total Outgoing Bills": "Total de faturas a pagar",
	"Total Incoming Bills": "Total de faturas a receber",
	"Total Incoming Payment": "Total de recebimentos",
	"Total Outgoing Payment": "Total de pagamentos",
	"Profit and Loss": "Resultado (DRE)",
	"Profit and Loss Statement": "Demonstrativo de resultados",
	"Accounts": "Contas",
	"Accounting Dashboard": "Painel contábil",
	"Bank Transaction": "Transação bancária",
	"Payment Order": "Ordem de pagamento",
	"Process Deferred Accounting": "Processar contabilidade diferida",
	"Invoice Discounting": "Antecipação de recebíveis",
	"Loyalty Point Entry": "Lançamento de pontos de fidelidade",
	"POS Closing Entry": "Fechamento de PDV",
	"POS Opening Entry": "Abertura de PDV",
	"POS Invoice": "Fatura PDV",
	"POS Profile": "Perfil de PDV",
	"Accounting Dimension Filter": "Filtro de dimensão contábil",
	"Auto Repeat": "Repetição automática",
	"Cheque Print Template": "Modelo de impressão de cheque",
	"Ledger Merge": "Mesclar razão",
	"Ledger Health": "Saúde do razão",
	"Coupon Code": "Cupom",
	"Pricing Rule": "Regra de preço",
	"Promotional Scheme": "Esquema promocional",
	"Currency Exchange Settings": "Configurações de câmbio",
	"Exchange Rate Revaluation": "Reavaliação da taxa de câmbio",
	"Multi Currency": "Multimoeda",
	"Subscription Management": "Gestão de assinaturas",
	"Share Management": "Gestão de ações",
	"Cost Center and Budgeting": "Centro de custo e orçamento",
	"Opening and Closing": "Abertura e fechamento",
	"Accounting Masters": "Cadastros contábeis",
	"Banking": "Bancos",
	"Payments": "Pagamentos",
	"Invoicing": "Faturamento",
	"Reports": "Relatórios",
	"Profitability": "Rentabilidade",
	"Financial Statements": "Demonstrativos financeiros",
	"Other Reports": "Outros relatórios",
	"Chart of Accounts": "Plano de contas",
	"Journal Entry": "Lançamento contábil",
	"Payment Entry": "Lançamento de pagamento",
	"General Ledger": "Livro razão",
	"Trial Balance": "Balancete",
	"Accounts Receivable": "Contas a receber",
	"Accounts Payable": "Contas a pagar",
	"Dashboard": "Painel",
	"Sales Invoice": "Nota fiscal de venda",
	"Purchase Invoice": "Nota fiscal de compra",
}

DIRECT_LABEL_MAP = {
	"Tax Masters": "Cadastros de impostos",
	"Bank Reconciliation Tool": "Ferramenta de conciliação bancária",
	"Dunning": "Cobrança",
	"Ledgers": "Razões",
	"Learn Accounting": "Aprenda contabilidade",
}

NUMBER_CARD_LABELS = {
	"Total Outgoing Bills": "Total de faturas a pagar",
	"Total Incoming Bills": "Total de faturas a receber",
	"Total Incoming Payment": "Total de recebimentos",
	"Total Outgoing Payment": "Total de pagamentos",
}

CHART_LABELS = {
	"Profit and Loss": "Resultado (DRE)",
}

HEADER_HTML = {
	"Reports &amp; Masters": "Relatórios e cadastros",
	"Reports & Masters": "Relatórios e cadastros",
	"Shortcuts": "Atalhos",
}

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

def fix_workspace(name: str) -> int:
	if not frappe.db.exists("Workspace", name):
		return 0
	doc = frappe.get_doc("Workspace", name)
	changes = 0

	if doc.title in TRANSLATIONS and TRANSLATIONS[doc.title] != doc.title:
		pass

	for s in doc.shortcuts or []:
		if s.label in DIRECT_LABEL_MAP:
			new = DIRECT_LABEL_MAP[s.label]
			if s.label != new:
				print(f"  {name} shortcut label {s.label!r} -> {new!r}")
				s.label = new
				changes += 1

	for link in doc.links or []:
		if link.label in DIRECT_LABEL_MAP:
			new = DIRECT_LABEL_MAP[link.label]
			if link.label != new:
				print(f"  {name} link {link.label!r} -> {new!r}")
				old = link.label
				link.label = new
				changes += 1
				if doc.content and link.type == "Card Break":
					doc.content = doc.content.replace(
						f'"card_name": "{old}"', f'"card_name": "{new}"'
					)
					doc.content = doc.content.replace(
						f'"card_name": "{old}"', f'"card_name": "{new}"'
					)

	for nc in doc.number_cards or []:
		if nc.label in NUMBER_CARD_LABELS:
			new = NUMBER_CARD_LABELS[nc.label]
			if nc.label != new:
				print(f"  {name} nc label {nc.label!r} -> {new!r}")
				nc.label = new
				changes += 1
		key = nc.number_card_name
		if key in NUMBER_CARD_LABELS and frappe.db.exists("Number Card", key):
			new = NUMBER_CARD_LABELS[key]
			frappe.db.set_value("Number Card", key, "label", new, update_modified=False)
			print(f"  Number Card {key!r} label -> {new!r}")

	for ch in doc.charts or []:
		if ch.label in CHART_LABELS:
			new = CHART_LABELS[ch.label]
			if ch.label != new:
				print(f"  {name} chart label {ch.label!r} -> {new!r}")
				ch.label = new
				changes += 1

	if doc.content:
		try:
			blocks = json.loads(doc.content)
			c_changed = False
			for b in blocks:
				if b.get("type") != "header":
					continue
				text = (b.get("data") or {}).get("text") or ""
				for en, pt in HEADER_HTML.items():
					if en in text:
						new_text = text
						if f"<b>{en}</b>" in text:
							new_text = text.replace(f"<b>{en}</b>", f"<b>{pt}</b>")
						elif en in text:
							new_text = text.replace(en, pt)
						if new_text != text:
							b["data"]["text"] = new_text
							c_changed = True
							print(f"  {name} header -> {pt!r}")
			if c_changed:
				doc.content = json.dumps(blocks, ensure_ascii=False)
				changes += 1
		except Exception as e:
			print("  content parse err", e)

	if doc.content:
		for en, pt in DIRECT_LABEL_MAP.items():
			if f'"card_name": "{en}"' in doc.content:
				doc.content = doc.content.replace(f'"card_name": "{en}"', f'"card_name": "{pt}"')
				print(f"  {name} content card_name {en!r} -> {pt!r}")
				changes += 1
			if f'"shortcut_name": "{en}"' in doc.content:
				doc.content = doc.content.replace(
					f'"shortcut_name": "{en}"', f'"shortcut_name": "{pt}"'
				)
				changes += 1

	if changes:
		doc.save(ignore_permissions=True)
	return changes

def main():
	os.chdir("/home/frappe/frappe-bench/sites")
	frappe.init(site=SITE)
	frappe.connect()
	frappe.set_user("Administrator")

	tc = {"created": 0, "updated": 0, "ok": 0}
	for src, tgt in TRANSLATIONS.items():
		r = upsert_translation(src, tgt)
		tc[r] += 1
	print("translations:", tc)

	total = 0
	for name in ("Accounting", "Payables", "Receivables", "Financial Reports"):
		print(f"--- {name} ---")
		total += fix_workspace(name)

	frappe.db.commit()
	from frappe.translate import clear_cache

	clear_cache()
	frappe.clear_cache()
	print(f"workspace field changes: {total}")
	print("done")
	frappe.destroy()

if __name__ == "__main__":
	main()
