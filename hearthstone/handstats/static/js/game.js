// Get matching cards to the string 'search' and update the div 'divId'
function getMatchingCards(search, type) {
	$.get("/get_matching_cards", {search: search})
		.done(function(data) {
			// When we get all matching cards, writing a new div with all of them
			var divMatchingCards = $("#matching-cards-" + type);
			divMatchingCards.empty();

			if (data.cards != undefined) {
				// Writing all cards
				for (var i = 0; i < data.cards.length; i++) {
					var newCard = $(data.cards[i].html);
					divMatchingCards.append(newCard);
				}
			}
			
			// Put function on all matching cards that, when clicked, should do an action depending on the type
			$(".matching-card").on("click", function(event) {
				var gameId = $("#game").val();
				var cardId = event.currentTarget.id.split("_")[event.currentTarget.id.split("_").length - 1];
				if (type == "played") {
					$.post("/use_opponent_card", {game_id: gameId, card_id: cardId})
					.done(function(data) {
						if (data == "Success") {
							var message = document.createElement("h5");
							message.className = "green-text";
							message.textContent = "Card correctly used! Update will be seen next turn.";
							divMatchingCards.prepend(message);
						}
						else {
							var message = document.createElement("h5");
							message.className = "red-text";
							message.textContent = "Error! The card could not have been used.";
							divMatchingCards.prepend(message);
						}
					});
				}
				else if (type == "maybe") {
					$.post("/update_opponent_prob_maybe", {game_id: gameId, card_id: cardId})
					.done(function(data) {
						$("#info_message").empty();
						if (data == "Success") {
							var message = document.createElement("h5");
							message.className = "green-text";
							message.textContent = "Probabilities correctly updated! Update will be seen next turn.";
							divMatchingCards.prepend(message);
						}
						else {
							var message = document.createElement("h5");
							message.className = "red-text";
							message.textContent = "Error! The probabilities could not have been updated.";
							divMatchingCards.prepend(message);
						}
						
					});
				}
				else if (type == "sure") {
					$.post("/update_opponent_prob_sure", {game_id: gameId, card_id: cardId})
					.done(function(data) {
						if (data == "Success") {
							var message = document.createElement("h5");
							message.className = "green-text";
							message.textContent = "Probabilities correctly updated! Update will be seen next turn.";
							divMatchingCards.prepend(message);
						}
						else {
							var message = document.createElement("h5");
							message.className = "red-text";
							message.textContent = "Error! The probabilities could not have been updated.";
							divMatchingCards.prepend(message);
						}
						
					});
				}
			});

	});
}

function getMatchingCardsSure(e) {
	var search = $("#search-sure").val();
	getMatchingCards(search, "sure");
}

function getMatchingCardsMaybe(e) {
	var search = $("#search-maybe").val();
	getMatchingCards(search, "maybe");
}

function getMatchingCardsPlayed(e) {
	var search = $("#search-played").val();
	getMatchingCards(search, "played");
}

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
  
  $("#search-sure").on("input", getMatchingCardsSure);
  $("#search-maybe").on("input", getMatchingCardsMaybe);
  $("#search-played").on("input", getMatchingCardsPlayed);

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