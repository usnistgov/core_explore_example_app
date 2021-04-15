/**
 * Show the custom tree to choose a field for the query builder
 */
var showCustomTree = function(currentCriteriaID)
{
    $("#current_criteria").html(currentCriteriaID);
    $( "#custom-tree-modal" ).modal("show");
    // hide remove and add buttons
    var xsd_form = $("#xsd_form");
    xsd_form.find(".remove").hide();
    xsd_form.find(".add").hide();
};


/**
 * Select an element to insert in the query builder
 */
var selectElement = function(event)
{
    var elementID = $(event.target).attr('select_id');
    var criteriaID = $("#current_criteria").html();
	$.ajax({
        url : selectElementUrl,
        type : "POST",
        dataType: "json",
        data : {
        	elementID: elementID
        },
		success: function(data){
            var $criteriaTag = $("#" + criteriaID);
            $($criteriaTag.children()[1]).val(data.elementName);
            $($criteriaTag.children()[1]).attr("class","elementInput");
            $($criteriaTag).attr("element_id", elementID);
            $($criteriaTag).attr("element_name", data.elementName);
            updateUserInputs(elementID, criteriaID.substring(4, criteriaID.length)); // crit0 -> 0
            $( "#custom-tree-modal" ).modal("hide");
	    }
    });
};


/**
 * Select an element from the custom tree, for sub-elements query
 */
var selectParent = function(event)
{
    var leavesID = $(event.target).attr('select_id');
    $("#leaves_id").html(leavesID);

    $('#subElementQueryError').html("");
    $( "#custom-tree-modal" ).modal("hide");
    $( "#sub-elements-query-builder-modal" ).modal("show");
    $( "#sub_elements_query_insert" ).on('click', insert_sub_element_query);

	prepare_sub_element_query();
};


/**
 * AJAX call, get the sub elements query builder
 */
var prepare_sub_element_query = function(){
    var templateID = $("#template_id").html();
    var leavesID = $("#leaves_id").html();

    $.ajax({
        url : getSubElementsQueryBuilderUrl,
        type : "POST",
        dataType: "json",
        data : {
        	leavesID: leavesID,
            templateID: templateID
        },
		success: function(data){
			$("#subElementQueryBuilder").html(data.subElementQueryBuilder);
	    }
    });
};


/**
 * AJAX call, inserts a sub query in the form
 */
var insert_sub_element_query = function(){
    var $subElementQueryBuilder = $("#subElementQueryBuilder");
    var selectedCheckboxes = $subElementQueryBuilder.find("input[type=checkbox]:checked");

    // sub element query only makes sense when at least 2 elements are selected
    if (selectedCheckboxes.length < 2){
        $('#subElementQueryError').html("Please select at least two elements.");
        return;
    }

    var templateID = $("#template_id").html();
    var criteriaID = $("#current_criteria").html();
    var formValues = getFormValues($subElementQueryBuilder);
    $.ajax({
        url : insertSubElementsQueryUrl,
        type : "POST",
        dataType: "json",
        data : {
        	formValues: formValues,
            templateID: templateID,
            criteriaID: criteriaID
        },
		success: function(data){
            var $criteria = $("#" + data.criteriaID);
            // set criteria attributes
            $criteria.attr("element_id", data.queryID);
            $criteria.attr("element_name", data.prettyQuery);
            $criteria.attr("element_type", "query");
            // insert the pretty query in the query builder
            $($criteria.children()[1]).val(data.prettyQuery);
            var field = $criteria.children()[1];
            // replace the pretty by an encoded version
            $(field).val($(field).html($(field).val()).text());
            // set the class to query
            $($criteria.children()[1]).attr("class", "queryInput");
            // remove all other existing inputs
            $("#" +data.uiID).children().remove();
            // close the modal
            $( "#sub-elements-query-builder-modal" ).modal("hide");
	    },
	    error: function(data){
            $('#subElementQueryError').html(data.responseText);
        }
    });
};


/**
 * When an element is selected in the query builder, input fields are added to the
 * form according to the type of the element.
 * @param elementID
 * @param criteriaID
 */
var updateUserInputs = function(elementID, criteriaID){
    var templateID = $("#template_id").html();
	update_user_inputs(elementID, criteriaID, templateID);
};


/**
 * AJAX call, update user inputs for the selected element type
 */
