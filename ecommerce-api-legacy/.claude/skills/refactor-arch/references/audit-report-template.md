# Template de relatório de auditoria

```markdown
# Relatório de auditoria de arquitetura - <project>

## Fase 1 - Análise do projeto

- Linguagem:
- Framework:
- Dependências:
- Domínio:
- Arquitetura:
- Arquivos-fonte analisados:
- Tabelas/modelos de BD:

## Resumo

| Severidade | Quantidade |
|---|---:|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 0 |
| LOW | 0 |

## Achados

### [<SEVERIDADE>] <Título do achado>

- Arquivo: `<path>:<linha ou intervalo>`
- Descrição:
- Impacto:
- Recomendação:

## Plano de validação da Fase 3

- Checagem de boot/import:
- Checagens de endpoints:
- Risco residual:
```

Regras:

- Achados devem ser ordenados por severidade e depois por impacto esperado.
- Use números de linha exatos do checkout atual.
- Evite localizações vagas como "múltiplos arquivos", salvo quando cada arquivo importante estiver listado.
- Mencione se um achado corresponde a uma API obsoleta.
