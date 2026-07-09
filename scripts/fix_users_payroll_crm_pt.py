from __future__ import annotations

import json
import os
import re

import frappe

SITE = os.environ.get("SITE", "frontend")

TRANSLATIONS: dict[str, str] = {
	"Users": "Usuários",
	"Permission Manager": "Gerenciador de permissões",
	"Role Permissions Manager": "Gestor de permissões por função",
	"User Permissions": "Permissões de usuário",
	"Reports & Masters": "Relatórios e cadastros",
	"Reports &amp; Masters": "Relatórios e cadastros",
	"Seus Atalhos": "Seus atalhos",
	"Your Shortcuts": "Seus atalhos",
	"Quick Access": "Acesso rápido",
	"Documents": "Documentos",
	"Get started": "Comece por aqui",
	"Components to build your app": "Componentes para montar seu app",
	"Models": "Modelos",
	"DocType": "Tipo de documento",
	"Newsletter": "Informativo (newsletter)",
	"Print Format Builder (New)": "Construtor de formato de impressão (novo)",
	"Webhook": "Webhook",
	"Payroll": "Folha de pagamento",
	"Salary Payout": "Pagamento de salário",
	"Tax & Benefits": "Impostos e benefícios",
	"Tax Setup": "Configuração de impostos",
	"Benefits": "Benefícios",
	"Outgoing Salary": "Salários a pagar",
	"Quick Links": "Links rápidos",
	"Payroll Entry": "Lançamento de folha",
	"Salary Slip": "Holerite / contracheque",
	"Salary Register": "Registro de salários",
	"Salary Component": "Componente salarial",
	"Salary Structure": "Estrutura salarial",
	"Income Tax Slab": "Faixa de IR",
	"Payroll Period": "Período da folha",
	"Additional Salary": "Salário adicional",
	"Employee Incentive": "Incentivo ao colaborador",
	"Retention Bonus": "Bônus de retenção",
	"Payroll Settings": "Configurações da folha",
	"Employee Tax Exemption Declaration": "Declaração de isenção de IR do colaborador",
	"Employee Tax Exemption Proof Submission": "Comprovantes de isenção de IR",
	"Employee Tax Exemption Category": "Categoria de isenção de IR",
	"Employee Tax Exemption Sub Category": "Subcategoria de isenção de IR",
	"Employee Benefit Application": "Solicitação de benefício",
	"Employee Benefit Claim": "Reembolso de benefício",
	"Gratuity": "Gratificação / verbas rescisórias",
	"Gratuity Rule": "Regra de gratificação",
	"Employee Lifecycle": "Ciclo de vida do colaborador",
	"Employee Onboarding": "Integração de colaborador",
	"Employee Separation": "Desligamento de colaborador",
	"Empregado Onboarding": "Integração de colaborador",
	"Masters & Reports": "Cadastros e relatórios",
	"Masters &amp; Reports": "Cadastros e relatórios",
	"CRM": "CRM",
	"CRM Settings": "Configurações do CRM",
	"Lead": "Lead / prospecto",
	"Opportunity": "Oportunidade",
	"Opportunity Summary by Sales Stage": "Resumo de oportunidades por estágio",
	"Sales Pipeline Analytics": "Análise do pipeline de vendas",
	"Territory Wise Sales": "Vendas por território",
	"Learn Sales Management": "Aprenda gestão de vendas",
	"Prospect": "Prospecto",
	"{} Assigned": "{} Atribuídos",
	"{} Open": "{} Em aberto",
	"Your Shortcuts": "Seus atalhos",
}

DIRECT: dict[str, str] = {
	"Permission Manager": "Gerenciador de permissões",
	"Tax Setup": "Configuração de impostos",
	"Benefits": "Benefícios",
	"Quick Links": "Links rápidos",
	"CRM Settings": "Configurações do CRM",
	"Opportunity Summary by Sales Stage": "Resumo de oportunidades por estágio",
	"Sales Pipeline Analytics": "Análise do pipeline de vendas",
	"Lead": "Lead",  # termo comum no mercado; mantem curto
	"Newsletter": "Informativo",
	"Print Format Builder (New)": "Construtor de impressão (novo)",
	"Empregado Onboarding": "Integração de colaborador",
	"DocType": "Tipo de documento",
	"Models": "Modelos",
	"Learn Sales Management": "Aprenda gestão de vendas",
}

FORMAT_PT = {
	"{} Assigned": "{} Atribuídos",
	"{} Open": "{} Em aberto",
	"{} Pending": "{} Pendentes",
	"{} Draft": "{} Rascunho",
	"{} Available": "{} Disponíveis",
}

