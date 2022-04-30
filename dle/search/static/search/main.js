//validates form for user so no empty entries get accepted into the tracking history
function validateForm() {
    var x = document.forms["trackingForm"]["tracking"].value;
    if (x == "") {
      alert("Error: your submission is empty");
      return false;
    }
  }