# Template: comunicação de release

> **Este é o template padrão da skill `demo-release-comms`, o mesmo para toda a gente que a usar.** A skill lê-o sempre que corre.
> Se for preciso mudar a comunicação (títulos, ordem, textos, perguntas, secções), edita este ficheiro e a mudança vale para todos.
> Cada secção tem **Escrever** (o que a skill deve pôr) e **Perguntar** (o que pergunta se faltar, com um exemplo).

## Público, tamanho e tom
- **Público: senior leadership.** Vão ler depressa e decidir ou acompanhar: o mais importante primeiro, em linguagem de negócio (impacto, resultado, decisões), sem detalhe técnico nem jargão de equipa.
- **A skill melhora sempre o que a pessoa escreve** para este público (frases curtas, claras, orientadas ao resultado), sem acrescentar factos que ela não deu.
- Até ~150 palavras. Sem frases de marketing vazias.
- Datas absolutas e claras.

## Secções (por ordem)

### 1. Título
- **Escrever:** nome da release e o estado (por exemplo, confirmada, atrasada ou concluída). A data fica na secção seguinte.
- **Perguntar:** qual é a release e em que estado está? (ex.: "Release das notificações, atrasada")

### 2. Data da release
- **Escrever:** a data prevista, em formato claro (dia e mês, e o ano se não for o corrente). Se a data mudou, a nova e a anterior. Se ainda não está fechada, dizer o que a condiciona e quando se confirma.
- **Perguntar:** qual é a data da release? Mudou? (ex.: "7 dez, antes era 30 nov")

### 3. O que muda com esta release
- **Escrever:** 2 a 4 pontos, na linguagem de quem lê: benefício e impacto, não tarefas técnicas. Se algo ficou fora do âmbito, dizer.
- **Perguntar:** o que fica diferente para quem lê (utilizadores, clientes, equipas)? (ex.: "passam a receber avisos em tempo real")

### 4. O que estamos a validar
- **Escrever:** o que queremos aprender **a nível de negócio** com este lançamento (não testes técnicos): a hipótese, como vamos saber se resultou (indicador ou sinal) e quando se avalia. Se for preciso algo dos leitores (feedback, decisão, dados), dizer exatamente o quê.
- **Perguntar:** o que queres validar a nível de negócio e como vais saber? (ex.: "se os utilizadores reagem mais depressa aos avisos; avaliamos a taxa de abertura nas 2 primeiras semanas")

### 5. Próximos passos
- **Escrever:** lista curta com ação, responsável e data. Terminar com quando será a próxima atualização.
- **Perguntar:** quais são os próximos passos, quem os faz e quando? (ex.: "decisão go/no-go na sexta, 4 dez")

### 6. Recursos
- **Escrever:** lista de links úteis, cada um com uma frase a dizer o que é (por exemplo, release notes, documentação, quadro do projeto, painel de métricas, FAQ). Só os links que a pessoa der, copiados tal como os deu. Se não houver links, **omitir esta secção**.
- **Perguntar:** há links ou recursos a partilhar? (ex.: "release notes, quadro do épico, painel de métricas")

### 7. Fecho de agradecimento (sem título de secção)
- **Escrever:** **não leva título.** É a frase final da comunicação, que **relembra e agradece** a quem colaborou, dizendo em que ajudou. Concreto, nunca "obrigado a todos". Só quem a pessoa indicar e só pelo que disser.
- **Perguntar:** a quem queres agradecer no fim e em quê? (ex.: "à equipa de QA pelos testes de regressão")

## Modelo visual da resposta
```
**{Título}**
**Data da release:** ...

**O que muda com esta release**
- ...

**O que estamos a validar**
...

**Próximos passos**
- ação · responsável · data

**Recursos**
- [nome](link): o que é

Obrigada a ... por ...
```
