//Load controllers for results page
$(document).ready(function() {
    initBanner();
    get_results(1);
});

initBanner = function()
{
    $("[data-hide]").on("click", function(){
        $(this).closest("." + $(this).attr("data-hide")).hide(200);
    });
};


get_results = function(page){
    $("#banner_results_wait").show(200);
    var templateID = $("#template_id").html();
    $.ajax({
        url : getResultsUrl,
        type : "POST",
        dataType: "json",
        data : {
        	templateID: templateID,
            page:page
        },
        success: function(data){
            $("#banner_results_wait").hide(200);
        	$("#results").html(data.results);
        	if (data.hasResult)
        	    $("#results_select").show();
        },
        error:function(data){

        }
    });
};


/**
 * Shows/hides a result of the results page
 * @param event
 */
showhideResult = function(event){
	var button = event.target;
	var parent = $(event.target).parent();
	$(parent.children('.xmlResult')).toggle("blind",500);
	if ($(button).attr("class") == "expand"){
		$(button).attr("class","collapse");
	}else{
		$(button).attr("class","expand");
	}
};
