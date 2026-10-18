# Produção e segurança — bilheteria de shows

**Status:** planejamento para um MVP estático clicável; não é uma autorização de lançamento.

**Idioma e contexto:** português do Brasil, Brasil/BRL, venda online de ingressos para shows ao vivo.

> **Regra de leitura.** Tudo marcado como **FATO** é uma referência externa ou uma restrição já dada pelo produto. Tudo marcado como **PROPOSTA** é uma decisão de produto/arquitetura sugerida para validação. A proposta não substitui revisão jurídica, contratual, de segurança, do adquirente ou do provedor de pagamentos.

## 1. Escopo e limites

### 1.1 Premissas provisórias

- **PROPOSTA:** operar inicialmente no Brasil, exibir valores em BRL e ter um único organizador.
- **PROPOSTA:** vender lotes e setores de acesso geral, sem mapa de assentos numerados.
- **PROPOSTA futura:** Pix e cartão poderão ser habilitados por um provedor de pagamentos; nenhum provedor foi escolhido neste documento.
- **MVP atual:** apenas interface estática e clicável, publicável na Vercel pelo usuário; o deploy não foi realizado nesta entrega. Não haverá integração real com pagamento, coleta efetiva de dados pessoais, credencial de usuário, ingresso utilizável, QR Code de produção, estoque concorrente ou check-in real.
- **FATO regulatório:** a LGPD alcança tratamento de dados pessoais inclusive em meios digitais e pode se aplicar à oferta de bens ou serviços a pessoas no território nacional.[1] No MVP, portanto, textos, telas e contratos devem ser desenhados para não simular que dados foram processados quando não foram.
- **FATO de segurança:** a ANPD recomenda medidas técnicas e administrativas e informa que a segurança deve ser considerada desde a concepção do produto até sua execução.[2]

### 1.2 O que este documento resolve

1. Jornada e estados que a interface deve tornar compreensíveis.
2. Fronteira entre protótipo e sistema transacional de produção.
3. Arquitetura-alvo recomendada, sem compromisso de stack.
4. Invariantes de estoque, pagamento, ingresso, reembolso e check-in.
5. Controles mínimos de segurança, privacidade, acessibilidade, operação e auditoria.
6. Portões de liberação e decisões que dependem de descoberta adicional.

### 1.3 O que fica fora do MVP

- Repasse, split de pagamentos, onboarding/KYC ou conciliação entre vários organizadores.
- Assentos numerados, meia-entrada juridicamente validada ou regras específicas de cada evento.
- Integração com Pix, cartão, antifraude, e-mail, SMS, storage, scanner ou ERP.
- Conta de cliente real, login, recuperação de senha e painel de organizador.
- QR Code/ código de ingresso que possa ser aceito na portaria.
- Operação offline de portaria.

## 2. Jornada de compra e linguagem de estados

A interface deve permitir que uma pessoa entenda **o que está comprando, quanto pagará, em que estado está a tentativa e como obter ajuda**, sem depender de conhecimento de pagamentos.

### 2.1 Fluxo principal

`Busca → Evento → Quantidade e meia-entrada → Total final → Checkout convidado ou conta → Pagamento → Resultado → Recuperar ingresso → Suporte/reembolso`

| Etapa | Conteúdo obrigatório na experiência | Estado que não pode ficar ambíguo |
|---|---|---|
| Busca | Nome, data, cidade/local, faixa de preço quando disponível e ação de detalhes | Nenhum evento deve parecer disponível se a disponibilidade for apenas ilustrativa. |
| Evento | Artista/show, data e hora, local, classificação/avisos quando aplicáveis, lotes/setores, política de troca/cancelamento e suporte | “Disponível”, “últimas unidades”, “esgotado” e “a confirmar” são estados distintos. |
| Quantidade | Seletor com limite por pedido, preço unitário, lote vigente e opção de meia-entrada somente quando o evento tiver regra configurada | A meia-entrada não deve ser apresentada como desconto incondicional; deve indicar que haverá comprovação conforme a política aplicável. |
| Total | Ingressos, taxa, descontos, impostos ou outros componentes aplicáveis e **total em BRL antes do pagamento** | O botão final repete valor, moeda e quantidade; nenhuma taxa aparece apenas depois. |
| Identificação | “Continuar como convidado” e “Criar/usar conta” podem existir como opções separadas | A conta não deve ser obrigatória apenas para recuperar um pedido, salvo decisão justificada. |
| Pagamento | Redirecionamento ou checkout hospedado do provedor quando houver integração | A página não coleta PAN/CVC no MVP e não deve fingir aprovação. |
| Resultado | Pendente, aprovado, recusado, expirado, cancelado ou erro técnico, com próxima ação | “Pedido criado” não é “pagamento aprovado”; “pagamento pendente” não é ingresso liberado. |
| Recuperação | E-mail/link seguro ou área autenticada para localizar o pedido, com suporte visível | Não exibir ingresso de outra pessoa por e-mail, ID previsível ou URL compartilhada. |
| Pós-venda | Política de cancelamento/reembolso, canal de suporte, prazo de resposta a definir e trilha do pedido | A política exibida deve ser a do evento/organizador vigente no momento da compra. |

