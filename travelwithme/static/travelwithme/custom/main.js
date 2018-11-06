
  document.addEventListener('DOMContentLoaded', function() {
    var options = {
      format: "dd, mm yyyy"
    };
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, options);
  });

  // Or with jQuery

       