# O teu novo par de mãos: AI para engineering managers

Cinco skills do Claude Code usadas nas demos da talk (Évora, 14 de novembro de 2026), com dados fictícios para experimentares.

| Skill | O que faz |
|---|---|
| `/demo-1on1-prep` | Lê transcrições de 1:1 e prepara o próximo: temas em aberto, o que prometeste (e o que a pessoa prometeu) e 3 perguntas |
| `/demo-vacation-calendar` | Junta as férias da equipa (vários países) num calendário único, com feriados e alertas |
| `/demo-feedback-writer` | Corrige um feedback com COIN, SBI ou STAR e ajuda-te a acompanhá-lo |
| `/demo-release-comms` | Escreve a comunicação de uma release para senior leadership, a partir de um template |
| `/demo-task-board` | Quadro de tarefas (Backlog, Para amanhã, In progress, Done) no browser |

## Como usar

1. Instala o [Claude Code](https://claude.com/claude-code).
2. Clona ou descarrega esta pasta.
3. Abre um terminal **dentro da pasta** e corre `claude`.
4. Escreve o nome de uma skill, por exemplo `/demo-task-board`.

Precisas de ter o Python 3 instalado (sem bibliotecas extra) para o calendário e o quadro.

> **Importante:** corre o Claude Code a partir desta pasta. Se copiares as skills para outro projeto, copia também `fontes/` e `talk/demos/` e mantém a mesma estrutura.

## Os teus próprios dados

Os ficheiros em `talk/demos/` são a fonte de verdade de cada skill (transcrições, férias, feedback e tarefas). Muda-os para os teus e mantém os nomes e o formato descritos no cabeçalho de cada um. Usa dados reais com cuidado, sobretudo se tiverem informação pessoal da tua equipa.

## Fontes

`fontes/` tem Poppins e Playfair Display (licença SIL Open Font License), usadas nas vistas em HTML.

## Licença

MIT (ver `LICENSE`). As fontes em `fontes/` mantêm a licença SIL Open Font License.
