# Laudo de Qualidade — AgendaFácil v1.0

## 1. Identificação

| Item | Valor |
|------|-------|
| Sistema | AgendaFácil: agendamento para barbearias e salões |
| Versão avaliada | 1.0 |
| Período dos testes | Novembro de 2026 |
| Responsável | Lucas Augusto Braz dos Santos |
| Testadores | 5 colegas (ver seção 3) |

## 2. Resultado dos testes automatizados

| Tipo | Quantidade | Aprovados | Falhas |
|------|-----------|-----------|--------|
| Unitários (`test_models.py`) | 32 | 32 | 0 |
| Integração (`test_rotas.py`) | 16 | 16 | 0 |
| **Total** | **48** | **48** | **0** |

Evidência: saída completa do `python -m pytest -v` em [`resultado-pytest.txt`](resultado-pytest.txt).

## 3. Resumo dos testes de usuário

| # | Testador | Funcionou | Não funcionou | Não testado / observações |
|---|----------|-----------|---------------|---------------------------|
| 1 | Otávio Calistro | Todas as funcionalidades | Nenhum problema | Nada; tudo foi testado |
| 2 | Alisson Dambrate | Agendamentos, filtros, edição e demais telas | Nenhum problema | Nada; tudo foi testado |
| 3 | Vinicius Prado Batista | Todas as opções e filtros | Nenhum problema | Sugeriu mais filtros e opções de agendamento |
| 4 | Letícia Alves Palamar | Todas as funcionalidades testadas | Nenhum problema | Sentiu falta de forma de pagamento |
| 5 | Victor Henrique Janisseti | Fluxo completo | Nenhum problema na versão final | Achou o sistema muito útil (o pai tem uma barbearia) |

## 4. Defeitos e sugestões

**Defeitos na versão final:** nenhum defeito foi apontado pelos testadores.

**Sugestões recebidas:**

| ID | Sugestão | Quem sugeriu | Decisão |
|----|----------|-------------|---------|
| S01 | Mais filtros e opções de agendamento | Vinicius Prado Batista | Pertinente. Registrada no backlog da versão 2.0 |
| S02 | Registrar a forma de pagamento do atendimento | Letícia Alves Palamar | Pertinente. Registrada no backlog da versão 2.0 |

### Correções feitas durante o desenvolvimento (testes internos)

| ID | Problema | Correção |
|----|----------|----------|
| I01 | As mensagens de erro do formulário continuavam na tela mesmo depois de o campo ser corrigido | A mensagem agora some assim que o valor fica válido (`app.js`) |
| I02 | Ao abrir o endereço principal sem login, aparecia o aviso "Faça login para continuar" sem necessidade | O aviso só aparece quando a pessoa tenta abrir uma página interna |
| I03 | Agendamento das 19:50 de um serviço de 30 min terminaria depois do horário de fechamento | A regra RN03 agora considera o **fim** do atendimento |
| I04 | Editar um agendamento sem mudar o horário acusava conflito com ele mesmo | O agendamento sendo editado é ignorado na verificação |
| I05 | No servidor do Render (fuso UTC), horários próximos podiam ser recusados como "no passado" | O sistema passou a usar sempre o fuso de Brasília |

## 5. Avaliação por característica de qualidade

| Característica | Avaliação | Justificativa |
|----------------|-----------|---------------|
| Funcionalidade | Ótima | Todos os requisitos implementados; nenhum defeito apontado pelos 5 testadores |
| Confiabilidade | Ótima | 48 testes automatizados aprovados; regras de negócio cobertas |
| Usabilidade | Ótima | Testadores usaram todas as telas sem dificuldade |
| Eficiência | Boa | Páginas simples, consultas com índice |
| Manutenibilidade | Boa | MVC, código comentado e testes |
| Segurança | Boa para a v1.0 | Senha com hash e rotas protegidas |

## 6. Conclusão

O AgendaFácil v1.0 atende aos requisitos funcionais e não funcionais definidos no planejamento. Os 48 testes automatizados foram aprovados, e os 5 testadores usaram todas as funcionalidades sem encontrar defeitos na versão final. As sugestões recebidas, mais filtros e opções de agendamento e o registro da forma de pagamento, são melhorias pertinentes e ficam registradas no backlog da versão 2.0.
