# Manual de Uso — AgendaFácil

## 1. Acessando o sistema

1. Abra https://agendafacil-pit2.onrender.com no navegador (computador ou celular). A primeira abertura pode demorar uns 50 segundos;
2. Entre com o usuário de demonstração:
   - **E-mail:** `admin@agendafacil.com`
   - **Senha:** `agenda123`
3. Você cai no **Painel (Início)**.

## 2. Painel (Início)

Mostra 4 números:
- **Atendimentos hoje**: quantos clientes ainda vão ser atendidos hoje;
- **Próximos agendamentos**: marcados para os próximos dias;
- **Clientes cadastrados**;
- **Faturado no mês**: soma dos atendimentos **concluídos** no mês.

Logo abaixo aparece a **agenda de hoje**, com botões para concluir, editar ou cancelar.

## 3. Clientes

- **Cadastrar:** menu **Clientes**, botão **+ Novo cliente**, preencha nome e telefone (obrigatórios) e clique em **Salvar**. O telefone é formatado sozinho enquanto você digita.
- **Buscar:** digite parte do nome ou do telefone e clique em **Buscar**.
- **Editar:** botão **Editar** na linha do cliente.
- **Excluir:** botão **Excluir** e confirme. Clientes que já têm agendamentos **não podem** ser excluídos, para não perder o histórico.

## 4. Serviços

- **Cadastrar:** menu **Serviços**, botão **+ Novo serviço**, informe nome, preço e duração em minutos.
- **Desativar:** o serviço deixa de aparecer na hora de agendar, mas o histórico continua. Dá para **Reativar** quando quiser.

## 5. Agendamentos

### Criar
1. Menu **Agenda**, botão **+ Novo agendamento**;
2. Escolha o **cliente** e o **serviço**;
3. Escolha a **data** e a **hora** (de 08h às 20h);
4. Clique em **Salvar**.

O sistema **não deixa**:
- marcar no passado;
- marcar fora do horário de funcionamento (o serviço precisa **terminar** até as 20h);
- marcar em cima de outro atendimento (ele considera a duração do serviço).

### Gerenciar
| Botão | O que faz |
|-------|-----------|
| **Concluir** | Marca o atendimento como feito (entra no faturamento) |
| **Editar** | Muda cliente, serviço, data ou hora |
| **Cancelar** | Cancela e libera o horário (pede confirmação) |
| **Reabrir** | Volta um cancelado para "agendado", se o horário ainda estiver livre |

### Filtrar
Use os campos **Data** e **Status** no topo da agenda e clique em **Filtrar**. O botão **Limpar** volta a mostrar tudo.

## 6. Sair
Clique em **Sair** no canto superior direito.

---

## Para desenvolvedores: rodando no seu computador

```bash
git clone https://github.com/lucasaugb/agendafacil-pit2.git
cd agendafacil-pit2
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
python run.py                    # abre em http://127.0.0.1:5000
```

Rodar os testes:

```bash
python -m pytest -v
```

Recriar o banco com os dados de exemplo:

```bash
flask --app run init-db
```
