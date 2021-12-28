$(function() {
  $('form.ajax_put').submit(function(e) {
    var $form = $(this);
    $.ajax({
      type: 'PUT',
      url: $form.attr('action'),
      data: $form.serialize()
    })
    e.preventDefault();
  });
});

$(function() {
  $('form.ajax_del').submit(function(e) {
    var $form = $(this);
    $.ajax({
      type: 'DELETE',
      url: $form.attr('action'),
      data: $form.serialize()
    })
    e.preventDefault();
  });
});

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