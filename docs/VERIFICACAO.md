# Verificação do protótipo

## Resultado observado

- **7 testes automatizados de integridade estática: aprovados.** Comando: `python3 -m unittest discover -s tests -v`.
- **37 verificações no navegador: aprovadas.** Aplicadas ao HTML real gerado, com interação real de DOM e teclado. Não são testes de backend.
- `node --check src/prototype.js`: sem erro de sintaxe.
- Geração dos dois documentos pelo script de build: concluída.
- Rotas locais `/` e `/agenda/`: HTTP 200, com cabeçalhos de `vercel.json` servidos pelo servidor de prévia.
- Campos `framework`, `buildCommand` e `outputDirectory` conferidos no schema oficial `https://openapi.vercel.sh/vercel.json`. Não foi executado um validador JSON Schema completo.

## Cobertura de navegador

- Catálogo com seis eventos fictícios; filtros por gênero, cidade, mês e busca sem resultados.
- Favoritos e filtragem de favoritos em memória.
- Abertura de show e totais de inteira/meia com taxa explícita.
- Limite de seis ingressos e bloqueio de continuação com zero.
- Campos pessoais demonstrativos somente leitura.
- Pendência inicial sem ingresso; recusa, nova tentativa, expiração e aprovação escolhida pelo usuário.
- Ingresso marcado sem validade, sem QR utilizável.
- Primeira e repetida leitura em simulação local, sem câmera ou validação de servidor.
- Catálogo editorial em 1440px e celular em 390px; agenda em 1440px e celular em 360px.
- Ausência de rolagem horizontal nas telas verificadas e nos diálogos móveis.
- Controles de quantidade e favoritos da agenda com área de pelo menos 44×44px.
- Fechamento de diálogo com Escape.

## Como a prévia foi examinada

O navegador disponível bloqueou o endereço HTTP local. A alternativa foi carregar **os próprios HTMLs gerados**, em fragmentos, em documentos isolados de uma aba de navegador. Foi usada uma navegação limpa para cada documento, evitando a reutilização de vínculos JavaScript globais. Isso permite verificar composição, DOM e interações, **mas não é um teste integrado dos cabeçalhos HTTP da Vercel**.

O servidor local foi testado separadamente por HTTP, e o hash CSP foi comparado ao JavaScript real por teste automatizado. Uma tentativa de instalar um navegador local não concluiu; foi abandonada em favor do navegador disponível. Nenhum resultado de execução local ausente foi substituído por saída inventada.

## Inspeção visual

As duas composições foram abertas e inspecionadas em desktop e celular. Foi corrigida a disputa de espaço entre o favorito e o preço da agenda no desktop, e ampliados alvos de toque. Escolha inicial: descoberta editorial para um catálogo curto; agenda para comparação rápida de datas.

Autoavaliação estética, não uma métrica de segurança: **1/10 de sinais genéricos**, atribuído ao fallback de fonte sans local para preservar o funcionamento sem rede. Não há gradiente tecnológico, estatísticas falsas, depoimentos, urgência artificial ou cartões genéricos de funcionalidades; os cartões representam eventos do catálogo.

## O que não foi verificado ou implementado

- Deploy na conta Vercel do usuário ou funcionamento no domínio publicado.
- Backend, banco, reserva real, concorrência de estoque, expiração de servidor ou assentos.
- Integração de pagamento, antifraude, assinatura/autenticação de webhook, reembolso ou conciliação.
- Sessões reais, RBAC, isolamento entre organizadores, MFA, ticket/QR válido ou check-in atômico.
- Entrega de e-mail, recuperação segura de ingresso, operação offline ou sincronização.
- Auditoria completa WCAG/leitor de tela, testes em todos os navegadores, teste de carga, pentest, conformidade LGPD ou PCI.

Os documentos de critérios de aceite são **obrigações futuras**, não uma lista de controles já aprovados. A publicação deste esboço não autoriza processar pagamentos ou dados pessoais reais.
