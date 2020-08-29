document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.querySelector("#addSubcategory");
  const formE = document.querySelector("#newSubcategory");
  const cancelBtn = document.querySelector("#cancelBtn");
  const saveBtn = document.querySelector("#saveBtn");
  const searchBtn = document.querySelector("#searchBtn");
  const searchFormDiv = document.querySelector("#searchFormDiv");

  addBtn.addEventListener("click", (event) => {
    const target_btn = event.target;
    target_btn.disabled = true;
    unhide(formE);
  });

  cancelBtn.addEventListener("click", () => {
    addBtn.disabled = false;
    hide(formE);
  });

  saveBtn.addEventListener("click", () => {
    hide(formE);
  });

  searchBtn.addEventListener("click", () => {
    if (searchFormDiv.style.display === "block") {
      hide(searchFormDiv);
    } else {
      unhide(searchFormDiv);
    }
  });

  function hide(e) {
    e.style.display = "none";
  }
  function unhide(e) {
    e.style.display = "block";
  }

  const tr = document.querySelectorAll("tr[data-href]");
  tr.forEach((t) => {
    t.addEventListener("click", () => {
      window.location.href = t.dataset.href;
    });
  });
});
