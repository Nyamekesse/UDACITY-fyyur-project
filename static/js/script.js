window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

const venue_deleteBtn = document.querySelectorAll(".delete-button");

venue_deleteBtn.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const venueId = e.target.dataset["id"];
    fetch("/venues/" + venueId, {
      method: "DELETE",
    });
  });
});