### 2.2 Estados de pagamento propostos

- `nao_iniciado`: carrinho sem tentativa criada.
- `aguardando_pagamento`: pedido criado e reserva ativa; usuário precisa concluir o checkout.
- `pendente`: provedor recebeu a tentativa, mas o resultado ainda não é final (por exemplo, confirmação assíncrona).
- `aprovado`: confirmação verificável do provedor, valor/moeda conferidos e pedido elegível para emissão.
- `recusado`: tentativa não autorizada; liberar a reserva conforme política e permitir nova tentativa sem duplicar pedido.
- `expirado`: prazo da tentativa ou da reserva terminou; informar se será necessário refazer a compra.
- `cancelado/reembolsado`: operação pós-venda concluída, com motivo e valor registrados.
- `erro_tecnico`: falha sem afirmar que o pagamento falhou; encaminhar para consulta/reconciliação.

**PROPOSTA de copy:** “Seu pagamento ainda está sendo confirmado. Não tente pagar novamente até verificarmos o status.” Isso evita cobrança duplicada quando o navegador perde a resposta.

## 3. Fronteira MVP → produção

| Tema | MVP estático | Produção obrigatória |
|---|---|---|
| Catálogo | Dados fictícios e links navegáveis | API/backend com dados versionados, validação de status e autorização por organizador. |
| Preço | Estados visuais | Cálculo no servidor com inteiro em centavos, moeda explícita, lote e taxa versionados. |
| Estoque | Simulação visual | Reserva atômica e server-authoritative com TTL, liberação segura e reconciliação. |
| Pagamento | Tela de exemplo, sem credenciais | Checkout hospedado/tokenizado, webhook autenticado conforme o provedor, idempotência e conciliação. |
| Identidade | Sem conta real | Sessão, conta opcional, recuperação segura e MFA para funções privilegiadas. |
| Ingresso | Não utilizável | Token opaco aleatório, emissão somente após regra de pagamento e revogação transacional. |
| Portaria | Não implementada | Check-in online, operação segura e teste de repetição; offline é decisão futura, não implícita. |
| Dados pessoais | Não coletados | Inventário de tratamento, finalidade/base legal, retenção, acesso, eliminação e resposta a direitos. |
| Operação | Sem SLO declarado | Monitoramento, alertas, backup/restauração, incidentes, reconciliação e suporte. |

## 4. Arquitetura-alvo (proposta, não compromisso)

```text
Navegador
   │ HTTPS
Frontend web (Vercel)
   │ API autenticada / endpoints de compra
Backend transacional separado (.NET ou TypeScript)
   ├─ Banco relacional: eventos, preços, reservas, pedidos, pagamentos, ingressos
   ├─ Fila/worker: outbox, e-mail, reconciliação, expiração de reserva
   ├─ Provedor de pagamentos: checkout hospedado/tokenização
   ├─ Scanner web futuro: endpoint de check-in
   └─ Observabilidade: logs estruturados, métricas, alertas e auditoria
```

### 4.1 Decisões de desenho

