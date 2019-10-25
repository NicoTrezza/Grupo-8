$(document).ready(function(){
  $('#tabla').pageMe({
    pagerSelector:'#myPager',
    activeColor: 'red',
    prevText:'Anterior',
    nextText:'Siguiente',
    showPrevNext:true,
    hidePageNumbers:false,
    perPage:10
  });
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems);
});

// Initialize collapsible (uncomment the lines below if you use the dropdown variation)
// var collapsibleElem = document.querySelector('.collapsible');
// var collapsibleInstance = M.Collapsible.init(collapsibleElem, options);

// Or with jQuery

$(document).ready(function(){
  $('.sidenav').sidenav();
});

document.addEventListener('DOMContentLoaded', function() {
var elems = document.querySelectorAll('select');
var instances = M.FormSelect.init(elems);
});

// Or with jQuery

$(document).ready(function(){
  var maxField = 10; //Input fields increment limitation
  var addButton = $('.add_button'); //Add button selector
  var wrapper = $('.field_wrapper'); //Input field wrapper
  var fieldHTML = '<form class="col s12"><div class="row"><div class="input-field col s12"><textarea id="ingresarRespuesta" class="materialize-textarea"></textarea><label for="ingresarRespuesta">Ingrese la Respuesta</label></div></div></form>'; //New input field html 
  var x = 1; //Initial field counter is 1
  $(addButton).click(function(){ //Once add button is clicked
      if(x < maxField){ //Check maximum number of input fields
          x++; //Increment field counter
          $(wrapper).append(fieldHTML); // Add field html
      }
  });
  $(wrapper).on('click', '.remove_button', function(e){ //Once remove button is clicked
      e.preventDefault();
      $(this).parent('div').remove(); //Remove field html
      x--; //Decrement field counter
  });
});
