# Roteiro do Vídeo — AgendaFácil (~5 minutos)

> **Antes de gravar:** abra o sistema já logado em uma aba, o GitHub em outra e o VS Code com o projeto. Use um gravador de tela (OBS Studio, Xbox Game Bar `Win + Alt + R` ou o Clipchamp do Windows). Fale com calma: não precisa decorar, leia por tópicos.

---

## Vídeo 1: solução funcionando (≈ 5 min)

### 0:00–0:30 · Abertura
**Tela:** página de login.
> "Olá, meu nome é ___, RGM ___. Este é o meu Projeto Integrador Transdisciplinar em Engenharia de Software II. Eu desenvolvi o **AgendaFácil**, um sistema web de agendamento para barbearias e salões. O problema que ele resolve é comum: muitos salões ainda anotam horários no papel ou no WhatsApp, e isso gera cliente marcado no mesmo horário, esquecimento e nenhum controle de faturamento."

### 0:30–1:00 · Tecnologias e arquitetura
**Tela:** VS Code mostrando as pastas `models`, `views` e `controllers`.
> "O back-end foi feito em **Python com Flask**, usando o padrão **MVC**. Em **Models** ficam as regras de negócio e o acesso ao banco, em **Views** as telas em HTML, CSS e JavaScript, e em **Controllers** as rotas que ligam as duas coisas. O banco de dados é **SQLite**, e os testes automatizados foram feitos com **pytest**."

### 1:00–1:30 · Login e painel
**Tela:** errar a senha uma vez e depois entrar certo.
> "O sistema tem login, e a senha fica salva com hash, nunca em texto puro. Se eu erro a senha, ele avisa. Entrando, aparece o painel com os atendimentos de hoje, os próximos, o total de clientes e o faturamento do mês."

### 1:30–2:15 · Clientes e serviços
**Tela:** cadastrar um cliente com telefone errado, mostrar o erro, corrigir e salvar. Depois mostrar a lista de serviços.
> "Aqui eu cadastro clientes. Repare que o telefone ganha máscara sozinho. Se eu coloco um telefone inválido, o sistema mostra a mensagem e não perde o que eu digitei. Corrigindo, ele salva e mostra a mensagem de sucesso. Nos serviços eu tenho preço e duração, e em vez de excluir eu posso **desativar** um serviço, para não perder o histórico."

### 2:15–3:30 · Agendamento: a parte principal
**Tela:** novo agendamento → salvar vazio → preencher → tentar horário ocupado → escolher horário livre.
> "Agora a funcionalidade principal. Se eu tento salvar vazio, os campos ficam vermelhos. Vou escolher um cliente e um serviço… e se eu tento marcar num horário que **já está ocupado**, o sistema bloqueia, porque ele considera a **duração** do serviço. Ele também não deixa marcar no passado nem fora do horário de funcionamento, das 8h às 20h. Escolhendo um horário livre, o agendamento é criado."

### 3:30–4:00 · Gerenciar a agenda
**Tela:** concluir um atendimento, cancelar outro (mostrar a confirmação), reabrir, usar o filtro.
> "Na agenda eu posso **concluir** um atendimento, que entra no faturamento, ou **cancelar**. O sistema pede confirmação antes. Um cancelado pode ser **reaberto** se o horário ainda estiver livre. Também dá para filtrar por data e status."

### 4:00–4:30 · Testes automatizados
**Tela:** terminal rodando `python -m pytest -v`.
> "Para garantir a qualidade, eu criei **48 testes automatizados**: testes unitários das regras de negócio e testes de integração que simulam o uso das telas. Todos passando."

### 4:30–5:00 · GitHub e encerramento
**Tela:** repositório no GitHub, abrindo a pasta `docs` e o diagrama de classes.
> "Todo o projeto está no GitHub: o código, a documentação com requisitos, diagramas UML, modelo do banco e dicionário de dados, o manual de uso e os testes. O sistema também está publicado online neste link. Obrigado!"

---

## Vídeo 2: correções após o feedback (até 5 min)

> Grave **depois** de receber os 5 formulários e corrigir o que for pertinente.

1. **(0:00–0:30)** "Neste vídeo eu mostro as mudanças feitas a partir dos testes que 5 colegas fizeram no AgendaFácil."
2. **(0:30–1:00)** Mostre o **laudo de qualidade** no GitHub e a tabela de defeitos.
3. **(1:00–4:00)** Para cada correção: *"O colega X apontou que ___. Antes estava assim [mostrar print]. Agora está assim [mostrar no sistema]."*
4. **(4:00–4:30)** Mostre o que **não** foi corrigido e explique o motivo (ex.: "fica para a versão 2.0").
5. **(4:30–5:00)** Rode o pytest de novo mostrando tudo verde e encerre.