var update_user_inputs = function(elementID, criteriaID, templateID){
    $.ajax({
        url : updateUserInputUrl,
        type : "POST",
        dataType: "json",
        data : {
        	elementID: elementID,
        	// criteriaID: criteriaID,
        	templateID: templateID
        },
        success: function(data){
            var $ui = $("#ui" + criteriaID);
            var $criteria = $("#crit" + criteriaID);
            $ui.html(data.userInputs);
            $criteria.attr('element_type', data.element_type);
        }
    });
};

/**
 * Get the id of the tag to be created
 * @returns {number}
 */
var getNextTagID = function(){
    // get last tag id
	var lastTagID = $("#queryForm").find("p:last").attr('id');
	// tag id format: crit + n
	var lastTagIDValue = parseInt(lastTagID.slice(4));
	// get value of next tag id
	return lastTagIDValue + 1;
};

/**
 * Add an empty field to the query builder
 */
var addField = function(){
	// get value of next tag id
	var nextTagIDValue = getNextTagID();
	add_field(nextTagIDValue);
};


/**
 * AJAX call, add field to the form
 * @param nextTagID
 */
var add_field = function(nextTagID){
    $.ajax({
        url : addCriteriaUrl,
        type : "POST",
        dataType: "json",
        data : {
        	tagID: nextTagID
        },
        success: function(data){
            var $queryForm = $("#queryForm");
            // remove all add buttons
            $queryForm.find(".add").remove();

            // add new criteria to form
            $queryForm.append(data.criteria);

            var $first_criteria = $($queryForm.find("p:first"));

            if ($first_criteria.find(".remove").length == 0){
                // clone existing button
                var remove_button = $queryForm.find(".remove:first").clone();
                // append missing button
                $first_criteria.append(remove_button);
            }
        }
    });
};

/**
 * Remove a field from the query builder
 */
var removeField = function(event){
    // get criteria id
    var $target = $(event.target);
    var $parent = $($target.parents("p"));
    var criteriaID = $parent.attr('id');
	var $queryForm = $("#queryForm");
    var $criteriaTag = $("#" + criteriaID);

    // save add button
    var add_button = $queryForm.find(".add:first").clone();
    // save first criteria select (different from others)
    var first_select = $queryForm.find("select.boolOperator:first").clone();

    // remove criteria
    $criteriaTag.remove();

    // delete remove button if only one criteria left
    var list_remove = $queryForm.find(".remove");
    if (list_remove.length == 1){
        $(list_remove[0]).remove();
    }
    // remove all add buttons
    $queryForm.find(".add").remove();
    // give add button to last criteria
    $queryForm.find("p:last").append(add_button);
    // give add button to last criteria
    $queryForm.find("p:first").find("select.boolOperator").replaceWith(first_select);
};


/**
 * Transforms form fields into JSON
 * @param $form
 */
var getFormValues = function ($form) {
    var values = [];
    $form.find("p").each(function(){
        var element_id = $(this).attr("element_id");
        if (typeof element_id !== typeof undefined && element_id !== false) {
            var formValue = Object();
            formValue.id = element_id;
            formValue.selected = $(this).find(".criteriaSelect").is(":checked");
            formValue.value = $(this).find(".valueInput").val();
            formValue.comparison = $(this).find(".valueComparison").val();
            formValue.operator = $(this).find(".boolOperator").val();
            formValue.name = $(this).attr("element_name");
            formValue.type = $(this).attr("element_type");
            values.push(formValue);
        }
    });

    return JSON.stringify(values);
};

/**
 * Save the current query
 */
var saveQuery = function(){
    var templateID = $("#template_id").html();
    var $queryForm = $("#queryForm");
    var formValues = getFormValues($queryForm);
	save_query(formValues, templateID);
};


/**
 * AJAX call, save the query
 */
var save_query = function(formValues, templateID){
    $.ajax({
        url : saveQueryUrl,
        type : "POST",
        dataType: "json",
        data : {
        	formValues: formValues,
        	templateID: templateID
        },
        success: function(data){
            $('#queriesTable').load(reloadBuildQueryUrl +  ' #queriesTable', function() {});
            clear_criteria();
        },
        error: function(data){
            showErrorModal(data.responseText);
        }
    });
};


/**
 * Clear the current criteria in the query builder
 */
var clearCriteria = function(){
	clear_criteria();
};


/**
 * AJAX call, clear current set of criteria
 */
var clear_criteria = function(){
    $.ajax({
        url : clearCriteriaUrl,
        type : "GET",
        dataType: "json",
        data : {

        },
        success: function(data){
        	$("#queryForm").html(data.queryForm);
        }
    });
};


/**
 * Delete all saved queries
 */
