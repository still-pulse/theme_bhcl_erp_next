import json
import os

import frappe

os.chdir("/home/frappe/frappe-bench/sites")
frappe.init(site="osscesariolange.erpnext.com")
frappe.connect()
frappe.set_user("Administrator")

NC_LABELS = {
	"Total Stock Value": "Valor total do estoque",
	"Valor Total de Estoque": "Valor total do estoque",
	"Total Warehouses": "Total de armazéns",
	"Total de Armazéns": "Total de armazéns",
	"Total Active Items": "Total de itens ativos",
	"Total de Itens Ativos": "Total de itens ativos",
}
CHART_LABELS = {
	"Warehouse wise Stock Value": "Valor do estoque por armazém",
	"Valor do estoque por armazém": "Valor do estoque por armazém",
}

for name, label in NC_LABELS.items():
	if frappe.db.exists("Number Card", name):
		frappe.db.set_value("Number Card", name, "label", label, update_modified=False)
		print("NC", name, "->", label)

for name, label in CHART_LABELS.items():
	if not frappe.db.exists("Dashboard Chart", name):
		continue
	if name == label:
		print("Chart", name, "already PT")
		continue
	if frappe.db.exists("Dashboard Chart", label):
		print("Chart skip rename", name, "(PT chart already exists:", label, ")")
		continue
	try:
		frappe.db.set_value("Dashboard Chart", name, "chart_name", label, update_modified=False)
		print("Chart", name, "->", label)
	except Exception as e:
		print("Chart rename failed", name, e)

doc = frappe.get_doc("Workspace", "Stock")
doc.title = "Stock"

SHORTCUT_FIX = {
	"Item": {"label": "Item", "format": "{} Disponíveis"},
	"Material Request": {"label": "Requisição de material", "format": "{} Pendentes"},
	"Stock Entry": {"label": "Movimento de estoque", "format": None},
	"Purchase Receipt": {"label": "Recebimento de compra", "format": "{} A faturar"},
	"Delivery Note": {"label": "Nota de entrega", "format": "{} A faturar"},
	"Stock Ledger": {"label": "Razão de estoque", "format": None},
	"Stock Balance": {"label": "Saldo de estoque", "format": None},
	"Dashboard": {"label": "Painel", "format": None},
	"Aprenda Gestão de Estoque": {"label": "Aprenda gestão de estoque", "format": None},
}

for s in doc.shortcuts or []:
	key = s.label
	if s.label not in SHORTCUT_FIX and s.link_to in SHORTCUT_FIX:
		key = s.link_to
	if key in SHORTCUT_FIX:
		fix = SHORTCUT_FIX[key]
		s.label = fix["label"]
		if fix["format"] is not None:
			s.format = fix["format"]
		elif s.format and any(x in (s.format or "") for x in ("Available", "Pending", "To Bill", "Open")):
			pass
		print("shortcut", key, "->", s.label, s.format)

for c in doc.number_cards or []:
	if c.label in NC_LABELS:
		c.label = NC_LABELS[c.label]
	elif c.number_card_name in NC_LABELS:
		c.label = NC_LABELS[c.number_card_name]
	pt_map = {
		"Total Stock Value": "Valor Total de Estoque",
		"Total Warehouses": "Total de Armazéns",
		"Total Active Items": "Total de Itens Ativos",
	}
	if c.number_card_name in pt_map and frappe.db.exists("Number Card", pt_map[c.number_card_name]):
		c.number_card_name = pt_map[c.number_card_name]
		c.label = NC_LABELS.get(c.number_card_name, c.label)
	print("ws number_card:", c.number_card_name, c.label)

for c in doc.charts or []:
	if c.label in CHART_LABELS:
		c.label = CHART_LABELS[c.label]
	pt_chart = "Valor do estoque por armazém"
	if c.chart_name == "Warehouse wise Stock Value" and frappe.db.exists("Dashboard Chart", pt_chart):
		c.chart_name = pt_chart
		c.label = "Valor do estoque por armazém"
	print("ws chart:", c.chart_name, c.label)

CARD_RENAME = {
	"Items Catalogue": "Catálogo de itens",
	"Serial No and Batch": "Nº de série e lote",
	"Tools": "Ferramentas",
	"Key Reports": "Relatórios principais",
	"Configurações": "Configurações",
	"Relatórios de Estoque": "Relatórios de estoque",
	"Relatórios Adicionais": "Relatórios adicionais",
	"Transações de Estoque": "Transações de estoque",
}

