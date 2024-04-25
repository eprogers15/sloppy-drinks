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

$(".dropdown-sort-item").click(function() {
  let new_sort_order = this.attributes.value.value;
  $("#sort-button").attr("value", new_sort_order);
  $("#sort-button").text("Sort by: " + this.innerText);
  $(".active").removeClass("active");
  $(this).addClass("active");
  $("#sort-hidden").attr("value", new_sort_order);
  $("#filter-button").attr("hx-vals", '{"sort": "' + new_sort_order + '"}');
});