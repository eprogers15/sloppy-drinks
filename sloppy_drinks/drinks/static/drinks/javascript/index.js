// Reset starting point of body content based on navbar height after button click
$(".navbar-toggler").click(function () {
  setTimeout(function () {
    let padding = $("nav").outerHeight(true) + "px";
    $("body").css("paddingTop", padding);
  }, 500);
});

// Reset starting point of body content based on navbar height after window resizing
$(window).resize(function () {
  setTimeout(function () {
    let padding = $("nav").outerHeight(true) + "px";
    $("body").css("paddingTop", padding);
  }, 500);
});

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
