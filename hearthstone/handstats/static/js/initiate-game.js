function heroChosen(e) {
	var hero = e.currentTarget.id;
	console.log(hero);
			
	var mainContentDiv = $('#main-content');
	mainContentDiv.empty();
	
	// Create new header
	var h4 = document.createElement("h4");
	h4.textContent = "Which deck(s) do you think he can be playing? (you can select multiple)";
	mainContentDiv.append(h4);
	
	var hiddenField = document.createElement("input");
	hiddenField.type = "hidden";
	hiddenField.id = "hero";
	hiddenField.name = "hero";
	hiddenField.value = hero;
	mainContentDiv.append(hiddenField);
	
	// Create ul for decks
	var ul = document.createElement("ul");
	ul.id = "decks";
	ul.className = "collection";
	mainContentDiv.append(ul);
	
	$.get("/existing_decks", {hero: hero})
		.done(function(data) {
			for (var i = 0; i < data.decks.length; i++) {
				var newDeck = $(data.decks[i].html);
				$("#decks").append(newDeck);
			}
			
		});
		
	// Create button to create the game
	var buttonDecksChosen = document.createElement("input");
	buttonDecksChosen.type = "button";
	buttonDecksChosen.id = "decks-chosen";
	buttonDecksChosen.value = "Submit";
	buttonDecksChosen.className = "btn";
	buttonDecksChosen.onclick = deckChosen;
	mainContentDiv.append(buttonDecksChosen);
	
}

function deckChosen(e) {
	// Get hero in hidden field
	var hero = $("#hero").val();
	
	// Get all decks selected
	var checkedBoxes = getCheckedBoxes("checkbox[]");
	if (checkedBoxes == null) {
		alert("You must choose at least one deck.");
		return;
	}
	var deckIds = [];
	for (var i = 0; i < checkedBoxes.length; i++) {
		var id = checkedBoxes[i].id;
		var deckId = id.split("_")[id.split("_").length - 1];
		console.log(deckId);
		deckIds.push(deckId);
	}
			
	var mainContentDiv = $('#main-content');
	mainContentDiv.empty();
	
	// Create new header
	var h4 = document.createElement("h4");
	h4.textContent = "Who is playing first?";
	mainContentDiv.append(h4);
	
	// Create form with hidden fields (hero and decks selected)
	var firstForm = document.createElement("form");
	firstForm.action = "new_game";
	firstForm.method = "post";
	firstForm.id = "game-form";
	mainContentDiv.append(firstForm);
	
	var hiddenFieldHero = document.createElement("input");
	hiddenFieldHero.type = "hidden";
	hiddenFieldHero.id = "hero";
	hiddenFieldHero.name = "hero";
	hiddenFieldHero.value = hero;
	$("#game-form").append(hiddenFieldHero);
	
	// Create string with ids of decks selected separated by a ','
	var decks = "";
	for (var i = 0; i < deckIds.length - 1; i++) {
		decks += deckIds[i] + ",";
	}
	decks += deckIds[deckIds.length - 1];
	
	var hiddenFieldDecks = document.createElement("input");
	hiddenFieldDecks.type = "hidden";
	hiddenFieldDecks.id = "decks";
	hiddenFieldDecks.name = "decks";
	hiddenFieldDecks.value = decks;
	$("#game-form").append(hiddenFieldDecks);
	
	var buttonMe = document.createElement("input");
	buttonMe.type = "submit";
	buttonMe.name = "button";
	buttonMe.id = "button-me";
	buttonMe.value = "Me";
	buttonMe.className = "btn";
	$("#game-form").append(buttonMe);
	
	var buttonOpponent = document.createElement("input");
	buttonOpponent.type = "submit";
	buttonOpponent.name = "button";
	buttonOpponent.id = "button-opponent";
	buttonOpponent.value = "My opponent";
	buttonOpponent.className = "btn";
	$("#game-form").append(buttonOpponent);
	
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
  $(".hero-opponent").click(heroChosen);

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