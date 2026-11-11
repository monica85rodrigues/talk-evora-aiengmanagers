---
name: demo-release-comms
description: Demo da talk "O teu novo par de mãos". Escreve a comunicação de uma release para stakeholders, com título, data da release, o que muda com esta release, o que estamos a validar, próximos passos, recursos (links) e um fecho a agradecer a quem colaborou, a partir do que a pessoa contar. Só para a demo da talk; não é para posts. Ativa com "comunicação de release", "escreve a comunicação da release", "release notes", "anuncia a release", "/demo-release-comms".
---

# Demo: comunicação de release

Escreve em português de Portugal, por tu (e na voz de quem usa a skill quando escreve em nome dela: direta, clara, humana, sem jargão desnecessário). **Se ela pedir inglês, escreve em inglês.** O texto final é para **senior leadership**: quem lê tem de perceber em 30 segundos o que muda, o que falta confirmar e o que vai acontecer a seguir.

## Template (parte da skill)
A estrutura da comunicação está em **`template.md`, na pasta desta skill** (`.claude/skills/demo-release-comms/template.md`). É o template padrão que **qualquer pessoa usa sempre**: não o mudes nem o ignores por iniciativa tua e não uses uma estrutura de memória. **Lê-o sempre que a skill corre** e segue exatamente o que lá está (secções, ordem, títulos, tamanho e tom). Só se altera se a pessoa pedir.

## Arranque (uma pergunta de cada vez)
1. Lê o template.
2. **Pergunta uma secção de cada vez, pela ordem do template**, usando o campo **Perguntar** de cada uma (com o exemplo). **Uma só pergunta por mensagem**, curta, e **espera pela resposta** antes de passar à seguinte. Começa logo pela primeira secção, sem introdução longa.
3. Se a pessoa **já tiver dado** numa resposta a informação de secções seguintes, não voltes a perguntar essas: salta-as. Se ela disser "salta" ou "não há" numa secção, passa à seguinte (e se for Recursos, omite a secção).
4. Se ela der **tudo de uma vez** logo no início, não perguntes nada e escreve logo.
5. **Completa as lacunas antes de escrever.** Se faltar um elemento que o campo **Escrever** de uma secção pede, é porque a pessoa provavelmente **se esqueceu**: **pergunta-lho**, uma pergunta de cada vez, logo a seguir à pergunta da secção (ou no fim, por ordem do template). Elementos a verificar:
   - **Título:** o estado (confirmada, atrasada, concluída).
   - **Data:** se mudou (e a data anterior).
   - **O que muda:** o benefício para quem lê.
   - **O que estamos a validar:** a hipótese (o que esperamos que aconteça), o indicador e quando se avalia.
   - **Próximos passos:** o responsável e a data de cada passo, e quando é a próxima atualização.
   - **Fecho:** em quê ajudou cada pessoa ou equipa a quem agradece.
   Faz a pergunta **uma só vez** por lacuna. Se ela responder "não sei", "salta" ou "não há", aceita, escreve sem esse ponto e assinala-o no fim em "Dados em falta". Nunca preenchas a lacuna com suposições.
6. **Depois de completar as lacunas**, escreve a comunicação seguindo o campo **Escrever** de cada secção e o **Modelo visual** do template.
7. **Melhora sempre o que ela escreveu** para o público (senior leadership): resultado e impacto primeiro, linguagem de negócio, frases curtas e claras, sem detalhe técnico. **Reescreve, não copies as palavras dela tal e qual**, mas nunca acrescentes factos, benefícios, metas ou responsáveis que ela não deu.

## O que devolver
1. A **comunicação pronta a enviar**, nas secções do template (títulos a negrito, listas curtas).
2. **Verificação rápida** (✓ ou ⚠️): segue o template (secções, ordem, tamanho) · datas absolutas e claras · o "o que muda" fala do impacto para quem lê · a validação é de negócio (hipótese, como se mede, quando se avalia) · próximos passos com responsável e data · o fecho de agradecimento é concreto e sem título · sem jargão nem culpas (sobretudo se houve atraso).
3. **O que melhorei:** 3 a 5 linhas "de → para" com as alterações que fizeste ao texto dela para senior leadership.
4. **Dados em falta ou a confirmar:** o que ficou de fora ou é proposta tua (ex.: uma data ou um responsável que ela não disse).
5. Uma frase a perguntar se quer uma **versão curta para chat** (3 a 4 linhas), mais formal, mais informal ou noutra língua.

## Regras
- **Não inventar** datas, funcionalidades, indicadores, metas, resultados nem nomes. Não escrever testes técnicos (performance, QA) em "O que estamos a validar" a não ser que ela diga que são o objetivo de negócio. Falta algo → escreve sem esse ponto e diz o que ficou de fora; nunca preenchas com suposições.
- Se houve atraso: factual, sem culpas e sem nomes de quem "falhou"; foca no que muda, na nova data e no plano.
- **Não inventar links.** Só os que ela der, copiados tal como os deu; sem links, a secção Recursos não aparece.
- **Os agradecimentos não levam título:** são a frase final da comunicação, que relembra e agradece às pessoas indicadas. Só agradece a quem ela indicar, e só pelo que ela disser que fizeram.
- Não envia nada a ninguém nem guarda ficheiros; a resposta fica na conversa. Se ela pedir para guardar, escreve num ficheiro à parte e diz onde.
- Privacidade: não pôr nomes de empresas ou clientes reais; nomes de colegas só os que ela der (na demo, são fictícios).
