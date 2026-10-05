(function () {
  var faqs = [
    {
      keywords: ["service", "services", "offer", "type", "types", "clean", "cleaning"],
      question: "What cleaning services do you offer?",
      answer: "We handle four categories: commercial (offices & retail), residential (homes & apartments), institutional (schools & clinics), and specialized cleaning (deep cleans, post-construction, post-event). See the Our Services page for details."
    },
    {
      keywords: ["area", "areas", "location", "where", "kigali", "cover"],
      question: "Which areas do you serve?",
      answer: "We're based in Kigali (Kicukiro, Niboye) and serve clients across the city."
    },
    {
      keywords: ["quote", "price", "pricing", "cost", "how much", "estimate"],
      question: "How do I get a quote?",
      answer: "Fill out the form on our Contact page with a few details about the space, and we'll follow up with a quote — usually the same business day."
    },
    {
      keywords: ["supplies", "equipment", "products", "bring", "own"],
      question: "Do you bring your own supplies and equipment?",
      answer: "Yes — our teams arrive with the cleaning products and equipment needed for the job, chosen with the surface and setting in mind."
    },
    {
      keywords: ["safety", "health", "protocol", "chemicals", "children", "safe"],
      question: "What are your health & safety standards?",
      answer: "We follow set protocols for product safety, staff protection, and site rules — especially in schools, clinics, and other sensitive spaces. See the Health & Safety page for the full breakdown."
    },
    {
      keywords: ["how soon", "start", "schedule", "availability", "recurring", "one-time", "one time", "frequency"],
      question: "Can I book a one-time clean, or only recurring service?",
      answer: "Both — we do one-off deep cleans and recurring contracts (daily, weekly, or a custom schedule), whichever fits what you need."
    },
    {
      keywords: ["contact", "phone", "email", "reach", "call"],
      question: "How can I reach you directly?",
      answer: "You can email info@lamarinvestment.rw, call +250 799 529 500, or use the Contact page form."
    }
  ];

  var suggestedOrder = [0, 1, 2, 4, 5];

  function scoreMatch(text, faq) {
    var lower = text.toLowerCase();
    var score = 0;
    faq.keywords.forEach(function (kw) {
      if (lower.indexOf(kw) !== -1) score += 1;
    });
    return score;
  }

  function findAnswer(text) {
    var best = null;
    var bestScore = 0;
    faqs.forEach(function (faq) {
      var s = scoreMatch(text, faq);
      if (s > bestScore) {
        bestScore = s;
        best = faq;
      }
    });
    return bestScore > 0 ? best.answer : null;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("lamar-chat-toggle");
    var panel = document.getElementById("lamar-chat-panel");
    var log = document.getElementById("lamar-chat-log");
    var form = document.getElementById("lamar-chat-form");
    var input = document.getElementById("lamar-chat-input");
    var chips = document.getElementById("lamar-chat-chips");
    var closeBtn = document.getElementById("lamar-chat-close");

    function addMessage(text, from) {
      var el = document.createElement("div");
      el.className = "chat-msg chat-msg-" + from;
      el.textContent = text;
      log.appendChild(el);
      log.scrollTop = log.scrollHeight;
    }

    function renderChips() {
      chips.innerHTML = "";
      suggestedOrder.forEach(function (idx) {
        var faq = faqs[idx];
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "chat-chip";
        btn.textContent = faq.question;
        btn.addEventListener("click", function () {
          addMessage(faq.question, "user");
          addMessage(faq.answer, "bot");
        });
        chips.appendChild(btn);
      });
    }

    if (!toggle) return;

    toggle.addEventListener("click", function () {
      panel.classList.toggle("open");
      if (panel.classList.contains("open") && log.children.length === 0) {
        addMessage("Hi! I'm the Lamar assistant. Ask me about our services, pricing, or coverage area — or tap a question below.", "bot");
        renderChips();
      }
    });

    closeBtn.addEventListener("click", function () {
      panel.classList.remove("open");
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var text = input.value.trim();
      if (!text) return;
      addMessage(text, "user");
      input.value = "";
      var answer = findAnswer(text);
      if (answer) {
        addMessage(answer, "bot");
      } else {
        addMessage("I don't have an exact answer for that — please reach out via the Contact page and our team will help directly.", "bot");
      }
    });
  });
})();
