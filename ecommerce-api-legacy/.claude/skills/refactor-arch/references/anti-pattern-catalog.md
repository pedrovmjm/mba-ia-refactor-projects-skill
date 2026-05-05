# Catálogo de antipadrões

Use esta escala de severidade:

- CRITICAL: exposição de segurança, execução arbitrária de código/query, colapso severo de arquitetura ou risco de quebrar produção.
- HIGH: violação forte de MVC/SOLID, alto acoplamento, lógica de negócio difícil de testar, tratamento inseguro de credenciais.
- MEDIUM: lógica duplicada, queries N+1, validação ausente, tratamento de erros fraco, risco de performance.
- LOW: nomes, valores mágicos, imports/logs ruidosos, problemas de legibilidade.

## Antipadrões obrigatórios

1. **Endpoint de query/comando arbitrário** (CRITICAL)
   - Sinais: rotas que aceitam SQL bruto, comandos de shell, `eval`, `exec`.
   - Recomende: remover o endpoint ou restringi-lo a operações administrativas explícitas com métodos de repositório parametrizados.

2. **Segredos/credenciais embutidos no código** (CRITICAL)
   - Sinais: `SECRET_KEY = "..."`, chaves de API, senhas, tokens vivos no código-fonte.
   - Recomende: configuração baseada em ambiente, com defaults seguros apenas para desenvolvimento local.

3. **Risco de injeção SQL/NoSQL** (CRITICAL)
   - Sinais: SQL concatenado por string, interpolação de query por template, filtros sem sanitização.
   - Recomende: queries parametrizadas/query builders de ORM.

4. **God Class/God Module** (HIGH)
   - Sinais: uma classe/arquivo é responsável por rotas, BD, regras de negócio, validação, relatórios e efeitos colaterais.
   - Recomende: dividir em routes/views, controllers, models/repositories e services.

5. **Lógica de negócio em routes/views** (HIGH)
   - Sinais: handlers HTTP calculando totais, decisões de pagamento, lógica de atraso, ramos de validação.
   - Recomende: mover a orquestração para controllers/services.

6. **Exposição de dados sensíveis** (HIGH)
   - Sinais: API retorna senhas, chaves secretas, flags de debug, dados de cartão, stack traces.
   - Recomende: serializers explícitos e respostas de health/debug sanitizadas.

7. **Uso de API obsoleta** (MEDIUM)
   - Sinais: APIs obsoletas pelo framework/runtime, como `Model.query.get()` do SQLAlchemy em versões modernas.
   - Recomende: usar o equivalente moderno, por exemplo `db.session.get(Model, id)`.

8. **Queries N+1** (MEDIUM)
   - Sinais: queries dentro de loops para registros relacionados.
   - Recomende: joins/eager loading/queries em lote.

9. **Validação de entrada ausente** (MEDIUM)
   - Sinais: acesso direto ao body sem checagens de tipo/intervalo/schema.
   - Recomende: helpers/schemas de validação próximos da fronteira da request.

10. **Estado mutável global** (MEDIUM)
    - Sinais: caches/contadores/conexão de BD compartilhada em nível de módulo e mutada entre requests.
    - Recomende: injeção de dependência, BD com escopo de request, serviço de cache explícito.

11. **Criptografia/armazenamento de senha fracos** (CRITICAL)
    - Sinais: MD5/base64/hashes customizados/senhas em texto puro.
    - Recomende: hash de senha com Werkzeug/PBKDF2/bcrypt/argon2.

12. **Valores mágicos e nomes ruins** (LOW)
    - Sinais: limites sem nome, tokens falsos, variáveis abreviadas, listas duplicadas de status/categorias.
    - Recomende: constantes e nomes descritivos.
