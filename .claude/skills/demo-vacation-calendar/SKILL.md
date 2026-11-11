---
name: demo-vacation-calendar
description: Demo da talk "O teu novo par de mãos". Junta as férias das pessoas da equipa (de países e sistemas diferentes) num calendário único em HTML, com uma pessoa por linha, feriados de cada país, sobreposições, marcos e pedidos à espera de aprovação. Só para a demo da talk (dados fictícios em talk/demos/ferias/). Ativa com "férias da equipa", "calendário de férias", "quem está fora", "a Inês vai de férias", "mostra as férias", "/demo-vacation-calendar".
---

# Demo: calendário de férias da equipa

Escreve em português de Portugal, por tu. As pessoas estão em vários países (Portugal, Polónia, Roménia) e marcam férias em sistemas diferentes (Google Calendar, portal de RH, email, pedido no 1:1). Esta skill junta tudo numa **vista única**.

## Ficheiros
- **Fonte de verdade:** `talk/demos/ferias/ferias.md` (pessoas, férias, feriados, marcos). Formato explicado no cabeçalho do ficheiro. Pessoas fictícias: Inês (Portugal), Carlos (Polónia), Joaquim (Roménia).
- **Vista:** `talk/demos/ferias/ferias.html`, gerada com `python3 .claude/skills/demo-vacation-calendar/scripts/gerar_ferias_html.py` (na raiz do projeto). **Não editar o HTML à mão.**
- Opções do script: `--de AAAA-MM-DD`, `--ate AAAA-MM-DD` (janela; por defeito o mês de hoje e o seguinte, ajustados à largura do ecrã, sem scroll horizontal) e `--hoje AAAA-MM-DD`.

## Como usar (fluxo da demo)
Sempre que a skill corre, **começa por perguntar**, sem mais nada antes: *"Quais as férias que queres adicionar? Diz-me o nome da pessoa e os dias."*

Depois de a pessoa responder:
1. **Acrescentar** ao `ferias.md`, na secção `## Férias`, sem fazer mais perguntas:
   - Estado `aprovado` por defeito (ela só diz nome e dias); `pendente` apenas se ela o disser.
   - Fonte: `Indicado pelo manager`.
   - Datas relativas ("a semana depois do Natal") passam a absolutas; confirmar numa linha só se houver dúvida real. Vários períodos da mesma pessoa, ou várias pessoas, numa só resposta: acrescentar todos.
   - Se a pessoa **ainda não existe** em `## Pessoas`, perguntar só o país (e acrescentá-la). Se o país não tiver feriados no ficheiro, perguntar e acrescentá-los.
2. **Gerar** o calendário (`python3 .claude/skills/demo-vacation-calendar/scripts/gerar_ferias_html.py`) e abrir `ferias.html` no browser (`open`).
3. **Resumir em 2 ou 3 linhas** o que mudou e o que passou a merecer atenção (sobreposições, conflito com um marco), a partir do que o script imprime. Terminar com a pergunta inicial outra vez, para ela poder juntar mais férias.

Se a pessoa pedir só para **ver** o calendário, saltar a pergunta e fazer os passos 2 e 3. Para **remover ou corrigir** férias, editar a linha em `ferias.md` e regenerar. Mudar para `aprovado` só quando a pessoa o disser.

## O que a vista mostra
- Uma linha por pessoa (país, dias úteis de férias já descontando fins de semana e feriados do país dela), aprovadas a azul e pendentes a bege com contorno.
- Feriados de cada país a tracejado, fins de semana a cinzento, marcos (◆) e a linha "Pessoas ausentes" com o número de pessoas de férias em cada dia útil (rosa a partir de 2; azul quando é toda a equipa).
- "O que merece a tua atenção": pedidos à espera de decisão, dias com 2 ou todos fora, férias que coincidem com um marco ou começam até 7 dias depois dele.

## Regras
- **Feriados do país da pessoa também não são férias:** se um período incluir um feriado, não se pinta nem conta; se o pedido for só um feriado, avisar de que não gasta dia de férias.
- **Fins de semana nunca são férias.** Se o período dado atravessar um fim de semana, regista-se o período tal como foi dito, mas o calendário não pinta nem conta sábados e domingos como férias (o script já o faz).
- **Não inventar datas, feriados nem estados.** Se faltar um dado, perguntar. Os feriados do ficheiro são nacionais e de exemplo: dizer que se confirmam os regionais antes de usar a sério.
- **Não aprova, não recusa e não escreve em nenhum calendário.** Só organiza e mostra; a decisão é tua. Esta versão não lê o Google Calendar nem portais de RH: as datas vêm do `ferias.md` (o que ela colar ou ditar).
- Não pôr nomes reais de pessoas ou empresas nos dados da demo.
- Ao concluir, indicar o caminho do `ferias.html`.
