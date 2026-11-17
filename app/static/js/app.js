// AgendaFácil - interações do front-end
(function () {
  "use strict";

  // 1) Menu no celular
  const btnMenu = document.querySelector("[data-menu]");
  if (btnMenu) {
    btnMenu.addEventListener("click", function () {
      document.getElementById("menu").classList.toggle("aberto");
    });
  }

  // 2) Fechar mensagens (e sumir sozinhas as de sucesso)
  document.querySelectorAll(".alerta .fechar").forEach(function (b) {
    b.addEventListener("click", function () { b.parentElement.remove(); });
  });
  setTimeout(function () {
    document.querySelectorAll(".mensagens .alerta-sucesso").forEach(function (a) { a.remove(); });
  }, 5000);

  // 3) Confirmação antes de ações destrutivas (excluir / cancelar)
  document.querySelectorAll("form[data-confirmar]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      if (!window.confirm(f.dataset.confirmar)) e.preventDefault();
    });
  });

  // 4) Máscara de telefone: (11) 98888-1111
  document.querySelectorAll("[data-mascara-telefone]").forEach(function (campo) {
    campo.addEventListener("input", function () {
      let d = campo.value.replace(/\D/g, "").slice(0, 11);
      if (d.length > 6) {
        const meio = d.length === 11 ? 7 : 6;
        campo.value = "(" + d.slice(0, 2) + ") " + d.slice(2, meio) + "-" + d.slice(meio);
      } else if (d.length > 2) {
        campo.value = "(" + d.slice(0, 2) + ") " + d.slice(2);
      } else {
        campo.value = d;
      }
    });
  });

  // 5) Data mínima = hoje (não deixa escolher dia passado no calendário)
  document.querySelectorAll("[data-hoje-minimo]").forEach(function (campo) {
    const h = new Date();
    const hoje = h.getFullYear() + "-" + String(h.getMonth() + 1).padStart(2, "0") + "-" + String(h.getDate()).padStart(2, "0");
    campo.min = hoje;
  });

  // 6) Validação no navegador, com mensagem embaixo do campo
  const mensagens = {
    valueMissing: "Este campo é obrigatório.",
    typeMismatch: "Formato inválido.",
    tooShort: "Muito curto.",
    rangeUnderflow: "Valor abaixo do permitido.",
    rangeOverflow: "Valor acima do permitido.",
  };
  document.querySelectorAll("form[data-validar]").forEach(function (form) {
    // Ao corrigir um campo, a mensagem de erro dele some na hora
    ["input", "change"].forEach(function (evento) {
      form.addEventListener(evento, function (e) {
        const campo = e.target;
        if (campo.classList.contains("invalido") && campo.checkValidity()) {
          campo.classList.remove("invalido");
          const msg = campo.nextElementSibling;
          if (msg && msg.classList.contains("msg-campo")) msg.remove();
        }
      });
    });
    form.addEventListener("submit", function (e) {
      let primeiroInvalido = null;
      form.querySelectorAll(".msg-campo").forEach(function (m) { m.remove(); });
      form.querySelectorAll("input, select, textarea").forEach(function (campo) {
        campo.classList.remove("invalido");
        if (!campo.checkValidity()) {
          campo.classList.add("invalido");
          const tipo = Object.keys(mensagens).find(function (k) { return campo.validity[k]; });
          const span = document.createElement("span");
          span.className = "msg-campo";
          span.textContent = mensagens[tipo] || "Valor inválido.";
          campo.insertAdjacentElement("afterend", span);
          primeiroInvalido = primeiroInvalido || campo;
        }
      });
      if (primeiroInvalido) {
        e.preventDefault();
        primeiroInvalido.focus();
      }
    });
  });
})();
