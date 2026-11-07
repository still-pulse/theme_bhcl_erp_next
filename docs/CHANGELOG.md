# Changelog — bhcl_theme

Histórico reconstruído de `git tag` e `git log` do app (somente leitura) e conferido com os arquivos; as entradas
descrevem o assunto das mensagens de commit e do diff, e nada além disso. As datas são as do commit marcado pela tag.

## v2.0.0 — experimento Desk Liquid Glass · (feature/desk-liquid-glass)

Branch `feature/desk-liquid-glass`. Overlay CSS `desk_liquid_glass.css` (tokens glass/teal do portal
espelhados no Desk): canvas ambiental, navbar/sidebar/page-head/cards; menus/dropdowns/popovers
jateados; widgets translúcidos sem blur (tooltips de gráfico); tema escuro revisado; spacer
discreto; `ind_tiles.css` como SSOT de contraste dos tiles `.ind-alerta` (Jurídico/SESMT/…).
Sem mudança de login ou traduções. Major 2.x pela regra `feature/*` = major da `main` + 1.

## Limites do histórico git

- **Início do histórico:** o repositório tem 10 commits e **uma raiz**, `d9c7cdc` (2026-09-02, "Merge pull request #1
  from still-pulse/fix/check-radio-miolo"), sem pai, que já traz o app inteiro. O git não registra o que veio antes.
- **Tags fora do histórico:** `v1.0.0`, `v1.0.2` e `v1.0.3` (`git tag --no-merged HEAD`). Vêm da linha anterior à
  raiz `d9c7cdc` (histórico reescrito, como diz a entrada "Histórico anterior" abaixo) e não são ancestrais do HEAD;
  viram entradas por faixa, descritas só pelo assunto. `v1.0.2` e `v1.0.3` marcam o mesmo commit (`7da0efe`).
- **Tags que nunca existiram:** não há `v1.0.1` nem `v1.0.4`. O commit `d9c7cdc` (2026-09-02) não tem tag.
  Tags `rc/*` não existem e seriam ignoradas.
- **Tags fora de ordem:** pela data do commit, `v1.0.5` (2026-10-22) vem depois de `d9c7cdc`, que por sua vez vem
  depois de `v1.0.3` (2026-07-10); as tags `v1.0.0`–`v1.0.3` estão num ramo à parte.
- **Anotação x conteúdo:** a anotação da `v1.0.3` ("miolo visível em checkbox e radio") não bate com o commit marcado
  (`7da0efe`), que ainda não tem `desk_controls.css`. Esse arquivo só aparece em `d9c7cdc`.
- **`__version__` x tags:** de `v1.0.0` a `v1.0.6` o `__init__.py` dizia `0.1.0`; a partir da `v1.0.7` ele e a tag
  batem (hoje `1.0.11`, na tag `v1.0.11` e no HEAD). O `hooks.py` não tem `app_version`.
- **Patches:** o app não tem patches (`patches.txt` vazio) nem testes.
- **Tags anotadas e leves:** `v1.0.0`, `v1.0.2`, `v1.0.3`, `v1.0.6` e `v1.0.8` são anotadas; as demais são leves.

## v1.0.11 — ferramentas de checagem do Frappe · 2026-10-28

Commit `d7ec00f`. Adiciona commitlint, workflow de linter (`.github/workflows/linter.yml`), `.pre-commit-config.yaml`,
`.eslintrc`, `.editorconfig` e a configuração do ruff no `pyproject.toml`. Sem mudança no tema.

## v1.0.10 — `frappe-dependencies` no pyproject · 2026-10-28

Merge `3840cf0` (PR #2) do commit `4203ee7`: declara `[tool.bench.frappe-dependencies]` (`frappe>=15.0.0,<16.0.0`)
para o `bench get-app`.

## v1.0.9 — `set_title` antes do primeiro título · 2026-10-28

Commit `2bd51c5`. O JS evita exceção em `set_title` antes de haver título definido. Novo cache-buster
(`20261028a`).

## v1.0.8 — sino: botão de ação e título sem prefixo repetido · 2026-10-28

Commit `b40c99d`. O botão **Ver** da faixa de notificações abre a notificação (ou a lista, quando há várias) e o
título da aba deixa de acumular o prefixo de contagem (`frappe.utils.set_title` passa a limpá-lo). Só
`desk_theme.js` e `__init__.py`; o cache-buster não mudou.

## v1.0.7 — menu de pesquisa cortado pela borda dos modais · 2026-10-27

Commit `6eea810`. Ajuste em `desk_theme.css` (overflow do dropdown e dos modais, raio do cabeçalho do modal). Primeira
tag em que `__version__` bate com a tag. Cache-buster `20261027a`.

## v1.0.6 — rótulos da cadeia de compras em pt-BR · 2026-10-26

Commit `af1a30f`. +240 linhas em `pt-BR.csv` e em `pt.csv`: rótulos e descrições em Material Request, Request for
Quotation, Supplier Quotation, Purchase Order, Purchase Receipt, Purchase Invoice e itens, inclusive chaves com espaço
no fim (`"Accounting Dimensions "`). Os CSVs passam de 507 para 747 linhas (745 entradas).

## v1.0.5 — ajustes no tema e links do login · 2026-10-22

Commits `45737a4` (2026-10-20, "ajustes no tema do Desk (css/js)") e `8325ed9` (2026-10-22).

- **Notificações:** o `desk_theme.js` ganha o bloco de notificações (badge, título da aba, toast, sino e faixa de
  ação) e o `desk_theme.css` os estilos correspondentes; cache-buster `20261019c`.
- **Login:** os links de "Trabalhe Conosco", "Institucional", "Unidades", "página institucional", "Termos de Uso" e
  "Política de Privacidade" passam de `#` para `/jobs`, `/institucional`, `/unidades`, `/termos` e `/privacidade`.

## Sem tag — raiz do histórico atual · 2026-09-02

Commit `d9c7cdc` ("Merge pull request #1 from still-pulse/fix/check-radio-miolo"), raiz do repositório. Em relação à
`v1.0.3`, acrescenta `public/css/desk_controls.css` (checkbox e radio com miolo visível) e o inclui em
`app_include_css`; cache-buster `20260902a`. Não tem tag nem alteração de `__version__` (`0.1.0`).

## v1.0.2 e v1.0.3 — estrutura do módulo para o Frappe Cloud · 2026-07-10 (fora do histórico)

Mesmo commit `7da0efe` ("corrige package do módulo bhcl_theme (install Frappe Cloud)"), precedido por commits que
adicionam o `patches.txt` ("validação Frappe Cloud"). Anotações: `v1.0.2` "estrutura do módulo para install no Frappe
Cloud"; `v1.0.3` "miolo visível em checkbox e radio" (ver o aviso acima).

## v1.0.0 — tema BHCL Next (histórico limpo) · 2026-07-09 (fora do histórico)

Commit `09549ad` ("docs: changelog v1.0.0") sobre `218d043` ("estado inicial limpo do tema BHCL Next"). Histórico do
repositório reescrito (orphan): um único commit limpo com o estado do tema, sem comentários longos de
desenvolvimento. Segundo o changelog anterior, as tags `v0.2.x` foram removidas; nenhuma tag `v0.*` existe hoje.

Conteúdo (do changelog anterior; o conjunto de arquivos confere com o diff de `v1.0.0` e `v1.0.3`):

- Tema Desk (tokens teal, workspace, forms, badges).
- Login customizado.
- Traduções pt-BR.
- Scripts de localização de workspaces.
- JS: pin de Editar/+ Novo no page-head.

## Histórico anterior à reescrita (relato do changelog antigo, sem tag nem commit no git)

Os commits antigos não existem mais; o texto abaixo foi mantido do changelog anterior e **não é verificável** no git.

### v0.2.0 — 2026-07-09

- **Tema Desk v2:** design tokens (teal BHCL, superfícies, tinta, bordas); polimento de List View, dialogs,
  dropdowns e tabelas filhas; Workspace com cards, badges, atalhos e rodapé institucional; `prefers-reduced-motion`.
- **Correções de UI:** inputs invisíveis no estado ocioso (removido `background: white` forçado; restaurado
  `--control-bg` com borda de 1 px nos forms); "Editar / + Novo" deixa de flutuar (sem `position: fixed`; o JS move o
  rodapé para o `.page-head`); `app_include_js` reativado.
- **Traduções:** `pt-BR.csv` e `pt.csv` expandidos (~460 entradas) para Estoque, Compras, badges e UI do Desk.
- **Scripts:** `build_pt_translations.py`, `upsert_translations.py`, `fix_stock_workspace_pt.py`,
  `audit_translations.py`, `dump_stock_workspace.py`.
- **Observação:** o filtro de List View por User Permission de Item Group fica no app `integracoes_customizadas`.

### v0.1.0

- App inicial: tema Desk, login customizado, traduções base pt-BR.
