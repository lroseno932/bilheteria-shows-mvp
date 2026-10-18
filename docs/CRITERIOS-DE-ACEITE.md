# Critérios de aceite — bilheteria de shows

**Status:** critérios para o protótipo estático e para a futura decisão de produção.

**Escopo de referência:** Brasil/BRL, um organizador, lotes/setores de acesso geral, compra online, frontend estático clicável no MVP. Não há backend, pagamento real, coleta de PII, conta, QR utilizável ou scanner nesta etapa.

> **Como usar.** Cada critério tem um resultado observável. Os itens **MVP** validam a experiência sem criar transação real. Os itens **PRODUÇÃO** são portões: não devem ser marcados como concluídos por telas ou mocks. **FATO** identifica uma referência externa; **PROPOSTA** identifica uma decisão de produto/engenharia que ainda precisa de aprovação.

## 1. Convenções

- **Prioridade:** `P0` bloqueia venda segura; `P1` bloqueia experiência/ operação; `P2` reduz risco antes de escala; `P3` evolução.
- **Tipos:** `MVP` = protótipo estático; `PRODUÇÃO` = comportamento do sistema transacional; `SEG` = segurança/privacidade; `A11Y` = acessibilidade; `OPS` = operação.
- **Evidência aceita:** gravação/screenshot para interface; teste automatizado ou manual reproduzível para comportamento; log/auditoria/consulta de banco mascarada para transação; documento aprovado para política/contrato.
- **Não confundir:** “visualiza o estado aprovado” não significa “autorizou um pagamento”; “QR exibido como ilustração” não significa “credencial válida”.

## 2. Critérios propostos para evolução do protótipo

**Cobertura da entrega atual:** esta seção é um checklist de produto, não uma declaração de que todos os itens estão implementados ou aprovados. O recorte entregue e os testes efetivamente executados estão em `README.md` e `VERIFICACAO.md`. Não foram implementados nesta versão estados de disponibilidade por evento (MVP-003/005), evento sem opção de meia (parte de MVP-008), cupons/descontos e detalhamento de cada tipo no resumo (parte de MVP-009), alternativa de conta (parte de MVP-011), erro técnico de pagamento (parte de MVP-014) nem recuperação de pedido por formulário/link (MVP-017 e parte de MVP-018). Auditoria completa de acessibilidade, zoom e conexão lenta também está pendente. Todos os controles de produção abaixo são futuros.

A interface permite explorar os demais caminhos de demonstração sem os transformar em transações reais.

### 2.1 Descoberta e detalhe do evento

| ID | Prioridade | Critério verificável | Evidência |
|---|---:|---|---|
| MVP-001 | P1 | A página inicial permite iniciar a busca e navegar para pelo menos um evento fictício sem quebrar o fluxo. | Clique gravado/roteamento verificável. |
| MVP-002 | P1 | O card e o detalhe exibem nome do show, data, horário, local, cidade, preço inicial ou “a definir”, lotes/setores e chamada para compra. | Captura em viewport móvel e desktop. |
| MVP-003 | P1 | Disponibilidade fictícia é visualmente distinguida entre `disponível`, `últimas unidades`, `esgotado` e `a confirmar`; nenhum texto sugere que o protótipo consultou estoque real. | Caminho para cada estado + texto de protótipo. |
| MVP-004 | P1 | A tela de evento mostra “taxas e total antes do pagamento” e link para suporte/política, ainda que a política seja conteúdo de exemplo. | Captura do detalhe completo. |
| MVP-005 | P1 | O botão de comprar é desabilitado ou apresenta aviso de protótipo quando não existe disponibilidade fictícia. | Teste com evento esgotado. |

### 2.2 Quantidade, lotes e meia-entrada