- **PROPOSTA:** manter frontend e backend transacional separados. Vercel hospeda a experiência; o backend mantém transações, segredos, webhooks e concorrência fora do navegador.
- **PROPOSTA:** usar .NET ou TypeScript no backend conforme equipe e operação; a escolha exige prova de concorrência, suporte e segurança, não preferência abstrata.
- **PROPOSTA:** banco relacional como autoridade para disponibilidade e estado do pedido; cache acelera leitura, mas não decide estoque.
- **PROPOSTA:** outbox transacional registra “evento a publicar” na mesma transação que altera o pedido. Worker pode repetir com segurança e marcar a entrega, sem depender de uma chamada externa dentro da transação.
- **PROPOSTA:** toda rota sensível deve buscar o objeto por ID e verificar organizador/evento/usuário no servidor. O OWASP API Security Top 10 chama atenção para autorização por objeto, autenticação, consumo irrestrito de recursos e fluxos sensíveis como comprar ingressos.[7]

### 4.2 Entidades mínimas

`Organizer`, `Event`, `Venue`, `Lot`, `TicketType`, `Order`, `OrderItem`, `Reservation`, `PaymentAttempt`, `WebhookReceipt`, `Ticket`, `Refund`, `CheckIn`, `SupportCase`, `AuditEntry`.

Cada registro deve ter identificador não previsível para exposição externa, timestamps em UTC, estado controlado e referências suficientes para auditoria. Preço e total devem ser armazenados como valor inteiro em centavos + moeda, e não recalculados a partir de texto formatado.

## 5. Estoque, reserva e emissão

### 5.1 Invariantes

1. Nunca confirmar mais unidades que a capacidade publicada do lote/setor.
2. A quantidade aceita vem do backend; o navegador não escolhe preço, disponibilidade ou desconto final.
3. Uma reserva tem `expires_at`, pedido proprietário e estado (`ativa`, `convertida`, `liberada`, `cancelada`).
4. A criação ou extensão de reserva deve ser atômica: transação, bloqueio/condição adequada e verificação de capacidade no mesmo caminho.
5. Expiração é idempotente: executar o worker duas vezes não libera duas vezes nem reduz estoque abaixo de zero.
6. Pagamento aprovado não pode emitir ingresso para reserva já liberada sem uma política explícita de recuperação.
7. A emissão é uma operação única e auditável; uma repetição do webhook não cria segundo ingresso.

### 5.2 TTL e pagamento tardio

**PROPOSTA:** reservar por TTL curto configurável, exibindo cronômetro apenas se ele representar o relógio do servidor. O valor exato depende do provedor, comportamento de Pix/cartão, suporte e capacidade do evento; não fixar prazo neste documento.

Antes de produção, escolher e testar uma política para “pagamento chegou depois da reserva”: (a) rejeitar/reembolsar automaticamente; (b) recolocar estoque e tentar realocar; ou (c) manter fila manual. A escolha deve considerar valor, confirmação do provedor, prevenção de oversell e comunicação ao cliente. Nunca assumir que “aprovado” resolve a disputa de estoque.

### 5.3 Check-in

**PROPOSTA:** token do ingresso é aleatório, opaco, sem nome, CPF, e-mail ou outros dados pessoais; o servidor resolve o token e retorna apenas o mínimo necessário à portaria. Não usar ID sequencial, hash de e-mail ou QR contendo PII.

O check-in deve ser uma transação atômica: “válido e não usado” → “usado em data/hora, operador e ponto”. Se a resposta se perder, repetir a mesma operação com sua chave idempotente deve devolver o resultado original, permitindo ao operador distinguir confirmação recuperada de uma nova tentativa de entrada. Uma leitura distinta do mesmo ingresso retorna “já utilizado” e não admite entrada duas vezes. Consulta pública de autenticidade não pode consumir o ingresso; somente a operação autorizada de portaria faz a baixa. Modo offline fica fora desta versão; um scanner sem conectividade exige desenho separado de sincronização e resolução de conflitos.

## 6. Pagamentos e pós-venda

### 6.1 Integração segura

- **PROPOSTA:** usar checkout hospedado ou tokenização do provedor, mantendo PAN/CVC fora do backend próprio. Isso reduz exposição, mas **não elimina automaticamente** obrigações de segurança, escopo PCI, dependências do site ou responsabilidades contratuais.
- **FATO:** PCI DSS é uma linha de base de requisitos técnicos e operacionais para proteger dados de pagamento e alcança entidades que armazenam, processam, transmitem ou podem impactar a segurança do ambiente de dados de cartão.[8]
- **FATO:** o FAQ 1588 do PCI SSC esclarece que o critério específico de elegibilidade SAQ A sobre ataques de scripts aplica-se à página que incorpora formulário/página de pagamento de terceiro (por exemplo, iframe), e não à página que apenas redireciona ou terceiriza integralmente o pagamento. Isso não dispensa os demais critérios e obrigações; o questionário aplicável deve ser confirmado com a entidade que recebe a avaliação.[9]
- **PROPOSTA:** preferir redirecionamento para página hospedada enquanto a escolha do provedor e o assessment PCI não autorizarem outra modalidade. Validar domínio, retorno, CSP, scripts de terceiros, contrato e questionário aplicável com o adquirente/provedor/QSA.

