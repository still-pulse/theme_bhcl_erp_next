# bhcl_theme

O restante das instruções do repositório está em `CLAUDE.md`. Regra de versão:

- **Branch `feature/*` usa o major da `main` + 1** (regra vigente desde 2026-11-01). Minor e patch correm normalmente
  dentro dele: com a `main` em `vX.Y.Z`, a feature nasce em `v(X+1).0.0` e segue `v(X+1).0.1`, `v(X+1).1.0`...
  enquanto estiver na branch. Se a `main` subir de major, a feature sobe junto. Confira a versão da `main`
  (`git show main:bhcl_theme/__init__.py`) e `git tag` antes de tagear, e não reutilize número existente.

## Git tags in cloud agent sessions

Agents running in a Claude Code cloud session cannot push git tags: the egress proxy answers `HTTP 403` (verified
2026-11-26; branch pushes work). It is a policy denial: do not retry or route around it. Commit and push the branch,
update `__version__` only when the task asks, and report once that the tag is pending. A human creates the tag
(`git tag vX.Y.Z && git push origin vX.Y.Z` from a normal machine, or a GitHub release). Details:
`pulse_platform/docs/handoff-dev-data.md`.
