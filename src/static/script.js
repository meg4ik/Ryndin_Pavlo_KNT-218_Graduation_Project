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

$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});