### 6.2 Webhooks e idempotência

1. Receber o corpo bruto quando o provedor exigir isso para autenticação.
2. Validar autenticidade **segundo a documentação do provedor escolhido**; não inventar “assinatura genérica”, algoritmo, cabeçalho ou campo.
3. Registrar o evento externo, identificador, tipo, timestamp recebido e hash/corpo mínimo necessário, com proteção contra replay conforme o provedor.
4. Deduplicar por uma chave do provedor + tipo/versão; a transição de negócio deve ser idempotente.
5. Conferir servidor-servidor: pedido interno, valor, moeda, referência, status e evento esperado.
6. Responder rapidamente e processar trabalho pesado no worker; retentar com backoff seguro.
7. Tratar eventos duplicados, fora de ordem e atrasados; o estado final deve depender de uma máquina de estados válida, não da ordem de chegada.
8. Consultar/reconciliar o provedor para `pendente`/`erro_tecnico`, sem marcar como aprovado apenas pelo retorno do navegador.

### 6.3 Cancelamento, reembolso e chargeback

- Cancelamento de evento deve congelar novas vendas, informar clientes, invalidar ingressos quando aplicável e iniciar fluxo de reembolso conforme política e regra do provedor.
- Reembolso deve ser autorizado por função adequada, registrar motivo, valor, operador e referência externa, e ser idempotente.
- Um ingresso cancelado/reembolsado não pode passar no check-in.
- Chargeback/disputa deve gerar caso de conciliação; não apagar pedido ou auditoria para “corrigir” o saldo.
- **DEPENDÊNCIA:** regras de consumidor, meia-entrada, prazo de arrependimento/cancelamento, taxas e responsabilidade do organizador precisam de revisão jurídica local antes de venda real.

## 7. Segurança, privacidade e confiança

### 7.1 Baseline de aplicação

**FATO:** o OWASP ASVS fornece uma base para testar controles técnicos de segurança e requisitos para desenvolvimento seguro; no momento da pesquisa a página aponta a versão estável 5.0.0.[3] Usar referências versionadas, por exemplo `v5.0.0`, e registrar exceções.

**PROPOSTA de controles P0:**

- TLS em produção, HSTS após confirmar domínio/certificados e nenhuma credencial em código, logs ou frontend.
- Segredos em secret manager/variáveis protegidas, rotação e acesso por função; nunca em repositório ou bundle do navegador.
- Sessões com cookies `Secure`, `HttpOnly`, `SameSite` apropriado, expiração/rotação e invalidação no logout; evitar tokens de sessão em `localStorage`. A orientação do OWASP destaca que o sequestro de sessão pode equivaler à personificação e recomenda atributos seguros de cookie.[4]
- CSRF para toda operação mutável autenticada por cookie, usando proteção nativa do framework ou tokens; não usar `GET` para alterar estado. O OWASP recomenda tokens/defesas equivalentes e explicita que XSS pode derrotar mitigação de CSRF.[5]
- XSS: escaping contextual padrão, sanitização somente quando realmente houver HTML permitido, validação de URL, revisão de “escape hatches” e CSP testada. O OWASP alerta que frameworks modernos ajudam, mas uso inseguro e conteúdo não confiável ainda pode causar XSS.[6]
- Autorização server-side por usuário, organizador, evento e função; negar por padrão. Funções administrativas e de suporte devem ter MFA, menor privilégio, reautenticação para ações de alto impacto e trilha de auditoria.
- Rate limit e proteção contra abuso em login, recuperação, consulta de pedido, reserva, cupom, webhook e scanner. Limites não substituem capacidade atômica.
- Dependências fixadas/atualizadas, SAST/DAST quando possível, revisão de configuração e teste de restauração.

### 7.2 PII, LGPD e recuperação de pedido

