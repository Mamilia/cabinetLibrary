document.addEventListener("DOMContentLoaded", () => {
  const bananaDiv = document.querySelector("#banana_img");
  const countBanana = document.querySelector("#count_banana");

  bananaDiv.addEventListener("click", (btn) => {
    const img = btn.target;
    if (bananalike) {
      img.style.opacity = "0.3";
      bananalike = false;
      countBanana.innerHTML--;
      putBanana();
    } else {
      img.style.opacity = "1";
      bananalike = true;
      countBanana.innerHTML++;
      putBanana();
    }
  });

  function putBanana() {
    const reading = parseInt(readingId);

    const requestOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
    };
    fetch(`bananalike/${readingId}`, requestOptions).then((response) => {
      response.json();
    });
  }

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
      const reviewId = parseInt(parentDiv.id);

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
        fetch(`/edit-review/${reviewId}`, {
          method: "PUT",
          body: JSON.stringify({
            body: newBody,
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
      const reviewId = parseInt(parentDiv.id);
      parentDiv.remove();

      const requestOptions = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      };
      fetch(`/edit-review/${reviewId}`, requestOptions).then((response) => {
        response.json();
        console.log(response);
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
