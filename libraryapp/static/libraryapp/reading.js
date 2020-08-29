document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.querySelector("#addBtn");
  const uploadBtn = document.querySelector("#uploadBtn");
  const uploadFormDiv = document.querySelector("#uploadFormDiv");
  const searchBtn = document.querySelector("#searchBtn");
  const searchFormDiv = document.querySelector("#searchFormDiv");

  addBtn.addEventListener("click", () => {
    if (uploadFormDiv.style.display === "block") {
      hide(uploadFormDiv);
    } else {
      unhide(uploadFormDiv);
    }
  });

  searchBtn.addEventListener("click", () => {
    if (searchFormDiv.style.display === "block") {
      hide(searchFormDiv);
    } else {
      unhide(searchFormDiv);
    }
  });

  uploadBtn.addEventListener("click", () => {
    hide(uploadFormDiv);
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
