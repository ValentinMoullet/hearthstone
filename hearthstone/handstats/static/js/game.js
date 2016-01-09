// Check that at least one checkbox is checked, otherwise alert + stop
function checkAtLeastOneCheckbox(e) {
	var checkBoxes = getCheckedBoxes("checkbox[]")
	if (checkBoxes == null) {
		alert("You must choose at least one deck.");
		e.preventDefault();
	}
}

// Pass the checkbox name to the function
function getCheckedBoxes(chkboxName) {
	var checkboxes = document.getElementsByName(chkboxName);
	var checkboxesChecked = [];
	// loop over them all
	for (var i=0; i<checkboxes.length; i++) {
	 // And stick the checked ones onto an array...
	 if (checkboxes[i].checked) {
		checkboxesChecked.push(checkboxes[i]);
	 }
	}
	// Return the array if it is non-empty, or null
	return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}

$(document).ready(function () {
  // Add event-handlers
  $("#end-turn").click(checkAtLeastOneCheckbox);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});