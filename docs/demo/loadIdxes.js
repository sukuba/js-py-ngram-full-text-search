// example using JsNgram
// https://github.com/sukuba/js-py-ngram-full-text-search

$(document).ready(function(){
  // This file is not a part of demo itself.
  // It is a part of document,
  // to generate links to files in idx folder
  // loading idxes.json.
  
  var $idx = $('#idx');
  var file = 'idxes.json';
  var idxDir = 'idx/';
  
  function toUnicodeStr(x) {
    var extRemoved = x.replace(/.json$/, '');
    var bytes = extRemoved.split('/');
    var twoBytes = [];
    for(var i = 0; i < bytes.length; i+=2) {
      twoBytes.push(parseInt(bytes[i], 16) * 256 + parseInt(bytes[i+1], 16));
    }
    var text = String.fromCharCode.apply(String, twoBytes);
    return(text);
  }
  
  function makeHtml(x) {
    // no needs to escape x in this time.
    var li =[
      '<li>',
      '<span style="',
      'background-color: #ffb3e6;',
      'display: inline-block;',
      'margin: 0.3rem;',
      'width: 6rem;',
      'text-align: center;',
      '">',
      toUnicodeStr(x),
      '</span>',
      '<a href="',
      idxDir,
      x,
      '"',
      ' target="_blank"',
      ' type="text/plain; charset=utf-8"',
      '>',
      idxDir,
      x,
      '</a>',
      '</li>'
    ];
    return(li.join(''));
  }
  
  $.ajax(file, JsNgram.ajaxJson).done(function(result){
    $.each(result, function(index, value){
      $idx.append(makeHtml(value));
    });
  }).fail(function(xhr, ajaxOptions, thrownError){
    var msg =xhr.status + ' / ' + thrownError;
    var msg2 = this.url + ' / ' + msg;
    console.log(msg2);
  });
});
