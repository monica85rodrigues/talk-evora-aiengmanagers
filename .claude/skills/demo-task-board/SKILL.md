---
name: demo-task-board
description: Demo da talk "O teu novo par de mãos". Gere as tarefas do manager em 4 listas (Backlog, Para amanhã, In progress, Done) e mostra-as num quadro HTML de 4 colunas, com prazo e uma nota opcional de delegação (se vai ser delegada e a quem). Só para a demo da talk, com dados fictícios em talk/demos/tarefas/; não é a skill tarefas do projeto. Ativa com "acrescenta uma tarefa", "passa a tarefa para in progress", "está feito", "mostra o quadro", "/demo-task-board".
---

# Demo: quadro de tarefas

Escreve em português de Portugal, por tu. **Só tarefas de quem usa a skill** (não há campo de responsável). Cada tarefa pode ter um prazo e uma nota de delegação.

## Ficheiros
- **Fonte de verdade:** `talk/demos/tarefas/tarefas.md`, com quatro secções: `## Backlog`, `## Para amanhã`, `## In progress`, `## Done`. Formato no cabeçalho do ficheiro.
- **Vista:** `talk/demos/tarefas/tarefas.html`, gerada com `python3 .claude/skills/demo-task-board/scripts/gerar_quadro_html.py` (na raiz do projeto). **Não editar o HTML à mão.** Opção: `--hoje AAAA-MM-DD`.
- **Não confundir com a skill `tarefas`** (a lista real do projeto, em `tarefas/tarefas.md`): nunca a leias nem a alteres aqui.

## Formato de uma tarefa
`- Título | prazo AAAA-MM-DD (opcional) | nota de delegação (opcional) | adiada Nx (opcional) | Bloqueada: motivo (opcional)`
- Nota de delegação: `Delegar a: Nome` ou `Não delegar`. Sem nota = ainda por decidir.
- Em Done, acrescentar `feito AAAA-MM-DD` com a data em que ficou feita.

## Como usar (fluxo da demo)
Sempre que a skill corre, **primeiro gera o quadro e abre-o no browser** (`python3 .claude/skills/demo-task-board/scripts/gerar_quadro_html.py` e depois `open talk/demos/tarefas/tarefas.html`), **e só depois** pergunta, sem mais nada antes: *"Qual é a tarefa, ou o que queres atualizar?"* Assim ela vê o estado atual enquanto responde.

O quadro **atualiza-se sozinho no browser a cada 3 segundos**: depois de qualquer alteração basta voltar a gerá-lo (não abras outro separador; só voltas a abrir se ela disser que fechou o quadro).

Depois de a pessoa responder:
1. **Nova tarefa:** vai para `## Backlog`, a menos que ela diga outra coluna.
   - Prazo: só se ela o disser. Datas relativas ("sexta") passam a absolutas (AAAA-MM-DD) e ficam confirmadas na resposta.
   - **Delegação:** se ela não disse nada sobre delegar, pergunta **uma vez**: *"Vais delegar? A quem?"*. "Não" → `Não delegar`; um nome → `Delegar a: Nome`; "não sei" → sem nota.
2. **Mover:** "passa X para in progress", "põe X para amanhã" ou "X está feito" → muda a tarefa de secção. Em Done acrescenta `feito` com a data de hoje. Se o título for ambíguo, pergunta qual.
3. **Planear o dia seguinte:** quando ela disser "planeia-me o amanhã" (ou parecido), **sugere até 3 tarefas** do Backlog, pela ordem: atrasadas, prazo mais próximo e, entre iguais, as que **não vão ser delegadas** (as que têm `Delegar a:` ficam de fora ou vão no fim, ditas como tal). Explica em meia linha porquê cada uma e **só as move para `## Para amanhã` quando ela confirmar**. A coluna tem um limite de 3: se já tiver 3, diz-lho e pergunta o que sai.
4. **Novo dia** ("novo dia", "começar o dia", ou quando ela diz que ontem não deu para fazer o que estava planeado): **vê o que ficou por fazer em `## Para amanhã`** e passa por cada tarefa, **uma de cada vez**, perguntando o que fazer:
   - **Continua hoje** → passa para `## In progress`.
   - **Adiar** → fica em `## Para amanhã` e soma 1 ao campo `adiada Nx` (começa em `adiada 1x`).
   - **Voltar ao Backlog** → deixou de ser prioridade (mantém o prazo, se tiver).
   - **Delegar** → pergunta a quem e acrescenta `Delegar a: Nome`.
   - **Dividir** → pergunta os títulos das partes mais pequenas, acrescenta-as e retira a original (as partes herdam o prazo).
   **Regra das 2 adiadas:** se a tarefa já tem `adiada 2x` (ou mais) e ela não a fez, **não a empurres outra vez sem perguntar**. Primeiro pergunta o que a prende: *é grande demais? alguém a pode fazer? já não importa? está bloqueada por algo?* e segue a resposta (dividir, delegar, voltar ao Backlog, ou `Bloqueada: motivo`). Nunca a apagues: só se ela o pedir.
5. **Alterar ou apagar:** editar a linha (prazo, delegação, título) ou apagá-la só se ela pedir.
6. **Gerar** o quadro outra vez (o separador já aberto atualiza-se sozinho).
7. **Resumir em 2 ou 3 linhas** o que mudou e o que merece atenção (tarefas atrasadas, In progress com mais de 3, Para amanhã com mais de 3). Terminar com a pergunta inicial outra vez, para ela poder juntar mais.

Se ela pedir só para **ver** o quadro, fica só o que já foi aberto no arranque: não perguntes nada e resume o estado como no passo 7.

## O que a vista mostra
- Quatro colunas: Backlog (bege), **Para amanhã** (claro, com a data do próximo dia útil, por exemplo "seg 16 nov" à sexta), In progress (azul) e Done (rosa), com o número de tarefas em cada uma.
- Em cada cartão: título, prazo (rosa se atrasada, bege se é hoje) e a nota de delegação (azul se delegada, cinzento claro se não), e ainda "Adiada N×" (rosa a partir de 2) e "Bloqueada: motivo" quando existirem.
- Avisos no topo: tarefas adiadas 2 vezes ou mais, tarefas atrasadas **In progress com mais de 3 tarefas** (demasiadas coisas em simultâneo) e **Para amanhã com mais de 3** (um plano com demasiadas prioridades).

## Regras
- **Não inventar** tarefas, prazos nem nomes. Só o que ela disser.
- Mover, não apagar: uma tarefa feita passa para Done, não se elimina.
- Não escreve em nenhuma ferramenta externa (Jira, Notion, etc.). Tudo vive em `tarefas.md`.
- Não pôr nomes de empresas ou pessoas reais nos dados da demo.
- Ao concluir, indicar o caminho do `tarefas.html`.
