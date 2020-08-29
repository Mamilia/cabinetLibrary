document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".body").style.backgroundColor = "white";

  document.querySelectorAll(".edit-btn").forEach((button) => {
    button.addEventListener("click", (event) => {
      const target_btn = event.target;
      const btnDiv = target_btn.parentElement;
      const parentDiv = target_btn.parentElement.parentElement;
      const textarea = document.createElement("textarea");
      const btnSaveChanges = document.createElement("button");
      const btnCancelChanges = document.createElement("button");
      const bodyDiv = parentDiv.children[2];
      const contentText = bodyDiv.innerHTML;
      const post_id = parseInt(parentDiv.id);

      parentDiv.style.backgroundColor = "#b7f3cb";
      bodyDiv.innerHTML = "";
      textarea.setAttribute("class", "form-control");
      textarea.innerHTML = contentText;
      bodyDiv.append(textarea);
      hide(btnDiv);
      btnSaveChanges.type = "button";
      btnCancelChanges.type = "button";
      btnSaveChanges.className = "btn save-btn m-2 btn-default";
      btnCancelChanges.className = "btn cancel-btn m-2 btn-default";
      btnSaveChanges.innerHTML = "Save";
      btnCancelChanges.innerHTML = "Cancel";
      parentDiv.appendChild(btnSaveChanges);
      parentDiv.appendChild(btnCancelChanges);

      btnSaveChanges.addEventListener("click", () => {
        const newBody = textarea.value;
        fetch(`/edit/${post_id}`, {
          method: "PUT",
          body: JSON.stringify({
            body: newBody,
            userId: userId,
          }),
        });

        bodyDiv.innerHTML = newBody;
        textarea.remove();
        unhide(btnDiv);

        hide(btnSaveChanges);
        hide(btnCancelChanges);
      });

      btnCancelChanges.addEventListener("click", () => {
        textarea.remove();
        bodyDiv.innerHTML = contentText;
        unhide(btnDiv);
        hide(btnSaveChanges);
        hide(btnCancelChanges);
      });
    });
  });

  document.querySelectorAll(".delete-btn").forEach((button) => {
    button.addEventListener("click", (event) => {
      const target_btn = event.target;
      const parentDiv = target_btn.parentElement.parentElement;
      const post_id = parseInt(parentDiv.id);

      parentDiv.remove();

      const requestOptions = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId: userId,
        }),
      };
      fetch(`/edit/${post_id}`, requestOptions).then((response) => {
        response.json();
      });
    });
  });

  function hide(div) {
    div.style.display = "none";
  }
  function unhide(div) {
    div.style.display = "block";
  }
});