- **FATO:** pela LGPD, dado pessoal é informação relacionada a pessoa natural identificada ou identificável; tratamento inclui coleta, acesso, armazenamento, eliminação e outras operações.[1]
- **PROPOSTA:** coletar no checkout somente o necessário para executar a compra, emitir o ingresso, suporte e obrigações aplicáveis. Separar comunicações opcionais de marketing da transação.
- **PROPOSTA:** manter mapa de dados: campo, finalidade, base legal a validar, controlador/operador, destinatário, região, retenção e forma de eliminação/anonimização.
- **PROPOSTA:** logs não armazenam PAN/CVC, token de sessão, link integral de recuperação, QR/token de ingresso ou payload pessoal desnecessário. Mascarar e limitar acesso; definir retenção por classe de log.
- **PROPOSTA:** link de recuperação é aleatório, de uso limitado/expiração curta, não expõe PII na URL além do necessário, exige rate limit e pode pedir segundo fator contextual (por exemplo, e-mail + código). Para conta, exigir autenticação e autorização.
- **DEPENDÊNCIA:** política de privacidade, canal do titular, prazos de retenção, solicitação de acesso/correção/eliminação/portabilidade e resposta a incidente devem ser aprovados com jurídico/encarregado. Não prometer eliminação quando houver obrigação de retenção; separar dado operacional, financeiro, antifraude e auditoria.
- **FATO de acessibilidade:** WCAG 2.2 é uma recomendação W3C, com critérios testáveis e princípios de conteúdo perceptível, operável, compreensível e robusto.[10] **PROPOSTA:** testar teclado, foco, contraste, leitor de tela, mensagens de erro, contagem de quantidade, status de pagamento e QR ilustrativo sem depender apenas de cor.

### 7.3 Modelo de ameaça resumido

| Ameaça | Impacto | Controle proposto | Evidência antes de produção |
|---|---|---|---|
| Oversell por concorrência | Venda acima da capacidade | Transação atômica, TTL, testes concorrentes | Teste reproduzível com capacidade pequena e saldo correto. |
| Pedido de outro cliente | Exposição de ingresso/PII | Autorização por objeto, link aleatório, rate limit | Teste de troca de IDs/tokens e retorno sem vazamento. |
| Webhook forjado/repetido | Emissão ou reembolso indevido | Validação conforme provedor, dedupe, estado válido | Fixtures do provedor, inválido/duplicado/fora de ordem. |
| XSS em evento/suporte | Roubo de sessão ou ação | Escaping, sanitização, CSP, revisão | DAST/manual e payloads de contexto. |
| Roubo de conta/admin | Acesso a pedidos e dinheiro | MFA, sessão segura, menor privilégio, auditoria | Teste de autorização por papel e recuperação. |
| Script de pagamento comprometido | Exposição de cartão | Checkout hospedado, inventário de scripts, revisão PCI | Confirmação do provedor/QSA e verificação de integridade. |
| PII em observabilidade | Incidente/regulação | Minimização, mascaramento, retenção e acesso | Amostras de logs + consulta de permissões. |
| Abuso de reservas/checkout | Indisponibilidade ou estoque preso | Limites por IP/conta/evento, TTL, fila e alertas | Teste de carga/abuso e recuperação do estoque. |

## 8. Disponibilidade e operação em lançamento

- **PROPOSTA:** tratar lançamento de evento como burst: CDN para conteúdo público, cache sem comprometer disponibilidade, fila/controle de acesso se a descoberta indicar necessidade, banco dimensionado para transações e limites de requisição.
- O caminho de compra deve ter timeout, retry seguro e fallback de leitura; nunca repetir automaticamente uma cobrança sem chave idempotente.
- Monitorar: taxa de erro por endpoint, latência, reservas ativas/expiradas, pedidos por estado, webhooks atrasados/rejeitados, diferença entre provedor e banco, emissão, reembolso, check-in e chamados.
- Ter runbooks para: provedor indisponível, webhook parado, estoque preso, pagamento tardio, evento cancelado, vazamento de token, incidente LGPD e restauração de backup.
- Fazer backup e teste de restauração antes de confiar nele. Disponibilidade e recuperação devem ser objetivos aprovados; não declarar SLA/SLO sem medição e capacidade verificadas.
- Portaria offline **não está incluída**. Se for necessária, deve ter análise específica de ameaça, expiração/rotatividade, fila de sincronização, operação em dois operadores e resolução de conflito.

## 9. Multi-organizador, repasse e split

