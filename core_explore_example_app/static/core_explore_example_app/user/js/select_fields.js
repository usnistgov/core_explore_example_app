// Save the selected fields
var saveFields = function()
{
    var templateID = $("#template_id").html();
    var $xsd_form = $("#xsd_form");
    // Need to Set input values explicitly before sending innerHTML for save
    var elements = $xsd_form.find("input");
    for(var i = 0; i < elements.length; i++) {
    	// sent attribute to property value
    	elements[i].setAttribute("value", elements[i].checked);
    	if(elements[i].checked == true)
    	{
    		elements[i].setAttribute("checked","checked");
    	}
    }
    $('select option').each(function(){ this.defaultSelected = this.selected; });
    var formContent = $xsd_form.html();
    save_fields(formContent, templateID);
};


/**
 * AJAX call, save the selected fields and redirects to perform search
 * @param formContent
 * @param templateID
 */
var save_fields = function(formContent, templateID){
	$.ajax({
        url : saveFieldsUrl,
        type : "POST",
        dataType: "json",
        data : {
        	formContent : formContent,
            templateID: templateID
        },
        success: function(data){
        	window.location = buildQueryUrl;
        }
    });
};

//Load controllers for enter data
$(document).ready(function() {
    $('.btn.save-fields').on('click', saveFields);
});