| ID | Prioridade | Critério verificável | Evidência |
|---|---:|---|---|
| MVP-006 | P0 | O usuário consegue aumentar/diminuir quantidade por tipo de ingresso, com mínimo zero e limite de demonstração explícito. | Fluxo com 0, 1, limite e tentativa acima. |
| MVP-007 | P0 | A seleção mostra lote/setor, preço unitário em BRL e subtotal; alteração de quantidade atualiza o resumo sem recarregar de forma confusa. | Captura antes/depois. |
| MVP-008 | P0 | Meia-entrada aparece somente como opção configurada no evento e informa que comprovação/regras dependem da política aplicável; não promete elegibilidade universal. | Captura do texto e estado sem meia. |
| MVP-009 | P1 | O resumo distingue inteira, meia-entrada, taxa, desconto e total; valores usam `R$` e duas casas decimais quando aplicável. | Casos com e sem taxa/desconto. |
| MVP-010 | P1 | O total final é apresentado antes do CTA de continuidade, sem “taxa surpresa” na etapa seguinte. | Gravação do caminho completo. |

### 2.3 Checkout convidado, conta e pagamento simulado

| ID | Prioridade | Critério verificável | Evidência |
|---|---:|---|---|
| MVP-011 | P1 | A interface oferece “continuar como convidado” e uma alternativa de conta/identificação apenas como simulação; não solicita senha real. | Fluxo e texto de não produção. |
| MVP-012 | P0 | Nenhuma tela do MVP solicita PAN, CVC, senha, token de sessão ou documento real; campos sensíveis estão ausentes ou claramente desativados como demonstração. | Inspeção manual e busca no bundle/código. |
| MVP-013 | P0 | O CTA de pagamento leva a uma tela simulada identificada como “pagamento de demonstração”, nunca a um provedor real. | URL/roteamento + screenshot. |
| MVP-014 | P1 | O protótipo possui caminhos navegáveis para `pendente`, `aprovado`, `recusado`, `expirado` e `erro técnico`. | Matriz de cenários e gravação. |
| MVP-015 | P0 | A mensagem de aprovado não afirma que um ingresso real foi emitido; a mensagem de pendente orienta a não repetir o pagamento; a recusada orienta nova tentativa sem garantir cobrança. | Textos revisados por produto. |
| MVP-016 | P1 | O resumo em todas as telas críticas repete evento, quantidade e total em BRL, reduzindo erro de contexto. | Capturas das telas. |

### 2.4 Recuperação, suporte e reembolso ilustrativos

| ID | Prioridade | Critério verificável | Evidência |
|---|---:|---|---|
| MVP-017 | P1 | Existe tela de “recuperar pedido/ingresso” que explica que o recurso é demonstrativo e não envia e-mail real. | Captura e texto. |
| MVP-018 | P1 | O fluxo demonstra pedido localizado, não localizado e suporte, sem exibir PII real ou ingresso reutilizável. | Três estados navegáveis. |
| MVP-019 | P1 | Existe caminho de política de cancelamento/reembolso e contato de suporte, sem inventar prazos, direitos ou provedor. | Conteúdo revisado. |
| MVP-020 | P0 | Qualquer QR, código ou ingresso visualmente apresentado tem marcação inequívoca de “exemplo — não válido para entrada” e não contém PII. | Inspeção visual e payload. |

### 2.5 Qualidade de interface e acessibilidade

| ID | Prioridade | Critério verificável | Evidência |
|---|---:|---|---|
| MVP-021 | P1/A11Y | O fluxo completo funciona somente com teclado: busca, filtros, quantidade, seleção, CTA, modais e mensagens. | Gravação/planilha de teclas. |
| MVP-022 | P1/A11Y | Foco visível, ordem de foco coerente, rótulos associados, mensagens de erro compreensíveis e estados não dependem apenas de cor. | Checklist + captura. |
| MVP-023 | P1/A11Y | O design usa WCAG 2.2 como referência; a especificação W3C apresenta critérios testáveis e os princípios perceptível, operável, compreensível e robusto.[10] | Resultado de auditoria manual/automatizada, sem alegar conformidade automática. |
| MVP-024 | P1 | Layout e texto são utilizáveis em viewport móvel, zoom e conexão lenta simulada, sem esconder total ou CTA. | Capturas e teste de zoom. |
| MVP-025 | P1 | O texto deixa claro quando uma informação é fictícia, futura ou depende de escolha do provedor/organizador. | Revisão editorial. |

