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