**PROPOSTA de adiamento:** manter um organizador no primeiro recorte e não desenhar split como se fosse detalhe de implementação. Antes de aceitar múltiplos organizadores, decidir quem é vendedor/controlador, quem responde por consumidor e reembolso, onboarding/KYC, contas de recebimento, conciliação, chargeback, segregação de tenant, permissões de suporte e tributação.

Quando a descoberta justificar multi-tenant, exigir `organizer_id/tenant_id` em todas as entidades e consultas, autorização por função e tenant, testes de isolamento cruzado e trilha de repasse. Não permitir que um ID recebido do navegador escolha o organizador autorizado.

## 10. Portões de produção priorizados

### P0 — bloquear venda real

- Backend server-authoritative para preço, capacidade, pedido e estado.
- Reserva atômica com TTL e testes de concorrência.
- Checkout hospedado/tokenizado escolhido; PAN/CVC fora do sistema; escopo PCI validado com partes competentes.[8][9]
- Webhook autenticado conforme documentação do provedor, idempotente e reconciliável.
- Autorização por objeto/organizador, gestão segura de sessão, MFA privilegiado e CSRF.[3][4][5]
- XSS/CSP, segredos protegidos e controles de API devem passar por revisão específica.[6][7]
- Emissão/revogação de ingresso e check-in online idempotente.
- Política de preço, meia-entrada, cancelamento, reembolso e suporte aprovada.
- Privacidade, retenção, atendimento a titulares e incidente LGPD definidos.[1][2]

### P1 — bloquear experiência insegura ou não operável

- Acessibilidade testada contra WCAG 2.2 como referência.[10]
- Testes da matriz em `CRITERIOS-DE-ACEITE.md` aprovados.
- Observabilidade, alertas, backup/restauração, reconciliação e runbooks exercitados.
- Teste de carga/rajada e plano de suporte do evento.

### P2 — risco controlado antes de escala

- Revisão independente de segurança, dependências, configuração e scripts de terceiros.
- Exercício de cancelamento, reembolso em massa, chargeback e pagamento tardio.
- Limites de abuso ajustados com dados de operação.

### P3 — evolução

- Conta mais completa, assentos, novos métodos, app de scanner e offline.
- Multi-organizador, split e repasse somente após descoberta e testes de isolamento/conciliação.

## 11. Dependências e decisões em aberto

| Dependência/decisão | Por que bloqueia | Dono sugerido | Saída exigida |
|---|---|---|---|
| Provedor de pagamento e modalidade (redirect/iframe/tokenização) | Define webhook, PCI, fraude, UX e reconciliação | Produto + técnico + financeiro | Contrato, documentação e matriz de responsabilidades. |
| Política de pagamento tardio | Evita oversell e surpresa ao cliente | Produto + financeiro | Estados, prazos, reembolso e mensagens aprovados. |
| Regras de meia-entrada | Pode variar por evento e documentação | Organizador + jurídico | Regra exibível e operação de comprovação. |
| Reembolso/cancelamento/chargeback | Define estado de ingresso e caixa | Organizador + financeiro + jurídico | Política pública e runbook. |
| Controlador/operadores e retenção LGPD | Define coleta, acesso e eliminação | Responsável jurídico/encarregado | Registro de tratamento, política e canal. |
| Pico esperado e suporte | Define fila, capacidade e plantão | Produto + operação | Cenário de carga, alertas e escala de atendimento. |
| Necessidade de offline na portaria | Muda segurança e consistência do check-in | Operação do evento | Decisão explícita: online-only ou projeto offline. |
| Multi-organizador/split | Muda identidade, financeiro e isolamento | Produto + financeiro | Discovery aprovado antes de implementar. |

Não há orçamento, prazo, SLO ou capacidade numérica inventados neste documento; esses valores devem vir de dados do evento, fornecedor e operação.

## Sources

[1] https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
[2] https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_seguranca_da_informacao_para_atpps___defeso_eleitoral.pdf/@@display-file/file
[3] https://owasp.org/projects/asvs
[4] https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
[5] https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
[6] https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
[7] https://owasp.org/API-Security/editions/2023/en/0x11-t10
[8] https://www.pcisecuritystandards.org/standards/pci-dss
[9] https://www.pcisecuritystandards.org/faqs/1588
[10] https://www.w3.org/TR/WCAG22
