# Changelog — bhcl_theme

## v1.0.0 — 2026-07-09

Histórico do repositório reescrito (orphan): um único commit limpo com o estado atual do tema (sem comentários longos de desenvolvimento). Tags `v0.2.x` removidas.

Conteúdo:
- Tema Desk (tokens teal, workspace, forms, badges)
- Login customizado
- Traduções pt-BR
- Scripts de localização de workspaces
- JS: pin Editar/+Novo no page-head

## Histórico anterior (arquivado conceitualmente — commits antigos não existem mais no Git)

### v0.2.0 — 2026-07-09

### Tema Desk v2
- Design tokens completos (teal BHCL, surfaces, ink, borders)
- Polish de List View, dialogs, dropdowns, child tables
- Workspace: cards, badges, atalhos, rodapé institucional
- `prefers-reduced-motion` respeitado

### Correções de UI
- **Inputs invisíveis no idle:** removido `background: white` forçado; restaurado `--control-bg` com contraste + borda 1px nos forms (sem quebrar grid)
- **Editar / + Novo flutuando:** removido `position: fixed`; JS move o footer para o `.page-head` sticky
- `app_include_js` reativado para o pin dos botões do workspace

### Traduções
- Expandido `pt-BR.csv` / `pt.csv` (~460+ entradas): Estoque, Compras, badges, UI do Desk
- Inclui "To Receive" → "A receber" e formatos de badge

### Scripts utilitários (`scripts/`)
- `build_pt_translations.py` — gera CSVs
- `upsert_translations.py` — sobe para DocType Translation
- `fix_stock_workspace_pt.py` — localiza labels do workspace Estoque
- `audit_translations.py`, `dump_stock_workspace.py`

### Observações
- Filtro de List View por User Permission de **Item Group** fica no app `integracoes_customizadas` (não neste repositório)
- Documentação consolidada no monorepo Alessandro: `DOCUMENTACAO_CUSTOMIZACOES_BHCL.md`

## v0.1.0
- App inicial: tema Desk, login customizado, traduções base pt-BR
