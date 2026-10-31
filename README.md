# BHCL Theme (`bhcl_theme`)

App Frappe v15 com a **identidade visual do Desk** do Next BHCL (Beneficência Hospitalar de Cesário Lange): tema CSS
em teal, notificações em três níveis, a página `/login` customizada e as traduções pt-BR. Não tem DocTypes, patches
nem código de servidor além do `www/login.py`.

Repositório: [still-pulse/theme_bhcl_erp_next](https://github.com/still-pulse/theme_bhcl_erp_next). Versão atual:
**1.0.11** (`bhcl_theme/__init__.py`, tag `v1.0.11`).

## Funcionalidades

- **Tema do Desk** (`public/css/desk_theme.css`, 982 linhas): tokens de cor `--bhcl-*` (teal, tinta, linhas,
  superfícies) que sobrescrevem as variáveis do Frappe (`--primary`, `--bg-color`, `--text-color`, `--border-color`...),
  com estilos para navbar, sidebar, page-head, workspace, formulários, listas, tabelas filhas (grid), botões,
  indicadores, dropdowns, Awesomplete, modais e barras de rolagem. Há ajustes responsivos (≤1199, ≤767 e ≤575 px;
  ≥1440 px) e `prefers-reduced-motion` respeitado.
- **Controles Check e Radio** (`public/css/desk_controls.css`, 197 linhas): checkbox e radio com miolo visível (fundo
  teal e check branco quando marcados; anel e miolo no radio) que não se perdem no `:focus`. Carrega depois do
  `desk_theme.css`.
- **Botões do Workspace no page-head** (`public/js/desk_theme.js`, 1º bloco): move o rodapé do Workspace (Editar,
  + Novo) para o `.page-head` fixo, em vez de flutuar sobre o conteúdo. Roda em `page-change`, `form-refresh` e
  `ready`, com novas tentativas após 50, 200 e 500 ms porque o Workspace renderiza depois.
- **Notificações em três níveis** (`desk_theme.js`, 2º bloco; estilos no fim do `desk_theme.css`):
  - **Badge e título da aba, sempre:** contagem de não lidas no sino (`9+` acima de 9, `99+` a partir de 100), `aria-label`
    com a contagem e prefixo `(n)` no título da aba.
  - **Toast e sino balançando, na chegada:** ao receber o evento realtime `notification`, mostra um toast de 6 s com
    link para o documento (ou "N novas notificações", que abre a lista de não lidas). Chegadas em até 10 s são
    agrupadas; com a aba oculta o toast espera ela voltar.
  - **Faixa abaixo da navbar** enquanto houver não lidas dos tipos `Assignment`, `Mention` ou `Alert`. Botões
    **Ver** (abre o item, que é marcado como lido, ou a lista quando há vários), **Lembrar mais tarde** (4 h,
    em `localStorage`) e **Fechar** (até o fim da sessão, em `sessionStorage`). Ambos valem para o conjunto atual:
    um item novo que pede ação reabre a faixa. Alertas de `PDF OCR Document` (conclusão do OCR, do app `pdf_ocr`)
    contam no badge, mas não acionam a faixa.
  - Lê até 100 `Notification Log` não lidos do usuário e recontagem após fechar o dropdown, clicar na lista ou
    voltar à aba. Só ativa se o sino existir (notificações ligadas nas Desk Settings) e o usuário não for Guest.
  - `frappe.utils.set_title` é envelopado para tirar prefixos `(n)` já aplicados, evitando `(1) (1) ...` ao voltar a
    uma rota.
- **Login customizado** (`www/login.html` + `www/login.py`): tela de duas colunas em HTML e estilos inline, com faixa
  "portal exclusivo dos projetos vinculados ao Núcleo Alphaville", menu (Trabalhe Conosco, Institucional, Unidades),
  logotipo (`public/images/bhcl_logo.png`) e rodapé com Termos e Privacidade. O formulário autentica por
  `POST /` com `cmd=login`, mostra/oculta a senha e respeita `redirect-to`. `login.py` não deixa a página em cache e
  redireciona quem já está logado (para `redirect-to`, o caminho padrão do app, `/app` ou a home do site para
  Website User).
- **Traduções pt-BR** (`translations/pt-BR.csv` e `pt.csv`): **745 entradas** cada (747 linhas; algumas têm quebra de
  linha), em português do Brasil, com os dois arquivos idênticos (o `pt.csv` é cópia, como fallback do idioma
  `pt`). Cobrem Estoque, Compras (Material Request, RFQ, Supplier Quotation, Purchase Order/Receipt/Invoice), formatos
  de badge (`{} To Receive` → `{} A receber`), rótulos de workspace e da UI do Desk.
- **Scripts** (`scripts/`, 9 arquivos): utilitários manuais de localização, ver [Scripts](#scripts).

## Requisitos

- Frappe v15 (`frappe>=15.0.0,<16.0.0`, em `[tool.bench.frappe-dependencies]` do `pyproject.toml`) e Python ≥ 3.11
  (`requires-python`).
- Não declara `required_apps` no `hooks.py` e não importa nenhum outro app. O `pyproject.toml` não lista dependências
  Python de runtime (`dependencies` só traz um comentário).
- O JS cita o DocType `PDF OCR Document` do app opcional `pdf_ocr` (lista `INFO_DOCTYPES`); sem esse app, nada muda.

## Instalação

```bash
# na raiz da bench
bench get-app bhcl_theme https://github.com/still-pulse/theme_bhcl_erp_next.git
bench --site <site> install-app bhcl_theme
bench --site <site> clear-cache
```

Após atualizar o app: `bench build --app bhcl_theme` (se necessário), `bench --site <site> clear-cache` e atualização
forçada no navegador (Ctrl+Shift+R).

## Configuração e uso

Não há tela de configuração: o tema vale para todo o Desk assim que o app é instalado. O `hooks.py` injeta só:

```python
app_include_css = [
	"/assets/bhcl_theme/css/desk_theme.css?v=20261028a",
	"/assets/bhcl_theme/css/desk_controls.css?v=20261028a",
]
app_include_js = "/assets/bhcl_theme/js/desk_theme.js?v=20261028a"
```

Não há `web_include_*`, `boot_session`, `fixtures`, `after_install` nem outros hooks. O sufixo `?v=AAAAMMDDx` é o
**cache-buster**: troque-o nos três caminhos sempre que mudar CSS ou JS, senão o navegador serve a versão antiga (o
valor atual vem da v1.0.9).

### Traduções

Os CSVs são carregados pelo Frappe como traduções do app. Para gravá-las como registros de `Translation` no site
(necessário para chaves que o carregamento por app não cobre), use o `upsert_translations.py`. Ao acrescentar um
rótulo, edite os **dois** CSVs; o teste `test_traducoes_compras.py` do `integracoes_customizadas` lê esses arquivos.

### Scripts

São rotinas avulsas para `bench --site <site> console` ou `python`, escritas para o ambiente de quem as criou: abrem
o site com `frappe.init` depois de `os.chdir("/home/frappe/frappe-bench/sites")`. Quatro têm o site fixo
(`osscesariolange.erpnext.com`, `audit`, `dump`, `fix_stock`, `upsert`), um usa `frontend` (`inspect_buying_shortcuts`) e
três leem a variável `SITE` (padrão `frontend`). Confira o site antes de rodar: os `fix_*` e o `upsert` **gravam**
no banco (`Translation`, `Workspace`, `Number Card`, `Dashboard Chart`) e fazem `frappe.db.commit()`.

| Script | O que faz |
| --- | --- |
| `build_pt_translations.py` | Gera `pt-BR.csv` e `pt.csv` a partir da lista `TRANSLATIONS` do próprio arquivo (461 chaves distintas). Não toca no banco. |
| `upsert_translations.py` | Grava as linhas de `pt-BR.csv` como `Translation` pt-BR (cria ou atualiza), corrige "Warehouse" → "Armazém" e limpa o cache. |
| `audit_translations.py` | Somente leitura: idioma do sistema e dos usuários, Workspace Stock, traduções faltantes, DocTypes e relatórios do Estoque sem tradução. |
| `dump_stock_workspace.py` | Somente leitura: imprime nome, título, módulo e blocos de conteúdo do Workspace Stock. |
| `inspect_buying_shortcuts.py` | Somente leitura: confere se formatos de badge (`{} To Receive`...) estão no dicionário pt-BR e lista atalhos dos Workspaces de compras. |
| `fix_stock_workspace_pt.py` | Localiza o Workspace Stock: Number Cards, Dashboard Chart, atalhos, links e conteúdo. |
| `fix_accounting_workspace_pt.py` | Idem para Accounting, Payables, Receivables e Financial Reports. |
| `fix_users_payroll_crm_pt.py` | Idem para Users, Build, Tools, Integrations, Payroll, Salary Payout, Tax & Benefits, Employee Lifecycle, CRM, Support e Selling. |
| `fix_workspace_badges_pt.py` | Traduz o `format` dos atalhos (badges) de todos os Workspaces públicos e do Buying. |

> O `build_pt_translations.py` está defasado em relação aos CSVs: tem 461 chaves, os arquivos têm 745 (as 240 linhas
> da v1.0.6 foram acrescentadas direto nos CSVs). Rodá-lo **sobrescreve** `pt-BR.csv` e `pt.csv` e perde essas
> entradas. Não o use sem antes trazer o conteúdo dos CSVs para ele.

## Relação com o `bhcl_site`

O tema do Desk e a página `/login` ficam **aqui**; o `bhcl_site` cuida do site público e da área logada e **não
altera o Desk** (nem tem `app_include_*`). O `login.html` estende `templates/base.html` direto e não recebe a camada
visual do `bhcl_site`. Os links do login (`/institucional`, `/unidades`, `/jobs`, `/termos`, `/privacidade`) apontam
para páginas públicas servidas pelo `bhcl_site` e por `Web Page` do Desk; sem o `bhcl_site`, esses links dão 404.

Pendências visíveis no `login.html`: "Suporte TI", "Esqueceu a senha?" e "Inscrever-se" não têm destino
(`href="#"` ou sem link) e os botões "Entrar com Google" e "Entrar com Office 365" não têm ação. A tela de `/login`
não oferece login social nem login por CPF (o `bhcl_site` documenta o link "Entrar com CPF" como falta aqui).

## Desenvolvimento

```text
bhcl_theme/
├── CLAUDE.md                      instruções para agentes (local, ignorado pelo git)
├── docs/CHANGELOG.md              histórico por versão
├── scripts/                       9 utilitários de tradução e Workspace
├── .github/workflows/linter.yml   commitlint, pre-commit/ruff, Semgrep e pip-audit (só em PR)
├── .pre-commit-config.yaml, .eslintrc, .editorconfig, commitlint.config.js
└── bhcl_theme/
    ├── hooks.py                   app_include_css/js e cache-buster
    ├── modules.txt, patches.txt   módulo "BHCL Theme"; patches.txt vazio
    ├── public/css/                desk_theme.css, desk_controls.css
    ├── public/js/                 desk_theme.js
    ├── public/images/             bhcl_logo.png
    ├── translations/              pt-BR.csv, pt.csv (745 entradas)
    └── www/                       login.html, login.py
```

A pasta `bhcl_theme/bhcl_theme/` (módulo Frappe) só tem `__init__.py`.

### Testes

**O app não tem testes** (nenhum arquivo em `git ls-files` com "test" no caminho). Alterações no tema e na tela de
login são conferidas à mão no navegador (Desk e `/login`, em celular e desktop). Para validar as traduções existe o
`test_traducoes_compras.py` do `integracoes_customizadas`:

```bash
bench --site dev run-tests --module integracoes_customizadas.integracoes_customizadas.tests.test_traducoes_compras
```

### Lint

`.pre-commit-config.yaml` e o workflow rodam ruff, ruff-format, prettier, eslint e commitlint (mensagens
convencionais). O `pyproject.toml` configura o ruff (tabs, `line-length = 110`, `target-version = "py311"`). Em
2026-10-31, `env/bin/ruff check scripts bhcl_theme` aponta 1 erro (F601, chave repetida `"Your Shortcuts"` em
`scripts/fix_users_payroll_crm_pt.py:72`) e `ruff format --check` reformataria 5 arquivos. O CI roda em Python 3.10,
enquanto o app pede ≥ 3.11.

## Documentação

- [docs/CHANGELOG.md](docs/CHANGELOG.md): histórico por versão, com os limites do git.
- Visão geral dos apps e das dependências entre eles: `CLAUDE.md` na raiz da bench.

## Licença

MIT, conforme `app_license = "mit"` no `hooks.py`. O repositório não tem arquivo de licença (`LICENSE`/`license.txt`).
