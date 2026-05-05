# Diretrizes MVC

## Limites alvo

- **Models/Repositories**: schema do banco de dados, modelos de ORM, queries de persistência, mapeamento de linhas brutas para dicionários de domínio.
- **Controllers**: orquestração da aplicação, regras de negócio, decisões de validação, fluxos em nível de transação, escolha de chamadas de services.
- **Views/Routes**: registro de rotas HTTP, parsing de request, serialização de resposta/status codes.
- **Services**: operações de domínio reutilizáveis e efeitos colaterais como notificação, pagamento, hash de senha e relatórios.
- **Config/Settings**: variáveis de ambiente, defaults, portas, feature flags, origem dos segredos.
- **Middlewares**: error handlers, request logging, barreiras de auth, headers de CORS/segurança.

## Regras

- Routes devem permanecer enxutas.
- Controllers não devem conhecer globais do framework, salvo quando a convenção da stack tornar isso inevitável.
- Models/repositories não devem retornar segredos, salvo quando explicitamente exigido por um service interno.
- Nunca concatene input do usuário em queries de banco de dados.
- Mantenha URLs de endpoints e contratos de resposta existentes estáveis durante refatorações.
- Use injeção de dependência ou composition roots para BD/services quando prático.
- Centralize constantes de validação repetidas, como statuses, categorias e prioridades.
