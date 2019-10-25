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

/////////////////////////////////////////////////
function agregarOpcionAselect(select,value,text)
{
    var opt = document.createElement('option');
    opt.value = value;
    opt.appendChild( document.createTextNode(text));
    select.appendChild(opt); 
    
}

function selectTipoPreguntaOnChange(e) 
{

    
    var selectTipoPregunta = e.target;
    var contenedor = selectTipoPregunta.parentNode;
    var botonAgregarRespuesta = contenedor.lastChild;


    if(selectTipoPregunta.selectedIndex == 2) botonAgregarRespuesta.style.display = "inline";
    else
    {

        botonAgregarRespuesta.style.display = "none";

        var nodosAEliminar = [];
        for(var child=contenedor.childNodes[5]; child != botonAgregarRespuesta; child=child.nextSibling)
        {
            nodosAEliminar.push(child);
            
        }

        nodosAEliminar.forEach(function(element) 
        {
            element.remove();
        });

    } 
}

function agregarPregunta(e) 
{



    if( typeof agregarPregunta.idPregunta == 'undefined' ) {
        agregarPregunta.idPregunta = 0;
    }

    var idPregunta = agregarPregunta.idPregunta++;

  
    var form = document.getElementById("form");

    var contenedor = document.createElement('div');

    var textoPregunta = document.createElement('input');
    textoPregunta.type= "text";
    textoPregunta.name = idPregunta + "-texto";

    var labelTipoPregunta = document.createElement('label');
    labelTipoPregunta.innerHTML= "Tipo:";

    var selectTipoPregunta = document.createElement('select');
    selectTipoPregunta.addEventListener("change", selectTipoPreguntaOnChange);
    selectTipoPregunta.name = idPregunta + "-tipo";

    agregarOpcionAselect(selectTipoPregunta,"verdadera","verdadera");
    agregarOpcionAselect(selectTipoPregunta,"falsa","falsa");
    agregarOpcionAselect(selectTipoPregunta,"choice","choice");

    var botonEliminarPregunta = document.createElement('button');
    botonEliminarPregunta.type= "button";
    botonEliminarPregunta.innerHTML = "eliminar"
    botonEliminarPregunta.className = "btn waves-effect waves-light"
    botonEliminarPregunta.addEventListener("click", eliminarPregunta);


    var botonAgregarRespuesta = document.createElement('button');
    botonAgregarRespuesta.type= "button";
    botonAgregarRespuesta.innerHTML = "agregar respuesta"
    botonAgregarRespuesta.style.display = "none";
    botonAgregarRespuesta.name = idPregunta;
    botonAgregarRespuesta.addEventListener("click", agregarRespuesta);

    contenedor.appendChild(textoPregunta);
    contenedor.appendChild(labelTipoPregunta);
    contenedor.appendChild(selectTipoPregunta);
    contenedor.appendChild(botonEliminarPregunta);
    contenedor.appendChild(document.createElement('br'));
    contenedor.appendChild(botonAgregarRespuesta);
    form.insertBefore(contenedor,e.target);
    

}



function agregarRespuesta(e)
{


    if( typeof agregarRespuesta.idRespuesta == 'undefined' ) {
        agregarRespuesta.idRespuesta = 0;
    }


    var idRespuesta = agregarRespuesta.idRespuesta++;
    var botonAgregarRespuesta = e.target;
    var idPregunta = botonAgregarRespuesta.name;
    var contenedor = botonAgregarRespuesta.parentNode;


    var textoRespuesta =  document.createElement('input');
    textoRespuesta.type = "text";
    textoRespuesta.name = idPregunta + "-" + idRespuesta + "-texto";

    var botonEliminarRespuesta = document.createElement('button');
    botonEliminarRespuesta.type= "button";
    botonEliminarRespuesta.innerHTML = "eliminar"
    botonEliminarRespuesta.addEventListener("click", eliminarRespuesta);


    var labelRadioRespuestaCorrecta = document.createElement('label');
    labelRadioRespuestaCorrecta.innerHTML= "correcta:";
    

    var radioRespuestaCorrecta =  document.createElement('input');
    radioRespuestaCorrecta.type = "radio";
    radioRespuestaCorrecta.name = idPregunta + "-correcta";
    radioRespuestaCorrecta.value = idRespuesta;


    contenedor.insertBefore(textoRespuesta,e.target);
    contenedor.insertBefore(botonEliminarRespuesta,e.target);
    contenedor.insertBefore(labelRadioRespuestaCorrecta,e.target);
    contenedor.insertBefore(radioRespuestaCorrecta,e.target);
    contenedor.insertBefore(document.createElement('br'),e.target);



}

function eliminarPregunta(e)
{
    e.target.parentNode.remove();

}

function eliminarRespuesta(e)
{
    e.target.previousSibling.remove();
    e.target.nextSibling.remove();
    e.target.nextSibling.remove();
    e.target.nextSibling.remove();
    e.target.remove();

}

//////////////////////////////////////////
function selectCursadaOnChange()
{
    var selectCursada = document.getElementById("select-cursada");
    window.location.replace("/crearevaluacion?cursada=" + selectCursada.value);

}
function selectExamenOnchange()
{
    var selectCursada = document.getElementById("select-cursada");
    var selectExamen = document.getElementById("select-examen");
    window.location.replace("/crearevaluacion?cursada=" + selectCursada.value +"&examen="+selectExamen.value);

}