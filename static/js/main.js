function updateTables() {
  $('tr:visible').each(function(index) {
    $(this).css(
        'background-color',
        !!(index & 1) ? 'rgba(0,0,0,.05)' : 'rgba(0,0,0,0)');
  });
}