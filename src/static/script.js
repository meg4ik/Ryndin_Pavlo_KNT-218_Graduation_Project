
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
  if(+countPlus <= 4){
    bcn.innerHTML++;
  }
}

function MinusPrice(ckType){
  var b_id = document.getElementById(ckType.id)
  var bcn_second_part = b_id.id.slice(16)

  var bcn = document.getElementById("buttonCountNumber"+bcn_second_part)
  let countPlus = bcn.innerHTML;
  if(+countPlus > 1){
    bcn.innerHTML--;
  }
}