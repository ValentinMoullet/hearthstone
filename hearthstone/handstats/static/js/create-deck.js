function heroChosen(e) {
	var hero = e.currentTarget.id;
	
	var mainContentDiv = $('#main-content');
	mainContentDiv.empty();
	
	// Create new header
	var h4 = document.createElement("h4");
	h4.textContent = "Creating " + hero + " deck";
	mainContentDiv.append(h4);
	
	// Create div for cards to be displayed
	var divCards = document.createElement("div");
	divCards.id = "cards";
	mainContentDiv.append(divCards);
	
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
	$("#search").on("input",function(event) {
		var search = $("#search");
		$.get("/get_matching_cards", {search: search.val().trim()})
			.done(function(data) {
				// When we get all matching cards, writing a new div with all of them
				divMatchingCards = $("#matching-cards");
				divMatchingCards.empty();

				if (data.cards != undefined) {
					// Writing all cards
					for (var i = 0; i < data.cards.length; i++) {
						var newCard = $(data.cards[i].html);
						divMatchingCards.append(newCard);
					}
				}
				
				// Put function on all matching cards that, when clicked, should add it to the current cards
				$(".matching-card").on("click", function(event) {
					console.log("Clicked");
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
