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

$(".dropdown-item").click(function() {
  let new_sort_order = this.attributes.value.value;
  $("#sort-button").attr("value", new_sort_order);
  $(".active").removeClass("active");
  $(this).addClass("active");
  $("#search-bar").attr("hx-vals", '{"sort": "' + new_sort_order + '"}');
});

function getSortOrder() {
  let sort_order = $("#sort-button").attr("value");
  return sort_order;
};