## 3. Portões de produção (não implementados pelo MVP)

### 3.1 Catálogo, preço e autorização

| ID | Prioridade | Critério de aceite de produção | Evidência mínima |
|---|---:|---|---|
| PROD-001 | P0 | O backend é a autoridade para evento ativo, lote, capacidade, preço, taxa, moeda e limite por pedido; o cliente não consegue alterar o total por payload adulterado. | Teste de API + logs de decisão. |
| PROD-002 | P0 | O preço é calculado em centavos inteiros com moeda explícita e fica registrado no item do pedido; alterações futuras não reescrevem histórico. | Consulta mascarada + teste de alteração de lote. |
| PROD-003 | P0/SEG | Toda leitura/escrita verifica autorização por usuário, organizador/evento e função no servidor; IDs trocados não acessam pedido, ingresso ou painel de outro escopo. OWASP destaca autorização por objeto e por função como riscos centrais de APIs.[7] | Testes negativos de IDOR/BOLA e revisão de rotas. |
| PROD-004 | P1 | Limites de quantidade, cupom, reserva, recuperação e scanner têm rate limit e comportamento observável; abuso não cria estoque ou custo ilimitado. | Teste de limite e alerta. |

### 3.2 Reserva e concorrência

| ID | Prioridade | Critério de aceite de produção | Evidência mínima |
|---|---:|---|---|
| PROD-005 | P0 | Para capacidade N, N+1 compras concorrentes nunca confirmam mais de N unidades. | Teste repetível com banco limpo. |
| PROD-006 | P0 | Reserva grava proprietário, quantidade, lote, `expires_at` e estado; expiração e repetição do worker são idempotentes. | Teste com duas execuções e saldo final. |
| PROD-007 | P0 | O relógio de expiração é server-authoritative; o contador do frontend é apenas apresentação e não prolonga reserva. | Adulteração do relógio/cliente. |
| PROD-008 | P0 | Uma reserva liberada não vira ingresso por webhook tardio sem política explícita de pagamento tardio; o resultado é aprovado/reembolsado/encaminhado conforme regra documentada. | Casos tardio antes/depois de nova venda. |
| PROD-009 | P1 | O sistema registra e alerta estoque preso, reserva negativa, divergência de capacidade e worker atrasado. | Métrica, alerta e runbook exercitados. |

### 3.3 Pagamento e webhook

| ID | Prioridade | Critério de aceite de produção | Evidência mínima |
|---|---:|---|---|
| PROD-010 | P0 | PAN/CVC não entram no backend, logs, analytics ou banco; o fluxo usa checkout hospedado/tokenização conforme contrato e documentação do provedor. PCI DSS é baseline para proteger dados de pagamento, e seu escopo alcança quem pode impactar o ambiente de dados de cartão.[8] | Revisão de tráfego, logs, arquitetura e contrato. |
| PROD-011 | P0 | O escopo PCI e o questionário aplicável são confirmados com adquirente/provedor/QSA; não se declara “fora do PCI” apenas por usar terceiro. | Registro de decisão e responsabilidade compartilhada. |
| PROD-012 | P0 | O endpoint valida autenticidade conforme a documentação exata do provedor, sem algoritmo/cabeçalho inventado, e preserva corpo bruto quando exigido. | Fixture oficial ou teste de integração controlado. |
| PROD-013 | P0 | Repetir o mesmo webhook não duplica cobrança, pedido, ingresso, e-mail de aprovação ou reembolso. | Replay de evento e evidência de uma transição. |
| PROD-014 | P0 | Eventos fora de ordem, pendentes, recusados, cancelados e atrasados levam a estados válidos; retorno do navegador não substitui confirmação servidor-servidor. | Matriz de eventos e consulta final. |
| PROD-015 | P0 | Pedido só muda para aprovado quando referência, valor, moeda e status esperados conferem; divergência fica em erro/reconciliação. | Payloads alterados e logs sem segredo. |
| PROD-016 | P1 | Retentativas têm backoff e não executam efeito externo duplicado; outbox registra entrega e falha. | Teste de timeout/retry. |
| PROD-017 | P1 | Reconciliação consulta tentativas pendentes/erro técnico e produz relatório de divergências, sem apagar histórico. | Relatório e caso de divergência. |

