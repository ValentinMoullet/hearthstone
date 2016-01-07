function removeCard(e) {
	var deckCreationId = $("#deck-creation-id").val();
	var divId = e.currentTarget.parentElement.id;
	var cardId = divId.split("_")[divId.split("_").length - 1];
	
	$.post("/remove_card_from_deck_creation", {deck_creation_id: deckCreationId, card_id: cardId})
		.done(function(data) {
			var divCards = $('#cards');
			divCards.empty();
			if (data != "") {
				for (var i = 0; i < data.realCards.length; i++) {
					var newRealCard = $(data.realCards[i].html);
					divCards.append(newRealCard);
				}
				
				$(".remove-card").on("click", removeCard);
			}
			
		});
}

function submitDeck() {
	var deckCreationId = $("#deck-creation-id").val();
	var deckName = $("#deck-name").val();
	console.log(deckCreationId);
	console.log(deckName);
	$.post("/submit_deck_creation", {deck_creation_id: deckCreationId, deck_name: deckName})
		.done(function(data) {
			if (data == "Success") {
				alert("Deck successfully created!");
			}
			
		});
}

function heroChosen(e) {
	var hero = e.currentTarget.id;
	
	$.post("/create_new_deck_creation", {hero: hero})
		.done(function(data) {
			
			var mainContentDiv = $('#main-content');
			mainContentDiv.empty();
			
			// Get the id of the object DeckCreation and put in a hidden field
			var deckCreationId = data;
			var hiddenField = document.createElement("input");
			hiddenField.type = "hidden";
			hiddenField.id = "deck-creation-id";
			hiddenField.value = deckCreationId;
			$("body").append(hiddenField);
			
			// Create new header
			var h4 = document.createElement("h4");
			h4.textContent = "Creating " + hero + " deck";
			mainContentDiv.append(h4);
			
			// Create new header
			var h5 = document.createElement("h5");
			h5.textContent = "First, choose a name for your deck. It must be comprehensive.";
			mainContentDiv.append(h5);
			
			// Put input for deck name
			var inputDeckName = document.createElement("input");
			inputDeckName.type = "text";
			inputDeckName.id = "deck-name";
			inputDeckName.placeholder = "Enter the deck name";
			mainContentDiv.append(inputDeckName);
			
			// Create new header
			h5 = document.createElement("h5");
			h5.textContent = "Now, put all cards in the deck (30 cards).";
			mainContentDiv.append(h5);
			
			// Create div for cards to be displayed
			var divCards = document.createElement("div");
			divCards.id = "cards";
			mainContentDiv.append(divCards);
			
			// Create form for submitting deck
			var formSubmitDeck = document.createElement("form");
			formSubmitDeck.action = "existing_decks";
			formSubmitDeck.method = "get";
			formSubmitDeck.id = "form-submit-deck";
			mainContentDiv.append(formSubmitDeck);
			// Submit deck when clicking on submitting deck
			$("#form-submit-deck").submit(submitDeck);
			
			// Create button to submit deck
			var submitDeckButton = document.createElement("input");
			submitDeckButton.type = "submit";
			submitDeckButton.id = "submit-deck";
			submitDeckButton.value = "Submit deck";
			submitDeckButton.disabled = true;
			$('#form-submit-deck').append(submitDeckButton);
			
			// Create search bar
			var searchBar = document.createElement("input");
			searchBar.type = "text";
			searchBar.id = "search";
			searchBar.placeholder = "Enter card's name";
			mainContentDiv.append(searchBar);
			
			// Create div to display current matching cards when searching
			var divMatchingCards = document.createElement("div");
			divMatchingCards.id = "matching-cards";
			mainContentDiv.append(divMatchingCards);
			
			// Create function when searching
			$("#search").on("input", function(event) {
				var search = $("#search");
				$.get("/get_matching_cards", {search: search.val().trim()})
					.done(function(data) {
						console.log("Done getting matchng cards");
						// When we get all matching cards, writing a new div with all of them
						divMatchingCards = $("#matching-cards");
						divMatchingCards.empty();

						if (data.cards != undefined) {
							console.log("Not undefined");
							// Writing all cards
							for (var i = 0; i < data.cards.length; i++) {
								var newCard = $(data.cards[i].html);
								divMatchingCards.append(newCard);
							}
						}
						
						// Put function on all matching cards that, when clicked, should add it to the current cards
						$(".matching-card").on("click", function(event) {
							var cardId = event.currentTarget.id.split("_")[event.currentTarget.id.split("_").length - 1];
							$.post("/add_card_to_deck_creation", {deck_creation_id: deckCreationId, new_card_id: cardId})
								.done(function(data) {
									var divCards = $('#cards');
									divCards.empty();
									for (var i = 0; i < data.realCards.length; i++) {
										var newRealCard = $(data.realCards[i].html);
										divCards.append(newRealCard);
									}
									
									// If the deck contains 30 cards, enable the submit deck button
									if (data.complete == "True") {
										document.getElementById("submit-deck").disabled = false;
									}
									
									$(".remove-card").on("click", removeCard);
									
								});
						});

				});
			});
		});
}




$(document).ready(function () {
  // Add event-handlers
  $(".hero").click(heroChosen);

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
