# 1. Escopo e Requisitos — AgendaFácil

## 1.1 Problema

Pequenas barbearias e salões de beleza ainda controlam os horários em cadernos, agendas de papel ou conversas de WhatsApp. Isso causa:

- **Dois clientes marcados no mesmo horário** (conflito de agenda);
- **Esquecimento** de quem vem e qual serviço vai ser feito;
- **Nenhum controle** de quanto foi faturado no mês;
- Perda do histórico do cliente (preferências, alergias etc.).

## 1.2 Solução proposta

O **AgendaFácil** é um sistema web simples, que funciona no computador e no celular, para o dono ou a recepção do estabelecimento:

- Cadastrar **clientes** e **serviços** (preço e duração);
- Criar **agendamentos** com bloqueio automático de conflito de horário;
- Acompanhar a **agenda do dia** e marcar atendimentos como concluídos ou cancelados;
- Ver um **painel** com os números do dia e o faturamento do mês.

## 1.3 Partes interessadas (stakeholders)

| Ator | Descrição |
|------|-----------|
| Administrador / Recepcionista | Usa o sistema todos os dias para agendar e atender |
| Dono do estabelecimento | Acompanha o faturamento e o movimento |
| Cliente final | Não usa o sistema, mas é beneficiado (não sofre com horário duplicado) |

## 1.4 Escopo

**Dentro do escopo (versão 1.0):** login, CRUD de clientes, CRUD de serviços (com ativar/desativar), CRUD de agendamentos, mudança de status, filtros, painel e layout responsivo.

**Fora do escopo (versões futuras):** agendamento feito pelo próprio cliente, lembrete por WhatsApp/SMS, vários profissionais com agendas separadas, pagamentos online.

> **Revisão (melhoria contínua / Kaizen):** na revisão do planejamento, o escopo foi reduzido para um **único profissional por agenda**. Assim a regra de conflito fica simples e confiável, e a funcionalidade "vários profissionais" foi registrada como evolução futura.

## 1.5 Requisitos Funcionais (RF)

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF01 | O sistema deve permitir login com e-mail e senha | Alta |
| RF02 | O sistema deve permitir sair (logout) | Alta |
| RF03 | Cadastrar, listar, editar e excluir clientes | Alta |
| RF04 | Buscar clientes por nome ou telefone | Média |
| RF05 | Cadastrar, listar e editar serviços (nome, descrição, preço, duração) | Alta |
| RF06 | Desativar/reativar serviços sem apagar o histórico | Média |
| RF07 | Criar, listar e editar agendamentos | Alta |
| RF08 | Marcar agendamento como concluído, cancelado ou reabrir | Alta |
| RF09 | Filtrar a agenda por data e por status | Média |
| RF10 | Exibir painel com atendimentos do dia, próximos, total de clientes e faturamento do mês | Média |

## 1.6 Requisitos Não Funcionais (RNF)

| ID | Requisito | Categoria |
|----|-----------|-----------|
| RNF01 | As senhas devem ser guardadas com *hash* (nunca em texto puro) | Segurança |
| RNF02 | Todas as telas (menos o login) exigem usuário autenticado | Segurança |
| RNF03 | A interface deve funcionar em celular (layout responsivo) | Usabilidade |
| RNF04 | Toda ação deve dar retorno visual (mensagem de sucesso ou erro) | Usabilidade |
| RNF05 | Ações destrutivas (excluir, cancelar) pedem confirmação | Usabilidade |
| RNF06 | As páginas devem carregar em menos de 2 segundos | Desempenho |
| RNF07 | Código organizado no padrão MVC | Manutenibilidade |
| RNF08 | Cobertura de testes automatizados das regras de negócio | Confiabilidade |
| RNF09 | Banco de dados relacional popular (SQLite) | Portabilidade |

## 1.7 Regras de Negócio (RN)

| ID | Regra |
|----|-------|
| RN01 | O agendamento precisa de um cliente existente e de um serviço **ativo** |
| RN02 | Não é permitido agendar em data/hora que já passou |
| RN03 | O atendimento deve começar e terminar dentro do horário de funcionamento (08h às 20h) |
| RN04 | Não pode haver dois agendamentos **ativos** com horários sobrepostos (considera a duração do serviço) |
| RN05 | Agendamento concluído ou cancelado não pode ser editado |
| RN06 | Cliente que possui agendamentos não pode ser excluído (preserva o histórico) |
| RN07 | Nome do serviço é único |
| RN08 | Um agendamento cancelado só pode ser reaberto se o horário continuar livre |

## 1.8 Rastreabilidade (Requisito → Código → Teste)

| Requisito | Onde está no código | Teste automatizado |
|-----------|--------------------|--------------------|
| RF01 / RNF01 | `app/models/usuario.py` → `autenticar` | `TestUsuario`, `test_login_*` |
| RF03 / RN06 | `app/models/cliente.py` | `TestCliente`, `test_cadastrar_cliente_*` |
| RF05 / RN07 | `app/models/servico.py` | `TestServico` |
| RN01–RN04 | `app/models/agendamento.py` → `validar`, `tem_conflito` | `test_rn01_*` … `test_rn04_*` |
| RN05 / RN08 | `Agendamento.atualizar`, `alterar_status` | `test_concluir_*`, `test_reabrir_*` |
| RF10 | `Agendamento.resumo` | `test_faturamento_do_mes` |
