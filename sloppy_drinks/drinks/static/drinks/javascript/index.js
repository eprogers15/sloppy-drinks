// Prevent pressing Enter in search bar from submitting the form and reloading the page
$(function () {
  $("#search-bar-form").submit(function () {
    return false;
  });
});

$(".dropdown-sort-item").click(function () {
  let new_sort_order = this.attributes.value.value;
  $("#sort-button").attr("value", new_sort_order);
  $("#sort-button").text("Sort: " + this.innerText);
  $(".active").removeClass("active");
  $(this).addClass("active");
  $("#sort-hidden").attr("value", new_sort_order);
});

$(".dropdown-filter-checkbox").change(function () {
  let checkedValues = [];
  $(".dropdown-filter-checkbox:checked").each(function () {
    checkedValues.push($(this).attr("id"));
  });
  $("#filter-hidden").attr("value", checkedValues);
  let checkedValuesLength = checkedValues.length;
  if (checkedValuesLength > 0) {
    $("#filter-button").text("Ingredients (" + checkedValuesLength + ")");
  } else {
    $("#filter-button").text("Ingredients");
  }
});

// Prevent ingredients filter dropdown from closing when label is clicked
$(document).ready(function () {
  $(".ingredients-dropdown-list").on("click", function (e) {
    e.stopPropagation();
  });
});

// Determine whether or not clear button should be visible in search bar
$("#search-bar").on("input", function () {
  if ($("#search-bar").val()) {
    $("#clear-button").show(); // Show the clear button
    $("#search-bar").addClass("clear-visible"); // Change search bar
  } else {
    $("#clear-button").hide(); // Hide the clear button
    $("#search-bar").removeClass("clear-visible");
  }
});

// Handle change when search bar clear button is clicked
$("#clear-button").click(function () {
  $("#search-bar").val("");
  $("#search-bar").focus();
  $("#clear-button").hide();
  $("#search-bar").removeClass("clear-visible");
  $('#search-bar').change();
});

// Determine whether or not clear filters button should be visible in ingredients filter dropdown menu
$(".dropdown-filter-checkbox").change(function() {
  if ($('.dropdown-filter-checkbox:checked').length > 0) {
    $("#clearFilterButtonAndDivider").show();
  } else {
    $("#clearFilterButtonAndDivider").hide();
  }
});

// Handle change when clear filteres button is clicked
$("#clearFilterButton").click(function() {
  $('.dropdown-filter-checkbox:checked').prop('checked', false);
  $('.dropdown-filter-checkbox').change();
});