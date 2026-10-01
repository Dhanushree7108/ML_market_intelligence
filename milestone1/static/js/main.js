// Milestone 1 — light client-side polish only.
// Server-side validation in app.py is the source of truth.

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".intake-form");
  if (!form) return;

  const budgetInput = document.getElementById("budget");

  form.addEventListener("submit", (event) => {
    const requiredFields = form.querySelectorAll("[required]");
    let firstInvalid = null;

    requiredFields.forEach((field) => {
      if (!field.value.trim()) {
        field.style.borderColor = "#C24444";
        if (!firstInvalid) firstInvalid = field;
      } else {
        field.style.borderColor = "";
      }
    });

    if (budgetInput && budgetInput.value && Number(budgetInput.value) < 0) {
      budgetInput.style.borderColor = "#C24444";
      if (!firstInvalid) firstInvalid = budgetInput;
    }

    if (firstInvalid) {
      event.preventDefault();
      firstInvalid.focus();
    }
  });

  // Clear the red outline as soon as the person starts fixing a field.
  form.querySelectorAll("input, textarea").forEach((field) => {
    field.addEventListener("input", () => {
      field.style.borderColor = "";
    });
  });
});
