
function ckChangeGenre(ckType){
  var ckName = document.getElementsByClassName(ckType.className)
  for(var i=0; i < ckName.length; i++){
      if (ckName[i].name.slice(0,5)=='Genre'){
        ckName[i].checked = true;
      }
    } 
}

function ckChangeSubgenre(ckType){
  var ckName = document.getElementsByClassName(ckType.className)
  for(var i=0; i < ckName.length; i++){
      if (ckName[i].name.slice(0,8)=='Subgenre'){
        ckName[i].checked = false;
      }
    } 
}

$('[data-toggle="popover"]').popover({
  html: true,
  content: function () {
      var content = $(this).attr("data-popover-content");
      return $(content).find(".popover-body").clone();
  }
})

function ReplyComment(ckType){
  var form = document.getElementsByName(ckType.Name)
  form.classList.add('open');
}


function PlusPrice(ckType){
  var b_id = document.getElementById(ckType.id)
  var bcn_second_part = b_id.id.slice(15)

  var bcn = document.getElementById("buttonCountNumber"+bcn_second_part)
  let countPlus = bcn.innerHTML;

  var calc = document.getElementById("calculation"+bcn_second_part)
  var price = document.getElementById("price"+bcn_second_part)

  var total = document.getElementById("totalsum")
 
  if(+countPlus <= 4){
    bcn.innerHTML++;
    calc.innerHTML="$"+(parseInt(calc.innerHTML.slice(1))+parseInt(price.innerHTML.slice(1)));
    total.innerHTML="Total: $"+(parseInt(total.innerHTML.slice(8))+parseInt(price.innerHTML.slice(1)));
  }
}

function MinusPrice(ckType){
  var b_id = document.getElementById(ckType.id)
  var bcn_second_part = b_id.id.slice(16)

  var bcn = document.getElementById("buttonCountNumber"+bcn_second_part)
  let countMinus = bcn.innerHTML;

  var calc = document.getElementById("calculation"+bcn_second_part)
  var price = document.getElementById("price"+bcn_second_part)

  var total = document.getElementById("totalsum")

  if(+countMinus > 1){
    bcn.innerHTML--;
    calc.innerHTML="$"+(parseInt(calc.innerHTML.slice(1))-parseInt(price.innerHTML.slice(1)));
    total.innerHTML="Total: $"+(parseInt(total.innerHTML.slice(8))-parseInt(price.innerHTML.slice(1)));
  }
}

$(function() {
  $('form.ajax_del_game').submit(function(e) {
    var $form = $(this);
    $.ajax({
      type: 'DELETE',
      url: $form.attr('action'),
      data: $form.serialize()
    })
    e.preventDefault();
  });
});

$('div[data-href]').on("click", function() {
  document.location = $(this).data('href');
});