O FAQ 1588 do PCI SSC aplica o critério específico SAQ A sobre ataques de scripts à página com pagamento embutido de terceiro (por exemplo, iframe), não a simples redirecionamento ou terceirização integral. Os demais requisitos e critérios continuam sujeitos ao escopo real; confirmar a modalidade e o questionário com provedor/adquirente ou entidade responsável.[9]

### 3.4 Ingresso, recuperação e check-in

| ID | Prioridade | Critério de aceite de produção | Evidência mínima |
|---|---:|---|---|
| PROD-018 | P0 | Ingresso só é emitido após regra de pagamento aprovada e pedido consistente; retries não emitem duplicata. | Teste de webhook duplicado. |
| PROD-019 | P0/SEG | QR/token é opaco, aleatório, não previsível e não contém PII; logs e URLs não expõem o valor integral. | Inspeção de token, logs e resposta. |
| PROD-020 | P0/SEG | Recuperação exige link/token aleatório com expiração/uso limitado, rate limit e autorização; ID previsível ou e-mail isolado não localiza ingresso de terceiro. | Teste de enumeração e expiração. |
| PROD-021 | P0 | Check-in é atômico e one-time: primeira validação registra evento/operador; retry com a mesma chave idempotente recupera o resultado original, e nova leitura distinta retorna “já utilizado”, sem segunda entrada. | Duas requisições concorrentes + retry após timeout. |
| PROD-022 | P0 | Cancelamento/reembolso revoga ingresso de forma transacional e impede check-in; a auditoria permanece. | Cenário aprovado → reembolsado → scanner. |
| PROD-023 | P1 | Operação online-only é explícita; qualquer requisito offline abre projeto separado de sincronização/conflito. | Decisão de operação assinada. |

### 3.5 Segurança de aplicação e acesso privilegiado

| ID | Prioridade | Critério de aceite de produção | Evidência mínima |
|---|---:|---|---|
| SEG-001 | P0 | A equipe referencia e versiona o OWASP ASVS; a página do projeto o descreve como base para testar controles técnicos e desenvolvimento seguro, apontando versão estável 5.0.0 no momento da pesquisa.[3] | Checklist ASVS com exceções e revisão. |
| SEG-002 | P0 | Sessões usam cookies seguros (`Secure`, `HttpOnly`, `SameSite` conforme necessidade), expiram/rotacionam e são invalidadas em logout/comprometimento; tokens não ficam em `localStorage` sem justificativa. OWASP alerta que sequestro de sessão pode personificar o usuário.[4] | Inspeção de headers + testes de sessão. |
| SEG-003 | P0 | Operações mutáveis autenticadas por cookie têm CSRF nativo/token/defesa equivalente; `GET` não altera estado. OWASP recomenda proteção nas operações que alteram estado e observa que XSS pode vencer defesas CSRF.[5] | Teste cross-site e rota GET. |
| SEG-004 | P0 | Conteúdo de evento, suporte, cupons e parâmetros é validado/escapado por contexto; HTML permitido é sanitizado; CSP é testada. OWASP recomenda encoding contextual e alerta para “escape hatches” inseguros de frameworks.[6] | Payloads XSS + relatório de CSP. |
| SEG-005 | P0 | MFA é obrigatório para admin, financeiro, suporte privilegiado e operação de check-in quando houver acesso a dados/ação sensível. | Teste de login e recuperação. |
| SEG-006 | P0 | Segredos não aparecem no repositório, bundle, logs, traces ou mensagens de erro; rotação e acesso são auditáveis. | Secret scan + amostras de observabilidade. |
| SEG-007 | P0 | Falha de autorização em objeto, função, propriedade e tenant é testada; resposta não revela existência de pedido de terceiro. | Matriz negativa de permissões. |
| SEG-008 | P1 | Dependências, configuração e endpoints antigos são inventariados e atualizados; APIs públicas têm versão e desativação planejada. | SBOM/inventário + revisão. |

