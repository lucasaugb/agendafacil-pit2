# Laudo de Qualidade — AgendaFácil v1.0

> ⚠️ **Preencha as partes marcadas com `[PREENCHER]`** depois de receber os 5 formulários dos colegas. Não esconda as falhas encontradas: o professor pede justamente que elas apareçam.

## 1. Identificação

| Item | Valor |
|------|-------|
| Sistema | AgendaFácil: agendamento para barbearias e salões |
| Versão avaliada | 1.0 |
| Período dos testes | [PREENCHER] |
| Responsável | [PREENCHER — seu nome] |
| Testadores | 5 colegas (ver seção 3) |

## 2. Resultado dos testes automatizados

| Tipo | Quantidade | Aprovados | Falhas |
|------|-----------|-----------|--------|
| Unitários (`test_models.py`) | 32 | 32 | 0 |
| Integração (`test_rotas.py`) | 16 | 16 | 0 |
| **Total** | **48** | **48** | **0** |

Evidência: saída completa do `python -m pytest -v` em [`resultado-pytest.txt`](resultado-pytest.txt).

## 3. Resumo dos testes de usuário

| # | Testador | Data | Funcionou | Não funcionou | Não testado |
|---|----------|------|-----------|---------------|-------------|
| 1 | [PREENCHER] | | | | |
| 2 | [PREENCHER] | | | | |
| 3 | [PREENCHER] | | | | |
| 4 | [PREENCHER] | | | | |
| 5 | [PREENCHER] | | | | |

## 4. Defeitos e sugestões encontrados

| ID | Descrição | Quem achou | Gravidade | Decisão | Correção feita | Evidência |
|----|-----------|-----------|-----------|---------|----------------|-----------|
| D01 | [PREENCHER] | | Alta / Média / Baixa | Corrigir / Não corrigir (motivo) | | print antes/depois |
| D02 | | | | | | |
| D03 | | | | | | |

### Correções já feitas durante o desenvolvimento (testes internos)

| ID | Problema | Correção |
|----|----------|----------|
| I01 | As mensagens de erro do formulário continuavam na tela mesmo depois de o campo ser corrigido | A mensagem agora some assim que o valor fica válido (`app.js`) |
| I02 | Ao abrir o endereço principal sem login, aparecia o aviso "Faça login para continuar" sem necessidade | O aviso só aparece quando a pessoa tenta abrir uma página interna |
| I03 | Agendamento das 19:50 de um serviço de 30 min terminaria depois do horário de fechamento | A regra RN03 agora considera o **fim** do atendimento |
| I04 | Editar um agendamento sem mudar o horário acusava conflito com ele mesmo | O agendamento sendo editado é ignorado na verificação |

## 5. Avaliação por característica de qualidade

| Característica | Avaliação | Justificativa |
|----------------|-----------|---------------|
| Funcionalidade | [PREENCHER] | Todos os RF implementados e testados |
| Confiabilidade | [PREENCHER] | Regras de negócio cobertas por testes automatizados |
| Usabilidade | [PREENCHER — média das notas] | Feedback dos colegas |
| Eficiência | Boa | Páginas simples, consultas com índice |
| Manutenibilidade | Boa | MVC, código comentado e testes |
| Segurança | Boa para a v1.0 | Senha com hash e rotas protegidas |

## 6. Conclusão

[PREENCHER: o sistema atende ou não aos requisitos, o que foi corrigido e o que fica para a próxima versão.]
