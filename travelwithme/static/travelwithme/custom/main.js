
document.addEventListener('DOMContentLoaded', function() {
    var options = {
      format: "yyyy-mm-dd",
      container: 'body'
    };
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, options);
});

  // Or with jQuery
  $(document).ready(function(){
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.fixed-action-btn').floatingActionButton({hoverEnabled:true});
    $('.carousel.carousel-slider').carousel({
      fullWidth: true,
      indicators: true
    });
  });

  $(document).ready(function(){
  $('.modal').modal();
});