### 3.6 LGPD, privacidade e operação de dados

| ID | Prioridade | Critério de aceite de produção | Evidência mínima |
|---|---:|---|---|
| SEG-009 | P0 | Existe inventário de dados, finalidade, base legal a validar, papéis controlador/operador, compartilhamentos e retenção; LGPD define dado pessoal e tratamento de forma ampla.[1] | Registro de tratamento revisado. |
| SEG-010 | P0 | Coleta é minimizada; marketing é separado do necessário para compra; campos e finalidade aparecem de forma compreensível. | Teste de checkout + política. |
| SEG-011 | P0 | Canal e procedimento para acesso, correção, eliminação/bloqueio e demais direitos aplicáveis estão definidos, com exceções legais avaliadas. | Runbook e evidência de teste. |
| SEG-012 | P0 | Há plano de incidente: detecção, contenção, preservação de evidência, avaliação de risco, comunicação e contato responsável. ANPD destaca medidas de segurança desde concepção e execução.[2] | Exercício de mesa/runbook. |
| SEG-013 | P1 | Logs minimizam PII e secretos, possuem acesso restrito, retenção definida e auditoria de consulta; não registram PAN/CVC ou token de ingresso integral. | Busca em logs e revisão de IAM. |
| SEG-014 | P1 | Backup é criptografado/protegido e restauração é testada; eliminar dado não remove registro financeiro/auditoria sem análise de retenção. | Evidência de restauração e decisão de retenção. |

### 3.7 Acessibilidade, carga e suporte

| ID | Prioridade | Critério de aceite de produção | Evidência mínima |
|---|---:|---|---|
| A11Y-001 | P1 | Compra, pagamento pendente, recuperação e suporte funcionam com teclado, foco visível, leitor de tela e mensagens associadas. | Teste manual e ferramenta assistiva. |
| A11Y-002 | P1 | Erros não dependem somente de cor; status têm texto/semântica; zoom e viewport móvel não ocultam total/CTA. | Checklist e capturas. |
| OPS-001 | P1 | Existe cenário de rajada com métricas para frontend, API, banco, fila, provedor, reservas e webhooks; não se assume que CDN resolve concorrência de estoque. | Plano/resultado de carga com capacidade real informada. |
| OPS-002 | P1 | Alertas cobrem falhas de webhook, divergência de pagamento, reservas presas, erro de check-in, fila parada, saturação e indisponibilidade do provedor. | Alertas disparados em ambiente de teste. |
| OPS-003 | P1 | Suporte consegue distinguir pedido pendente, recusado, expirado, reembolsado e chargeback sem editar banco manualmente. | Runbook e caso de suporte. |
| OPS-004 | P1 | Cancelamento de evento e reembolso em lote têm simulação, autorização, idempotência e comunicação. | Exercício documentado. |

## 4. Matriz de testes obrigatória

