
document.addEventListener('DOMContentLoaded', function() {
    var options = {
      format: "yyyy-mm-dd"
    };
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, options);
});

  // Or with jQuery
  $(document).ready(function(){
    $('select').formSelect();
    $('.fixed-action-btn').floatingActionButton({hoverEnabled:true});
    $('.carousel.carousel-slider').carousel({
      fullWidth: true,
      indicators: true
    });
  });