LINK_LABELS = {
	"Item": "Item",
	"Item Group": "Grupo de itens",
	"Product Bundle": "Kit de produtos",
	"Price List": "Lista de preços",
	"Item Price": "Preço do item",
	"Shipping Rule": "Regra de frete",
	"Pricing Rule": "Regra de preço",
	"Item Alternative": "Item alternativo",
	"Item Manufacturer": "Fabricante do item",
	"Customs Tariff Number": "NCM / tarifa aduaneira",
	"Material Request": "Requisição de material",
	"Stock Entry": "Movimento de estoque",
	"Delivery Note": "Nota de entrega",
	"Purchase Receipt": "Recebimento de compra",
	"Pick List": "Lista de separação",
	"Delivery Trip": "Roteiro de entrega",
	"Stock Settings": "Configurações de estoque",
	"Warehouse": "Armazém",
	"Unit of Measure (UOM)": "Unidade de medida (UDM)",
	"Item Variant Settings": "Configurações de variantes",
	"Brand": "Marca",
	"Item Attribute": "Atributo do item",
	"UOM Conversion Factor": "Fator de conversão de UDM",
	"Serial No": "Nº de série",
	"Batch": "Lote",
	"Installation Note": "Nota de instalação",
	"Serial No Service Contract Expiry": "Vencimento do contrato de serviço (série)",
	"Serial No Status": "Status do nº de série",
	"Serial No Warranty Expiry": "Vencimento de garantia (série)",
	"Stock Reconciliation": "Ajuste de estoque",
	"Landed Cost Voucher": "Custo de desembaraço",
	"Packing Slip": "Romaneio de embalagem",
	"Quality Inspection": "Inspeção de qualidade",
	"Quality Inspection Template": "Modelo de inspeção de qualidade",
	"Quick Stock Balance": "Consulta rápida de estoque",
	"Requested Items To Be Transferred": "Itens solicitados a transferir",
	"Batch Item Expiry Status": "Status de validade do lote",
	"Item Prices": "Preços de itens",
	"Itemwise Recommended Reorder Level": "Nível de reposição recomendado por item",
	"Item Variant Details": "Detalhes da variante do item",
	"Subcontracted Raw Materials To Be Transferred": "MPs subcontratadas a transferir",
	"Subcontracted Item To Be Received": "Itens subcontratados a receber",
	"Stock Analytics": "Analíticos de estoque",
	"Delivery Note Trends": "Tendência de notas de entrega",
	"Purchase Receipt Trends": "Tendência de recebimentos",
	"Sales Order Analysis": "Análise de pedidos de venda",
	"Purchase Order Analysis": "Análise de pedidos de compra",
	"Item Shortage Report": "Itens em falta",
	"Batch-Wise Balance History": "Histórico de saldo por lote",
	"Lista de Escolhas": "Lista de separação",
	"Guia de Remessa": "Nota de entrega",
	"Recibo de Compra": "Recebimento de compra",
	"Lançamento no Estoque": "Movimento de estoque",
	"Solicitação de Compras": "Requisição de material",
	"Livro de Inventário": "Razão de estoque",
	"Balanço de Estoque": "Saldo de estoque",
	"Níves de Reposição Recomendados Por Item": "Nível de reposição recomendado por item",
	"Items Solicitados Mas Não Transferidos": "Itens solicitados a transferir",
	"Preço do Item Preço": "Preço de item (estoque)",
	"Saldo Inteligente de Estoque do Armazém": "Saldo de estoque por armazém",
	"Comprovante de Custos de Desembarque": "Custo de desembaraço",
	"Conciliação de Estoque": "Ajuste de estoque",
	"Lista de Embalagem": "Romaneio de embalagem",
	"Viagem de Entrega": "Roteiro de entrega",
	"Balanço Rápido de Estoque": "Consulta rápida de estoque",
	"Unidade de Medida (UDM)": "Unidade de medida (UDM)",
	"Configurações de Estoque": "Configurações de estoque",
	"Configurações da Variante de Item": "Configurações de variantes",
	"Atributos do Item": "Atributo do item",
	"Fator de Conversão da Unidade de Medida": "Fator de conversão de UDM",
	"Número de Tarifa Alfandegária": "NCM / tarifa aduaneira",
	"Pacote de Produtos": "Kit de produtos",
	"Regra de Envio": "Regra de frete",
	"Regra de Preços": "Regra de preço",
	"Alternativa de Itens": "Item alternativo",
	"Item Fabricante": "Fabricante do item",
	"Preço do Item": "Preço do item",
	"Lista de Preços": "Lista de preços",
	"Grupo de Itens": "Grupo de itens",
}

