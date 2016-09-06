// example using JsNgram
// https://github.com/sukuba/js-py-ngram-full-text-search

$(document).ready(function(){
  
  var $q = $('#q');
  var ignore = /[\s,.，．、。]/g;
  
  JsNgram.errorSelector = $('#error');
  JsNgram.resultSelector = $('#result');
  JsNgram.size = 2;
  JsNgram.indexBase = 'idx/';
  JsNgram.textBase = 'txt/';
  JsNgram.keySeparator = '/';
  JsNgram.verbose = 1;
  
  function enterSearch() {
    var what = $q.val();
    if(ignore.test(what)) {
      setTimeout(
        function(){
          JsNgram.appendErrorMessage(' / Blanks, periods, or other unsupported characters were removed before search.');
        }, 
        2400
      );
      what = what.replace(ignore, '');
      $q.val(what);
    }
    JsNgram.search(what);
  }
  
  $('#search').click(function(){
    enterSearch();
  });
  
  $q.keypress(function(k){
    if(k.which == 13) {
      enterSearch();
      return(false);
    }
  });
  
  $q.focus();
});
