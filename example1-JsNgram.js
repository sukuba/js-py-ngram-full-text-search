// example using JsNgram
// https://github.com/sukuba/js-py-ngram-full-text-search

$(document).ready(function(){
  
  var $q = $('#q');
  
  JsNgram.errorSelector = $('#error');
  JsNgram.resultSelector = $('#result');
  JsNgram.size = 2;
  JsNgram.indexBase = 'hoge/';
  JsNgram.textBase = 'txt/';
  JsNgram.keySeparator = '-';
  JsNgram.verbose = 3;
  
  function enterSearch() {
    var what = $q.val();
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
  
});