for link in doc.links or []:
	if link.type == "Card Break" and link.label in CARD_RENAME:
		link.label = CARD_RENAME[link.label]
	elif link.label in LINK_LABELS:
		link.label = LINK_LABELS[link.label]

seen = set()
new_links = []
for link in doc.links or []:
	if link.type == "Card Break":
		key = ("Card Break", link.label)
	else:
		key = (link.link_type or "", link.link_to or "", link.label)
	if key in seen:
		print("drop duplicate", key)
		continue
	seen.add(key)
	new_links.append(link)

doc.set("links", [])
for link in new_links:
	doc.append(
		"links",
		{
			"type": link.type,
			"label": link.label,
			"link_type": link.link_type,
			"link_to": link.link_to,
			"is_query_report": link.is_query_report,
			"onboard": link.onboard,
			"dependencies": link.dependencies,
			"hidden": link.hidden,
			"icon": getattr(link, "icon", None),
			"only_for": getattr(link, "only_for", None),
		},
	)

content = json.loads(doc.content or "[]")
CARD_CONTENT_RENAME = {
	"Items Catalogue": "Catálogo de itens",
	"Serial No and Batch": "Nº de série e lote",
	"Tools": "Ferramentas",
	"Key Reports": "Relatórios principais",
	"Transações de Estoque": "Transações de estoque",
	"Relatórios de Estoque": "Relatórios de estoque",
	"Configurações": "Configurações",
	"Relatórios Adicionais": "Relatórios adicionais",
}
NC_CONTENT = {
	"Total Stock Value": "Valor Total de Estoque",
	"Total Warehouses": "Total de Armazéns",
	"Total Active Items": "Total de Itens Ativos",
}
CHART_CONTENT = {
	"Warehouse wise Stock Value": "Valor do estoque por armazém",
}

new_content = []
seen_cards = set()
for block in content:
	btype = block.get("type")
	data = block.get("data") or {}
	if btype == "number_card":
		name = data.get("number_card_name")
		if name in NC_CONTENT and frappe.db.exists("Number Card", NC_CONTENT[name]):
			data["number_card_name"] = NC_CONTENT[name]
		block["data"] = data
		new_content.append(block)
	elif btype == "chart":
		name = data.get("chart_name")
		if name in CHART_CONTENT and frappe.db.exists("Dashboard Chart", CHART_CONTENT[name]):
			data["chart_name"] = CHART_CONTENT[name]
		block["data"] = data
		new_content.append(block)
	elif btype == "card":
		cname = data.get("card_name")
		if cname in CARD_CONTENT_RENAME:
			cname = CARD_CONTENT_RENAME[cname]
			data["card_name"] = cname
		if cname in seen_cards:
			print("drop content card dup", cname)
			continue
		seen_cards.add(cname)
		block["data"] = data
		new_content.append(block)
	elif btype == "shortcut":
		sname = data.get("shortcut_name")
		map_sc = {
			"Item": "Item",
			"Material Request": "Requisição de material",
			"Stock Entry": "Movimento de estoque",
			"Purchase Receipt": "Recebimento de compra",
			"Delivery Note": "Nota de entrega",
			"Stock Ledger": "Razão de estoque",
			"Stock Balance": "Saldo de estoque",
			"Dashboard": "Painel",
			"Aprenda Gestão de Estoque": "Aprenda gestão de estoque",
		}
		if sname in map_sc:
			data["shortcut_name"] = map_sc[sname]
		block["data"] = data
		new_content.append(block)
	else:
		new_content.append(block)

doc.content = json.dumps(new_content, ensure_ascii=False)
doc.save(ignore_permissions=True)
frappe.db.commit()
print("Workspace Stock saved. cards in content:", seen_cards)
print("links count:", len(doc.links))
frappe.clear_cache()
print("Done.")
frappe.destroy()
