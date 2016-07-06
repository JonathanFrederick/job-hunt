$(document).ready(function() {
  $(".open_h").click(toggleList);
  $("#LATER").children(".open_h").click();
});

function toggleList() {
  $(this).siblings().toggle();
  ($(this).children("span.open_s").text() === "+") ?
   $(this).children("span.open_s").text("-") :
   $(this).children("span.open_s").text("+");
}
