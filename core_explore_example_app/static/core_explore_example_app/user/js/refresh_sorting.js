/**
 * Init auto refresh of displayed Data
 */
$(document).ready(function() {
    // waiting for the end of the AJAX call result DOM injection
    var MAX_INTERVAL_ITER = 10;
    var iteration = 0;

    var interval = setInterval(function() {
        iteration++;
        if (iteration >= MAX_INTERVAL_ITER) clearInterval(interval);
        if ($(".filter-dropdown-menu").length > 0) {
            clearInterval(interval);
            initListener();
        }
    }, 500);
});

/**
 * Create the listener to trigger the data list refresh
 */
function initListener() {
    $(".dropdown-menu.tools-menu.filter-dropdown-menu li").click(debounce(function() {
        update_query();
    }, 2000));
}

/**
 * AJAX call, save query with the updated sorting fields
 */
var update_query = function() {
    var templateID = $("#template_id").html();
    var queryID = $("#query_id").html();
    // create the query update sorting structure
    var orderByField = $("#id_order_by_field").val();

    // get query from form
    $.ajax({
        url: getQueryUrl,
        type: "POST",
        dataType: "json",
        data: {
            orderByField: orderByField,
            templateID: templateID,
            queryID: queryID
        },
        success: function(data) {
            location.reload();
        },
        error: function(data) {
            showErrorModal(data.responseText);
        }
    });
};