| Caso | Pré-condição | Ação | Resultado esperado |
|---|---|---|---|
| Concorrência no último ingresso | Capacidade = 1 | Dois compradores reservam ao mesmo tempo | Um confirma/reserva; outro recebe indisponibilidade; saldo nunca fica negativo. |
| Reserva expirada | Reserva ativa com TTL vencido | Worker roda uma ou várias vezes | Reserva liberada uma vez; pedido não é aprovado por expiração isolada. |
| Duplo clique/refresh | Checkout iniciado | Reenviar mesma requisição com chave idempotente | Uma tentativa de negócio; resposta consistente. |
| Webhook duplicado | Evento aprovado registrado | Reenviar evento idêntico | Sem segundo ingresso/e-mail/refund; auditoria mostra dedupe. |
| Webhook fora de ordem | Evento pendente/cancelado | Enviar eventos em ordem invertida | Máquina de estados rejeita transição inválida ou reconcilia; nunca aprova indevidamente. |
| Webhook inválido | Corpo/cabeçalho adulterado | POST sem autenticidade | Rejeita, não muta pedido e gera alerta controlado. |
| Valor/moeda divergente | Pedido de R$ X BRL | Evento informa valor/moeda diferente | Não aprova; entra em reconciliação/erro. |
| Pagamento tardio | Reserva liberada e estoque possivelmente vendido | Provedor confirma depois | Aplica política documentada; não ocorre oversell silencioso. |
| Recuperação por enumeração | Dois pedidos distintos | Trocar IDs/tokens e repetir | Não revela existência/PII/ingresso de terceiro; rate limit funciona. |
| Check-in repetido | Ingresso válido já usado | Scanner repete após resposta perdida | A mesma chave idempotente recupera a decisão original; nova leitura recebe já utilizado; não permite entrada dupla. |
| Check-in cancelado | Ingresso reembolsado/cancelado | Scanner valida | Rejeitado com motivo operacional mínimo. |
| Autorização cruzada | Usuários/organizadores distintos | Alterar IDs em rotas | 403/404 seguro; nenhum dado do escopo alheio. |
| XSS | Evento/suporte com payload de teste | Renderizar em cada contexto | Texto inerte; CSP/alerta conforme política; sem execução. |
| CSRF | Sessão por cookie | Requisição cross-site mutável | Bloqueada; GET não muda estado. |
| Sessão | Usuário logado | Logout, expiração, rotação e tentativa com cookie antigo | Cookie antigo não autoriza ação. |
| Admin/MFA | Função privilegiada | Login sem segundo fator/alteração sensível | Bloqueia ou exige reautenticação; auditoria registra. |
| PII em logs | Pedido com dados de teste | Executar compra/erro/webhook | Logs mascarados e sem PAN/CVC/token integral. |
| Falha do provedor | Timeout/5xx controlado | Criar/retentar checkout | Usuário não vê aprovado falso; retry não duplica. |
| Restauração | Backup recente | Restaurar ambiente de teste | Dados e invariantes retornam; divergências detectadas. |
| Acessibilidade | Fluxo completo | Teclado, leitor, zoom e mobile | Pode concluir/entender cada estado e erro. |

## 5. Go/no-go

### Não liberar venda real se qualquer item ocorrer

- Preço, capacidade, autorização ou estado forem decididos pelo navegador.
- Não houver teste concorrente de reserva ou houver estoque negativo/oversell.
- Checkout, tokenização, escopo PCI ou responsabilidades do provedor estiverem indefinidos.
- Webhook aceitar evento não autenticado, duplicar efeitos ou aprovar sem conferir valor/moeda.
- Pedido/ingresso de terceiro puder ser obtido por ID, URL, e-mail isolado ou token previsível.
- Admin/financeiro/suporte sensível não tiver MFA, autorização e auditoria.
- Houver PAN/CVC, segredo, sessão ou QR válido em logs/bundle/repositório.
- Política de pagamento tardio, reembolso, cancelamento e chargeback não estiver aprovada.
- Não houver restauração testada, reconciliação e runbook para incidente/provedor.
- A jornada crítica falhar em teclado/leitor/zoom ou esconder custo/estado.

### Pode avançar apenas como protótipo

- Cenários são fictícios e marcados como demonstração.
- Não se coleta PII nem se pede credencial/pagamento real.
- QR/código é inutilizável e explicitamente marcado como exemplo.
- Cada estado é navegável, o total é upfront e suporte/política são localizáveis.
- O artefato não promete disponibilidade, aprovação, segurança absoluta ou conformidade automática.

## 6. Fontes e rastreabilidade

Os critérios legais, de segurança e acessibilidade devem ser rechecados na data de integração, porque versões, FAQs, contratos de provedor e regras de evento mudam. Os números entre colchetes apontam para as fontes oficiais listadas ao final deste documento.

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
