function heroChosen(e) {
	var hero = e.currentTarget.id;
	console.log(hero);
			
	var mainContentDiv = $('#main-content');
	mainContentDiv.empty();
	
	// Create new header
	var h4 = document.createElement("h4");
	h4.textContent = "Which deck do you think he is playing?";
	mainContentDiv.append(h4);
	
	var hiddenField = document.createElement("input");
	hiddenField.type = "hidden";
	hiddenField.id = "hero";
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
	
}

function deckChosen(e) {
	var hero = e.currentTarget.id;
	console.log(hero);
			
	var mainContentDiv = $('#main-content');
	mainContentDiv.empty();
	
	// Create new header
	var h4 = document.createElement("h4");
	h4.textContent = "Who is playing first?";
	mainContentDiv.append(h4);
	
	// Create form with hidden field (hero)
	var firstForm = document.createElement("form");
	firstForm.action = "new_game";
	firstForm.method = "post";
	firstForm.id = "game-form";
	mainContentDiv.append(firstForm);
	
	var hiddenField = document.createElement("input");
	hiddenField.type = "hidden";
	hiddenField.id = "hero";
	hiddenField.value = hero;
	$("#game-form").append(hiddenField);
	
	var buttonMe = document.createElement("input");
	buttonMe.type = "submit";
	buttonMe.name = "button-me";
	buttonMe.id = "button-me";
	buttonMe.value = "Me";
	buttonMe.className = "btn";
	$("#game-form").append(buttonMe);
	
	var buttonOpponent = document.createElement("input");
	buttonOpponent.type = "submit";
	buttonOpponent.name = "button-opponent";
	buttonOpponent.id = "button-opponent";
	buttonOpponent.value = "My opponent";
	buttonOpponent.className = "btn";
	$("#game-form").append(buttonOpponent);
	
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