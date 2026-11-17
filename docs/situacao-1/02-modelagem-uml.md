# 2. Modelagem UML — AgendaFácil

> Os diagramas estão em **Mermaid**, que o GitHub desenha automaticamente ao abrir este arquivo.

## 2.1 Diagrama de Casos de Uso

```mermaid
flowchart LR
    ator(("👤 Administrador /<br/>Recepcionista"))

    subgraph Sistema AgendaFácil
        UC01([UC01 - Fazer login])
        UC02([UC02 - Manter clientes])
        UC03([UC03 - Buscar cliente])
        UC04([UC04 - Manter serviços])
        UC05([UC05 - Ativar/desativar serviço])
        UC06([UC06 - Agendar atendimento])
        UC07([UC07 - Verificar conflito de horário])
        UC08([UC08 - Concluir / cancelar / reabrir])
        UC09([UC09 - Consultar agenda com filtros])
        UC10([UC10 - Ver painel do dia])
    end

    ator --> UC01
    ator --> UC02
    ator --> UC04
    ator --> UC06
    ator --> UC08
    ator --> UC09
    ator --> UC10
    UC02 -. extend .-> UC03
    UC04 -. extend .-> UC05
    UC06 -. include .-> UC07
    UC08 -. include .-> UC07
```

### Descrição do caso de uso principal — UC06 Agendar atendimento

| Item | Descrição |
|------|-----------|
| Ator | Administrador / Recepcionista |
| Pré-condição | Estar logado; existir ao menos um cliente e um serviço ativo |
| Fluxo principal | 1. Clica em "Novo agendamento" · 2. Escolhe cliente e serviço · 3. Informa data e hora · 4. Clica em "Salvar" · 5. O sistema valida (UC07) · 6. Grava e mostra "Agendamento criado com sucesso!" |
| Fluxo alternativo A1 | Campo vazio → o navegador destaca o campo e mostra "Este campo é obrigatório." |
| Fluxo alternativo A2 | Data no passado → "Não é possível agendar em uma data/hora que já passou." |
| Fluxo alternativo A3 | Fora do expediente → "Fora do horário de funcionamento (08h às 20h)." |
| Fluxo alternativo A4 | Horário ocupado → "Já existe um agendamento nesse horário. Escolha outro horário." |
| Pós-condição | Agendamento salvo com status **agendado** |

## 2.2 Diagrama de Classes (modelo de domínio / persistência)

```mermaid
classDiagram
    direction LR
    class Usuario {
        +int id
        +str nome
        +str email
        -str senha_hash
        +autenticar(email, senha) Usuario
        +buscar_por_id(id) Usuario
    }
    class Cliente {
        +int id
        +str nome
        +str telefone
        +str email
        +str observacoes
        +validar(dados)
        +listar(busca)
        +criar(dados) int
        +atualizar(id, dados)
        +excluir(id)
    }
    class Servico {
        +int id
        +str nome
        +str descricao
        +float preco
        +int duracao_min
        +bool ativo
        +validar(dados)
        +listar(somente_ativos)
        +criar(dados) int
        +atualizar(id, dados)
        +alternar_ativo(id)
    }
    class Agendamento {
        +int id
        +datetime data_hora
        +str status
        +str observacoes
        +validar(dados)
        +tem_conflito(inicio, fim) bool
        +criar(dados) int
        +atualizar(id, dados)
        +alterar_status(id, status)
        +resumo(hoje) dict
    }
    class StatusAgendamento {
        <<enumeration>>
        agendado
        concluido
        cancelado
    }
    class ValidacaoError {
        <<exception>>
        +list erros
    }

    Cliente "1" --> "0..*" Agendamento : possui
    Servico "1" --> "0..*" Agendamento : é usado em
    Agendamento --> StatusAgendamento
    Cliente ..> ValidacaoError : lança
    Servico ..> ValidacaoError : lança
    Agendamento ..> ValidacaoError : lança
```

## 2.3 Diagrama de Sequência — Criar agendamento (padrão MVC)

```mermaid
sequenceDiagram
    actor U as Recepcionista
    participant V as View (form.html + app.js)
    participant C as Controller (agendamento_controller)
    participant M as Model (Agendamento)
    participant DB as Banco SQLite

    U->>V: Preenche cliente, serviço, data e hora
    V->>V: Valida campos obrigatórios (JavaScript)
    V->>C: POST /agendamentos/novo
    C->>M: criar(dados)
    M->>DB: SELECT cliente / serviço ativo
    M->>DB: SELECT agendamentos do dia (verifica conflito)
    alt dados válidos e horário livre
        M->>DB: INSERT INTO agendamento
        M-->>C: id do novo agendamento
        C-->>V: redirect + mensagem "Agendamento criado com sucesso!"
    else regra violada
        M-->>C: ValidacaoError(lista de erros)
        C-->>V: mostra o formulário com os erros e os dados preenchidos
    end
    V-->>U: Exibe o resultado
```

## 2.4 Diagrama de Atividades — Validação do agendamento

```mermaid
flowchart TD
    A([Início]) --> B[Recebe cliente, serviço, data e hora]
    B --> C{Cliente existe?}
    C -- Não --> E1[Erro: selecione um cliente válido]
    C -- Sim --> D{Serviço existe e está ativo?}
    D -- Não --> E2[Erro: selecione um serviço válido]
    D -- Sim --> F{Data/hora válida?}
    F -- Não --> E3[Erro: data e hora inválidas]
    F -- Sim --> G{Está no futuro?}
    G -- Não --> E4[Erro: horário já passou]
    G -- Sim --> H{Entre 08h e 20h,<br/>incluindo a duração?}
    H -- Não --> E5[Erro: fora do horário]
    H -- Sim --> I{Sobrepõe outro<br/>agendamento ativo?}
    I -- Sim --> E6[Erro: horário ocupado]
    I -- Não --> J[Grava agendamento com status 'agendado']
    J --> K([Fim - mensagem de sucesso])
    E1 & E2 & E3 & E4 & E5 & E6 --> L([Fim - mostra erros ao usuário])
```

## 2.5 Diagrama de Estados — Agendamento

```mermaid
stateDiagram-v2
    [*] --> Agendado : criar
    Agendado --> Agendado : editar
    Agendado --> Concluido : concluir
    Agendado --> Cancelado : cancelar
    Cancelado --> Agendado : reabrir (se o horário estiver livre)
    Concluido --> [*]
```

## 2.6 Revisões feitas na modelagem (Kaizen)

| # | O que mudou | Por quê |
|---|-------------|---------|
| 1 | Criado o atributo `duracao_min` em Serviço | Sem a duração não dá para detectar conflito real (ex.: 10:00 de 50 min bate com 10:30) |
| 2 | Serviço ganhou `ativo` em vez de ser excluído | Excluir apagaria o histórico de agendamentos antigos |
| 3 | Status virou enumeração fechada | Evita valores inválidos e permite a restrição `CHECK` no banco |
| 4 | Criada a classe `ValidacaoError` | Padroniza as mensagens de erro mostradas ao usuário |
| 5 | Incluído o estado "reabrir" | Feedback: o cliente às vezes desiste do cancelamento |
