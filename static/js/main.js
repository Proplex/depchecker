function updateTables() {
  $('.table').each(function() {
    $(this).children('tr:visible').each(function(index) {
      $(this).css(
          'background-color',
          !!(index & 1) ? 'rgba(0,0,0,.05)' : 'rgba(0,0,0,0)');
    });
  });
}

function toggleModern() {
  $('.modern').each(function(index) {
    $(this).css('display', $(this).css('display') === 'none' ? 'table-row' : 'none');
  });
  updateTables();
}
window.addEventListener('DOMContentLoaded', updateTables());