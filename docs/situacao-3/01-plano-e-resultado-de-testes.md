# Plano e Resultado de Testes — Verificação e Validação

O projeto segue o **Modelo V**: cada fase de construção tem um tipo de teste correspondente.

| Fase (Verificação ↓) | Teste (Validação ↑) | Como foi feito no AgendaFácil |
|----------------------|---------------------|-------------------------------|
| Requisitos | **Teste de Aceitação** | 5 colegas usaram o sistema e preencheram o formulário (ver `02-formulario-teste-usuario.md`) |
| Análise | **Teste de Sistema** | Roteiro manual abaixo (seção 3), executado no navegador |
| Arquitetura | **Teste de Integração** | `tests/test_rotas.py`: tela, controller e banco juntos (16 testes) |
| Código | **Teste Unitário** | `tests/test_models.py`: regras de negócio isoladas (32 testes) |

## 1. Verificação (o produto está sendo construído do jeito certo?)

| Atividade | Resultado |
|-----------|-----------|
| Revisão dos requisitos x código (tabela de rastreabilidade em `situacao-1/01`) | Todos os RF e RN têm código e teste correspondentes |
| Revisão do modelo de dados (normalização até a 3FN) | OK |
| Inspeção do código seguindo o MVC (nenhum SQL dentro de controller ou view) | OK |
| Senhas guardadas com hash | OK, com `generate_password_hash` do Werkzeug |

## 2. Testes automatizados (pytest)

Como executar:

```bash
python -m pytest -v
```

**Resultado da última execução:** ✅ **48 testes aprovados, 0 falhas.**

### Testes unitários (`tests/test_models.py`)

| Grupo | O que é testado |
|-------|-----------------|
| `TestUsuario` | Login correto, senha errada, campos vazios, e-mail em maiúsculas |
| `TestCliente` | Cadastro válido; nome curto, telefone e e-mail inválidos; busca; exclusão bloqueada se houver agendamento |
| `TestServico` | Cadastro com vírgula no preço; preço negativo ou texto; duração fora da faixa; nome duplicado; desativar |
| `TestAgendamento` | RN01 serviço inativo, RN02 passado, RN03 fora do horário, RN04 conflito, horário "colado" permitido, cancelado libera horário, reabrir com horário ocupado, editar sem conflitar consigo mesmo, status inválido, faturamento |

### Testes de integração (`tests/test_rotas.py`)

| Teste | Comportamento esperado |
|-------|------------------------|
| Acesso sem login | Redireciona para `/login` |
| Login inválido / válido | Mostra o erro / abre o painel |
| Logout | Bloqueia o acesso de novo |
| Página inexistente | Retorna 404 com tela amigável |
| CRUD de clientes pela tela | Mensagens de sucesso e erro corretas |
| Cadastro de serviço pela tela | Aparece na lista |
| Criar agendamento pela tela | "Agendamento criado com sucesso" |
| Conflito pela tela | "Já existe um agendamento nesse horário" |
| Cancelar / filtrar por status | Lista filtrada corretamente |

## 3. Teste de sistema (roteiro manual)

| # | Passo | Resultado esperado | Resultado |
|---|-------|--------------------|-----------|
| 1 | Abrir o sistema sem login | Tela de login | ✅ |
| 2 | Entrar com senha errada | "E-mail ou senha incorretos." | ✅ |
| 3 | Entrar com admin | Painel com 4 cards | ✅ |
| 4 | Novo agendamento com tudo vazio → Salvar | Campos em vermelho com "Este campo é obrigatório." | ✅ |
| 5 | Agendar em horário já ocupado | "Já existe um agendamento nesse horário." e dados mantidos | ✅ |
| 6 | Cadastrar cliente com telefone "123" | "Telefone inválido…" | ✅ |
| 7 | Excluir cliente com agendamento | Confirmação → mensagem de bloqueio | ✅ |
| 8 | Concluir um atendimento | Selo "Concluído" e faturamento do mês aumenta | ✅ |
| 9 | Abrir no celular | Menu ☰ e tabelas em formato de cartão | ✅ |
| 10 | Acessar `/qualquer-coisa` | Tela 404 amigável | ✅ |

## 4. Validação (construímos o produto certo?)

A validação foi feita com **5 usuários-dublês** (colegas de curso), que usaram o sistema como se fossem o recepcionista de um salão. Os resultados estão em `03-laudo-de-qualidade.md`.