HEADER_MAP = {
	"Reports &amp; Masters": "Relatórios e cadastros",
	"Reports & Masters": "Relatórios e cadastros",
	"Your Shortcuts": "Seus atalhos",
	"Shortcuts": "Atalhos",
	"Documents": "Documentos",
	"Quick Access": "Acesso rápido",
	"Get started": "Comece por aqui",
	"Components to build your app": "Componentes para montar seu app",
	"Masters &amp; Reports": "Cadastros e relatórios",
	"Masters & Reports": "Cadastros e relatórios",
	"Seus Atalhos": "Seus atalhos",
}

NUMBER_CHART = {
	"Outgoing Salary": "Salários a pagar",
	"Territory Wise Sales": "Vendas por território",
}

WORKSPACES = [
	"Users",
	"Build",
	"Tools",
	"Integrations",
	"Payroll",
	"Salary Payout",
	"Tax & Benefits",
	"Employee Lifecycle",
	"CRM",
	"Support",
	"Selling",
]

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
	n = 0

	for s in doc.shortcuts or []:
		if s.label in DIRECT and s.label != DIRECT[s.label]:
			print(f"  {name} SC {s.label!r} -> {DIRECT[s.label]!r}")
			old = s.label
			s.label = DIRECT[s.label]
			if doc.content and f'"shortcut_name": "{old}"' in doc.content:
				doc.content = doc.content.replace(
					f'"shortcut_name": "{old}"', f'"shortcut_name": "{s.label}"'
				)
			n += 1
		if s.format:
			fmt = re.sub(r"^\{\}\s+", "{} ", s.format.strip()) if s.format.startswith("{}") else s.format
			pt = FORMAT_PT.get(fmt)
			if pt and s.format != pt:
				print(f"  {name} fmt {s.label}: {s.format!r} -> {pt!r}")
				s.format = pt
				n += 1

	for link in doc.links or []:
		if link.label in DIRECT and link.label != DIRECT[link.label]:
			old = link.label
			new = DIRECT[link.label]
			print(f"  {name} link {old!r} -> {new!r}")
			link.label = new
			n += 1
			if link.type == "Card Break" and doc.content:
				doc.content = doc.content.replace(f'"card_name": "{old}"', f'"card_name": "{new}"')

	for nc in doc.number_cards or []:
		key = nc.label or nc.number_card_name
		if key in NUMBER_CHART:
			new = NUMBER_CHART[key]
			if nc.label != new:
				nc.label = new
				n += 1
			if nc.number_card_name and frappe.db.exists("Number Card", nc.number_card_name):
				frappe.db.set_value(
					"Number Card", nc.number_card_name, "label", new, update_modified=False
				)

	for ch in doc.charts or []:
		key = ch.label or ch.chart_name
		if key in NUMBER_CHART:
			new = NUMBER_CHART[key]
			if ch.label != new:
				print(f"  {name} chart {ch.label!r} -> {new!r}")
				ch.label = new
				n += 1
		if ch.chart_name in NUMBER_CHART and frappe.db.exists("Dashboard Chart", ch.chart_name):
			pass

	if doc.content:
		try:
			blocks = json.loads(doc.content)
			cchg = False
			for b in blocks:
				if b.get("type") != "header":
					continue
				text = (b.get("data") or {}).get("text") or ""
				for en, pt in HEADER_MAP.items():
					if en in text:
						new_text = text.replace(f"<b>{en}</b>", f"<b>{pt}</b>")
						if new_text == text:
							new_text = text.replace(en, pt)
						if new_text != text:
							b["data"]["text"] = new_text
							cchg = True
							print(f"  {name} header -> {pt!r}")
			if cchg:
				doc.content = json.dumps(blocks, ensure_ascii=False)
				n += 1
		except Exception as e:
			print("  content err", e)

	if n:
		doc.save(ignore_permissions=True)
	return n

def main():
	os.chdir("/home/frappe/frappe-bench/sites")
	frappe.init(site=SITE)
	frappe.connect()
	frappe.set_user("Administrator")

	tc = {"created": 0, "updated": 0, "ok": 0}
	for src, tgt in TRANSLATIONS.items():
		tc[upsert_translation(src, tgt)] += 1
	print("translations:", tc)

	total = 0
	for name in WORKSPACES:
		print(f"--- {name} ---")
		total += fix_workspace(name)

	for en, pt in NUMBER_CHART.items():
		if frappe.db.exists("Dashboard Chart", en):
			try:
				frappe.db.set_value("Dashboard Chart", en, "chart_name", pt, update_modified=False)
			except Exception:
				pass

	frappe.db.commit()
	from frappe.translate import clear_cache

	clear_cache()
	frappe.clear_cache()
	print(f"workspace changes: {total}")
	print("done")
	frappe.destroy()

if __name__ == "__main__":
	main()
