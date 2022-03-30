//validates form for user so no empty entries get accepted into the tracking history
function validateForm() {
    var x = document.forms["trackingForm"]["tracking"].value;
    if (x == "") {
      alert("Error: your submission is empty");
      return false;
    }
  }

 // window.addEventListener('load', function() {
 // document.querySelector('input[type="file"]').addEventListener('change', function() {
//      if (this.files && this.files[0]) {
//          var img = document.querySelector('img');  // $('img')[0]
//          img.src = URL.createObjectURL(this.files[0]); // set src to blob url
//          img.onload = imageIsLoaded;
//      }
//  });
// }

// function imageIsLoaded() { 
//  alert(this.src);  // blob url
  // update width and height ...
//}