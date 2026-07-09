# BHCL Theme (`bhcl_theme`)

Tema visual do Desk (CSS/JS), página de login customizada e traduções pt-BR do **Next BHCL** (ERPNext/Frappe v15).

Repositório: [still-pulse/theme_bhcl_erp_next](https://github.com/still-pulse/theme_bhcl_erp_next)

## O que inclui

| Recurso | Descrição |
|---------|-----------|
| `desk_theme.css` | Tema do Desk (tokens teal, topbar, sidebar, workspace, forms, listas, dialogs) |
| `desk_theme.js` | Pin dos botões Editar/+Novo no page-head do Workspace |
| `www/login.html` | Tela de login customizada BHCL |
| `translations/` | pt-BR e pt (fallback) |
| `scripts/` | Utilitários de tradução e workspace |

## Instalação

```bash
bench get-app bhcl_theme https://github.com/still-pulse/theme_bhcl_erp_next.git
bench --site <site> install-app bhcl_theme
bench --site <site> clear-cache
```

Após atualizar o app:

```bash
bench --site <site> clear-cache
# hard refresh no browser (Ctrl+Shift+R)
```

## Hooks

```python
app_include_css = "/assets/bhcl_theme/css/desk_theme.css"
app_include_js = "/assets/bhcl_theme/js/desk_theme.js"
```

## Changelog

Ver [docs/CHANGELOG.md](docs/CHANGELOG.md).

## License

MIT
