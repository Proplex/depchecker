function updateTables() {
  $('.table').each(function() {
    $(this).find('tr:visible').each(function(index) {
      $(this).css(
          'background-color',
          !!(index & 1) ? 'rgba(0,0,0,.05)' : 'rgba(0,0,0,0)');
    });
  });
  AYAYA();
}

function toggleModern() {
  $('.modern').each(function(index) {
    $(this).css('display', $(this).css('display') === 'none' ? 'table-row' : 'none');
  });
  updateTables();
  AYAYA();
}

function AYAYA() {
  $('.table').each(function() {
    console.log($(this).find('tr:visible').length);
    if ($(this).find('tr:visible').length == 1) {
      $(this).addClass("AYAYA");
    } else {
      $(this).removeClass("AYAYA");
    }
  });
}

window.addEventListener('DOMContentLoaded', updateTables());