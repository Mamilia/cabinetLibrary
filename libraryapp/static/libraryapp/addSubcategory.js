document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.querySelector("#addBtn");
  const uploadBtn = document.querySelector("#uploadBtn");
  const uploadFormDiv = document.querySelector("#uploadFormDiv");

  addBtn.addEventListener("click", () => {
    if (uploadFormDiv.style.display === "block") {
      hide(uploadFormDiv);
    } else {
      unhide(uploadFormDiv);
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
});