var clearQueries = function()
{
    $("#delete-all-queries-modal").modal("show");
    $("#delete-all-queries").on('click', clear_queries);
};


/**
 * AJAX call, delete all saved queries
 */
var clear_queries = function(){
    var templateID = $("#template_id").html();
    $.ajax({
        url : clearQueriesUrl,
        type : "POST",
        dataType: "json",
        data:{
            templateID:templateID
        },
        success: function(data){
        	$('#queriesTable').load(document.URL +  ' #queriesTable', function() {});
        	$("#delete-all-queries-modal").modal("hide");
        }
    });
};

/**
 * Delete a saved query
 * @param savedQueryID
 */
var deleteQuery = function(savedQueryID){
    $("#delete-query-modal").modal("show");
    $("#delete-query").on('click', delete_query);

    $("#saved_query_id").html(savedQueryID);
};


/**
 * AJAX call, delete a saved query
 * @param savedQueryID
 */
var delete_query = function(savedQueryID){
    $.ajax({
        url : deleteQueryUrl,
        type : "POST",
        dataType: "json",
        data : {
        	savedQueryID: $("#saved_query_id").html()
        },
        success: function(data){
        	$('#queriesTable').load(document.URL +  ' #queriesTable', function() {});
        	$("#delete-query-modal").modal("hide");
        }
    });
};


/**
 * Insert a saved query in the query builder
 * @param savedQueryTagID
 */
var addSavedQueryToForm = function(savedQueryTagID){
    var nextTagID = getNextTagID();
    var savedQueryID = savedQueryTagID.substring(5, savedQueryTagID.length); // queryXXX -> XXX
	add_saved_query_to_form(nextTagID, savedQueryID);
};


/**
 * AJAX call, insert a saved query in the query builder
 * @param tagID next tag id
 * @param savedQueryID id of the query to insert
 */
var add_saved_query_to_form = function(tagID, savedQueryID){
    $.ajax({
        url : addQueryCriteriaUrl,
        type : "POST",
        dataType: "json",
        data : {
        	tagID: tagID,
        	savedQueryID: savedQueryID
        },
        success: function(data){
            var $queryForm = $("#queryForm");

            if (data.first){
                // keep only one field if many empty added
                $queryForm.find(":not(:first)").remove();
                // replace first field with query
                $queryForm.find("p:last").replaceWith(data.query);
            }else {
                // remove all add buttons
                $queryForm.find(".add").remove();
                // set query
                $queryForm.find("p:last").after(data.query);

                // update buttons
                var $first_criteria = $($queryForm.find("p:first"));

                if ($first_criteria.find(".remove").length == 0) {
                    // clone existing button
                    var remove_button = $queryForm.find(".remove:first").clone();
                    // append missing button
                    $first_criteria.append(remove_button);
                }
            }
        }
    });
};


/**
 * AJAX call, execute query and redirects to result page
 */
var submit_query = function(){
    //Save form values
    $("input").each(function(){
	    $(this).attr("value", $(this).val());
	});
	$('select option').each(function(){ this.defaultSelected = this.selected; });
	var $queryForm = $("#queryForm");
	var queryForm = $queryForm.prop('outerHTML');
	var templateID = $("#template_id").html();
    var queryID = $("#query_id").html();
    var formValues = getFormValues($queryForm);

    // get query from form
    $.ajax({
        url : getQueryUrl,
        type : "POST",
        dataType: "json",
        data : {
            formValues: formValues,
        	queryForm: queryForm,
            templateID: templateID,
            queryID: queryID,
            orderByField: dataSortingFields
        },
        success: function(data){
            window.location = resultsUrl;
        },
        error: function(data){
            showErrorModal(data.responseText);
        }
    });
};


//Load controllers for build query
$(document).ready(function() {
    var $xsdForm = $("#xsd_form");

    // hide inputs
    $xsdForm.find("input").hide();

    // set on click on elements
    $xsdForm.find("li[select_class=element]").each(function () {
        var $select_id = $(this).attr("select_id");
        var $add = $("<span select_id='"+ $select_id + "' class='can_click fas fa-arrow-right'/>");
        $add.on("click", selectElement);
		$(this).find("input:first").before($add);
    });

    // set on click on parents
    $xsdForm.find("li[select_class=parent]").each(function () {
        var $select_id = $(this).attr("select_id");
        var $add = $("<span select_id='"+ $select_id + "' class='can_click fas fa-arrow-right'/>");
        $add.on("click", selectParent);
		$(this).find("ul:first").before($add);
    });
});
