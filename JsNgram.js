// N-gram full text search client module
// https://github.com/sukuba/js-py-ngram-full-text-search

/*############
require JQuery
############*/

/* enable this when you wish to run within Node.js ...
define(function(){
*/

/*############
Namespace: JsNgram
  without Node.js, this will create a global entry point JsNgram.
############*/

var JsNgram = new function(){
  
  /*############
  Properties: 
    size: size of N-gram.
    indexBase: base url to refer N-gram index files.
    textBase: base url to refer text files.
    keySeparator: '/' for subdirectory keys, '-' for flat file keys.
    keyExt: file ext, such as '.json'.
    previewSize: text length shown as preview; see LoadFullText and makeTextHilighted.
    outputLimiter: doc or hit counts shown at once.
    outputLimiter1st: hit counts shown at the 1st time with doc.
    linkAttributes: additional atrributes to document link.
    resultSelector: JQuery selector pointing result wrapper.
    errorSelector: JQuery selector pointing error message box.
    ajaxJson: JQuery ajax settings for json.
    ajaxText: JQuery ajax settings for text.
    titleInfo: document information data such as title, authors and so on.
    work: structured data shared between callbacks while searching.
    verbose: level of verbosity to show debug information on console.
   * message constants
    msgOnSearch, ignoreBlank, resultNone, resultCount, askToShowFound,
    askToShowNextDocs, askToShowNextHits, partialMatches
  ############*/
  
  var _my = this;
  var _verbose;
  var _blankText = '';
  
  Object.defineProperties(_my, {
    "size": { value: 2, writable: true, configurable: true }, 
    "indexBase": { value: 'idx/', writable: true, configurable: true }, 
    "textBase": { value: 'txt/', writable: true, configurable: true }, 
    "keySeparator": { value: '/', writable: true, configurable: true }, 
    "keyExt": { value: '.json', writable: true, configurable: true }, 
    "previewSize": { value: 240, writable: true, configurable: true }, 
    "outputLimiter": { value: 100, writable: true, configurable: true }, 
    "outputLimiter1st": { value: 1, writable: true, configurable: true }, 
    "linkAttributes": { value: {
                          target: '_blank',
                          type: 'text/plain; charset=utf-8'
                          // unfortunately, safari doesn't use above advisory,
                          // but hoping it does in the future.
                          // also, html5 doesn't support charset attribute.
                        }, 
                        writable: true, configurable: true }, 
    "resultSelector": { value: undefined, writable: true, configurable: true }, 
    "errorSelector": { value: undefined, writable: true, configurable: true }, 
    "ajaxJson": { value: {
                    dataType: 'json',
                    mimeType: 'text/plain; charset=utf8'
                  }, 
                  writable: true, configurable: true }, 
    "ajaxText": { value: {
                    dataType: 'text',
                    mimeType: 'text/plain; charset=utf8'
                  }, 
                  writable: true, configurable: true }, 
    "msgOnSearch": { value: 'Searching ... please, wait.', writable: true, configurable: true }, 
    "ignoreBlank": { value: 'Blank query text is ignored.', writable: true, configurable: true }, 
    "resultNone": { value: 'Nothing found.', writable: true, configurable: true }, 
    "resultCount": { value: '%% hits in %% documents.', writable: true, configurable: true }, 
    "askToShowFound": { value: 'Want partial matches?', writable: true, configurable: true }, 
    "askToShowNextDocs": { value: 'More documents after %% ... ', writable: true, configurable: true }, 
    "askToShowNextHits": { value: '+ More hits after %% ... ', writable: true, configurable: true }, 
    "partialMatches": { value: '(partial matches)', writable: true, configurable: true }, 
    "titleInfo": { value: {}, writable: true, configurable: true }, 
    "work": { value: {}, writable: true, configurable: true }, 
    "verbose": { get: function(){ return _verbose; },
                 set: function(verbose){
                   if(!(verbose in [0,1,2,3])) {
                     throw "verbose value is out of range.";
                   }
                   if(_verbose == verbose) { return; }
                   _verbose = verbose;
                   _my.log = new Log(verbose);
                 }, 
                 configurable: true }
  });
  
  /*############
  inner Class: Log
    console logger with verbosity.
  ############*/
  
  function Log(verbose){
    function nop(){}
    function log(msg){ console.log.apply(console, arguments); }
    this.v0 = log;
    this.v1 = (verbose < 1) ? nop : log;
    this.v2 = (verbose < 2) ? nop : log;
    this.v3 = (verbose < 3) ? nop : log;
  }
  
  /*############
  kickup default logger (this.log) with verbose = 0
  ############*/
  _my.verbose = 0;
  
  /*############
  Method: search(text)
    perform search on text and insert results in html.
    this will be called when a search button is pushed.
  ############*/
  
  function search(text) {
    if(text == _blankText) {
      _my.log.v1(_my.ignoreBlank);
      return;
    }
    _my.clearErrorMessage();
    _my.clearSearchResult();
    _my.showOnSearchMessage();
    _my.appendSearchResult(_my.normalizeText(text));
  }
  _my.search = search;
  
  /*############
  Method: normalizeText(text)
    normalize text on search.
  ############*/
  
  function normalizeText(text) {
    return(text.toLowerCase());
  }
  _my.normalizeText = normalizeText;
  
  /*############
  Method: showErrorMessage(msg)
    replace content of error box with msg.
  ############*/
  
  function showErrorMessage(msg) {
    _my.errorSelector.text(msg);
  }
  _my.showErrorMessage = showErrorMessage;
  
  /*############
  Method: appendErrorMessage(msg)
    append content of error box with msg.
  ############*/
  
  function appendErrorMessage(msg) {
    _my.errorSelector.append(msg);
  }
  _my.appendErrorMessage = appendErrorMessage;
  
  /*############
  Method: showOnSearchMessage()
    show progress message on error box.
  ############*/
  
  function showOnSearchMessage() {
    _my.showErrorMessage(_my.msgOnSearch);
  }
  _my.showOnSearchMessage = showOnSearchMessage;
  
  /*############
  Method: showResultMessage(count)
    show result message on error box.
  ############*/
  
  function showResultMessage(count) {
    var msg;
    if(count[0] > 0) {
      msg = _my.sprintf(_my.resultCount, count);
    } else {
      msg = _my.resultNone
    }
    _my.showErrorMessage(msg);
  }
  _my.showResultMessage = showResultMessage;
  
  /*############
  Method: clearErrorMessage()
    clear content of error box.
  ############*/
  
  function clearErrorMessage() {
    _my.showErrorMessage(_blankText);
  }
  _my.clearErrorMessage = clearErrorMessage;
  
  /*############
  Method: clearSearchResult()
    clear content of result wrapper.
  ############*/
  
  function clearSearchResult() {
    _my.resultSelector.html(_blankText);
  }
  _my.clearSearchResult = clearSearchResult;
  
  /*############
  Method: makeHtmlLink(url, title)
    generate a tag for document link.
  ############*/
  
  function makeHtmlLink(url, title) {
    var tr = [];
    tr.push('<a href="');
    tr.push(url);
    tr.push('"');
    var attr = _my.linkAttributes;
    var key = Object.keys(attr);
    for(var i = 0; i < key.length; i++) {
      var k = key[i];
      tr.push(' ');
      tr.push(k);
      tr.push('="');
      tr.push(attr[k]);
      tr.push('"');
    }
    tr.push('>');
    tr.push(title);
    tr.push('</a>');
    return(tr.join(_blankText));
  }
  _my.makeHtmlLink = makeHtmlLink;
  
  /*############
  Method: makeResultHtml
    generate html for result.
    sub functions:
      header: generate table headers.
      content: generate table contents of hit.
      title: generate table contents of doc info.
      docbox: generate table contents of doc.
  ############*/
  
  _my.makeResultHtml = {
    'header': function(data){
      var headers = (Array.isArray(data) ? data : [data]).join('</span><span>');
      var tr = [];
      tr.push('<div class="head"><span>');
      tr.push(headers);
      tr.push('</span></div>');
      return(tr.join(_blankText));
    },
    'content': function(data){
      var tr = [];
      tr.push('<div class="hit"><span>');
      tr.push(data.join('</span><span>'));
      tr.push('</span></div>');
      return(tr.join(_blankText));
    },
    'title': function(url, title, data){
      var tr = [];
      tr.push('<div class="info"><span>');
      tr.push(_my.makeHtmlLink(url, title));
      if(data.length > 0) {
        tr.push('</span><span>');
        tr.push(data.join('</span><span>'));
      }
      tr.push('</span></div>');
      return(tr.join(_blankText));
    },
    'docbox': function(){
      return('<div class="doc"></div>');
    }
  };
  
  /*############
  Method: makeLinkToNext(isPerfection, selector, doc, start, limit)
    generate html for result.
  ############*/
  
  function makeLinkToNext(isPerfection, selector, doc, start, limit) {
    var colNum = _my.makeResultHtml.columns;
    var face;
    if(!isPerfection && !doc && start == 0) {
      face = _my.askToShowFound;
    } else {
      face = _my.sprintf(doc ? _my.askToShowNextHits : _my.askToShowNextDocs, [start]);
      if(!isPerfection) {
        face += _my.partialMatches;
      }
    }
    
    return($('<div class="ui"></div>').append(
      $('<button type="button"></button>').append(
        face
      ).on('click', function(){
        this.disabled = true;
        _my.showPage(isPerfection, selector, doc, start, limit);
      })
    ));
  }
  _my.makeLinkToNext = makeLinkToNext;
  
  /*############
  Method: escapeHtml(text)
    escape html special characters.
  ############*/
  
  //var escHtmlFrom = new RegExp(/[&<>"'`]/, 'g');
  // safari: Cannot supply flags when constructing one RegExp from another.
  var escHtmlFrom = /[&<>"'`]/g;
  var escHtmlTo = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '`': '&#x60;'
  }
  
  function escapeHtml(text) {
    return(text.replace(escHtmlFrom, function(x){return escHtmlTo[x];}));
  }
  _my.escapeHtml = escapeHtml;
  
  /*############
  Method: sprintf(format, arr)
    insert data of arr into format at %%.
  ############*/
  
  function sprintf(format, arr) {
    var s = format;
    for(var i = 0; i < arr.length; i++) {
      s = s.replace(/%%/, arr[i]);
    }
    return(s);
  }
  _my.sprintf = sprintf;

  /*############
  Method: makeTextHilighted(text, at, hiLen, outLen)
    generate html with text hilighted.
  ############*/
  
  function makeTextHilighted(text, at, hiLen, outLen) {
    if(text == _blankText) { return(_blankText); }
    
    var outLen = typeof outLen !== 'undefined' ? outLen : 240;
    // ES6 can use default value with declaring 'outLen=100', but be conservative.
    
    var start = at - Math.floor((outLen - hiLen) / 2);
    if(start < 0) { start = 0; }
    var x = text.substr(start, outLen);
    var pos = at - start;
    var xx = [
                escapeHtml(x.substr(0, pos)),
                '<b>',
                escapeHtml(x.substr(pos, hiLen)),
                '</b>',
                escapeHtml(x.substring(pos + hiLen, outLen))
              ];
    return(xx.join(_blankText));
  }
  _my.makeTextHilighted = makeTextHilighted;
  
  /*############
  Method: failMessageHandler(xhr, ajaxOptions, thrownError)
    handle the failure of ajax and show error message.
  ############*/
  
  function failMessageHandler(xhr, ajaxOptions, thrownError) {
    var msg =xhr.status + ' / ' + thrownError;
    var msg2 = this.url + ' / ' + msg;
    _my.log.v0(msg2);
    //_my.showErrorMessage(msg2);
    _my.showResultMessage(0);
    // notify end-user just result was 0, avoiding show them technical messages.
  }
  _my.failMessageHandler = failMessageHandler;
  
  /*############
  Method: encodeKey(text)
    convert text into hex byte string array of unicode.
  ############*/
  
  function encodeKey(text) {
    return(
      _my.cutString2by2(_my.toUnicodeArray(text).join(_blankText)).join(_my.keySeparator)
    );
  }
  _my.encodeKey = encodeKey;
  
  /*############
  Method: toUnicodeArray(text)
    convert text into strictly 4 digit hex string array of unicode.
  ############*/
  
  function toUnicodeArray(text) {
    var encodedArr = [];
    for(var i = 0; i < text.length; i++) {
      var twoByte = ('0000' + text.charCodeAt(i).toString(16)).slice(-4);
      encodedArr.push(twoByte);
    }
    return(encodedArr);
  }
  _my.toUnicodeArray = toUnicodeArray;
  
  /*############
  Method: cutString2by2(text)
    convert text into two by two character array.
  ############*/
  
  function cutString2by2(text) {
    var twoByTwo = [];
    for(var i = 0; i < text.length; i+=2) {
      twoByTwo.push(text.substr(i, 2));
    }
    return(twoByTwo);
  }
  _my.cutString2by2 = cutString2by2;
  
  /*############
  Method: indexFileName(text)
    get json file name of index to find text.
  ############*/
  
  function indexFileName(text) {
    return(_my.indexBase + _my.encodeKey(text) + _my.keyExt);
  }
  _my.indexFileName = indexFileName;
  
  /*############
  Method: fulltextFileName(id)
    get json file name of full text body.
  ############*/
  
  function fulltextFileName(id) {
    return(_my.textBase + id);
  }
  _my.fulltextFileName = fulltextFileName;
  
  /*############
  Method: loadIndexFile(text)
    load index json file to find text.
  ############*/
  
  function loadIndexFile(text) {
    return($.ajax(_my.indexFileName(text), _my.ajaxJson).fail(_my.failMessageHandler));
  }
  _my.loadIndexFile = loadIndexFile;
  
  /*############
  Method: loadFullText(selector, docId, pos, hiLen, tag)
    load full text at id (url) and show at result.
  ############*/
  
  function loadFullText(selector, docId, pos, hiLen, tag) {
    var contentFn = _my.makeResultHtml.content;
    var hilightFn = _my.makeTextHilighted;
    var esc = _my.escapeHtml;
    var outLen = _my.previewSize;
    
    // wrap $.ajax by $.when, 
    // because when multiple deferreds contains a fail, 
    // the surrounding when returns immediately, 
    // and that will cause unexpected sequence at caller, namely, 'showPage'.
    return($.when(
      $.ajax(_my.fulltextFileName(docId), _my.ajaxText).done(function(result){
        var x = hilightFn(result, pos, hiLen, outLen);
        //selector.append(contentFn([tag, esc(docId), pos, x]));
        selector.append(contentFn([x, pos+1]));
      }).fail(function(xhr, ajaxOptions, thrownError){
        //selector.append(contentFn([tag, esc(docId), pos, _blankText]));
        selector.append(contentFn([_blankText, pos+1]));
      })
    ));
  }
  _my.loadFullText = loadFullText;
  
  /*############
  Method: loadTitleInfo(selector, docId)
    show document title at result.
  ############*/
  
  function loadTitleInfo(selector, docId) {
    var titleFn = _my.makeResultHtml.title;
    var url = _my.convertIdToUrl(docId);
    var info = _my.titleInfo[docId];
    var title = docId;
    if(info && info.title) {
      title = info.title;
    }
    title = _my.escapeHtml(title);
    
    return(selector.append(titleFn(url, title, [])));
  }
  _my.loadTitleInfo = loadTitleInfo;
  
  /*############
  Method: loadHeader(arr)
    show header at result.
  ############*/
  
  function loadHeader(arr) {
    var headerFn = _my.makeResultHtml.header;
    var resultSelector = _my.resultSelector;
    
    return(resultSelector.append(headerFn(arr)));
  }
  _my.loadHeader = loadHeader;
  
  /*############
  Method: convertIdToUrl(docId)
    convert docId to URL.
  ############*/
  
  function convertIdToUrl(docId) {
    return(_my.encodeURI(_my.fulltextFileName(docId)));
  }
  _my.convertIdToUrl = convertIdToUrl;
  
  /*############
  Method: encodeURI(uri)
    escape uri string.
  ############*/
  
  _my.encodeURI = encodeURI;
  
  /*############
  Method: findPerfection(x, n)
    pick up perfect match from sorted result of N-gram partial matches.
    x: sorted result of match (by document)
    n: required count for perfect match
  ############*/
  
  function findPerfection(x, n) {
    var workHits = _my.work.result.hits.perfection; // hits by [pos, doc]
    var bag = {};
    var ids = Object.keys(x);
    for(var i = 0; i < ids.length; i++) { // loop by document
      var docId = ids[i];
      var xx = x[docId];
      var seqs = Object.keys(xx);  // N-gram keys in the current document
      if(seqs.length < n) { continue; }  // at least, should have all keys.
      
      // find a key that has minimum occurrences.
      // this will help performance.
      var mini = -1;
      var miniLength = Number.MAX_SAFE_INTEGER;
      for(var j = 0; j < n; j++) {
        if(xx[j].length < miniLength) {
          miniLength = xx[j].length;
          mini = j;
        }
      }
      
      // loop by occurence at mini.
      var xxx = xx[mini];
      for(var k = 0; k < xxx.length; k++) {
        var p = xxx[k] - mini;  // valid sequences have same p values.
        for(var j = 0; j < n; j++) {
          if(j == mini) { continue; }
          var q = xx[j].indexOf(p + j);
          if(q == -1) { break; }  // not valid
        }
        if(j == n) { // valid
          if(!(docId in bag)) {
            bag[docId] = [];
            workHits[1]++;
          }
          bag[docId].push([p]);
          // put in nested array to make it as same as 'found'
          workHits[0]++;
        }
      }
    }
    return(bag);
  }
  _my.findPerfection = findPerfection;
  
  /*############
  Method: startWork(what)
    start up with the property work.
  ############*/
  
  function startWork(what) {
    //clearWork();
    var work = {};
    work['what'] = what;
    work['nWhat'] = what.length;
    work['nGram'] = _my.size;
    work['nIter'] = work['nWhat'] - work['nGram'] + 1;
    work['texts'] = _my.generateTexts(work);
    work['nText'] = work['texts'].length;
    work['result'] = {'hits':{'found':[0,0],'perfection':[0,0]}};
    work['deferred'] = _my.generateDeferred(work);
    // the last one submits multiple ajax requests.
    return(work);
  }
  _my.startWork = startWork;
  
  /*############
  Method: clearWork()
    clear the property work.
  ############*/
  
  function clearWork() {
    _my.work = {};
  }
  _my.clearWork = clearWork;
  
  /*############
  Method: generateTexts(work)
    generate N-gram splitted keyword texts as array.
  ############*/
  
  function generateTexts(work) {
    var texts = [];
    // single character (or shoter than N-gram size) text
    // will not go into this loop.
    for(var i = 0; i < work.nIter; i++) {
      texts.push(work.what.substr(i, work.nGram));
    }
    
    // for a short word
    if(work.nWhat < work.nGram) {
      texts.push(work.what);
      _my.log.v1('adjusted: ', texts);
    }
    return(texts);
  }
  _my.generateTexts = generateTexts;
  
  /*############
  Method: generateDeferred(work)
    generate ajax request array for each N-gram keyword after submit.
  ############*/
  
  function generateDeferred(work) {
    var deferred = [];
    for(var i = 0; i < work.nText; i++) {
      deferred.push(_my.loadIndexFile(work.texts[i]));
    }
    return(deferred);
  }
  _my.generateDeferred = generateDeferred;
  
  /*############
  Method: showLinkToNext(isPerfection, selector, doc, start, limit)
    privide a link to show found.
  ############*/
  
  function showLinkToNext(isPerfection, selector, doc, start, limit) {
    return function(){
      selector.append(_my.makeLinkToNext(isPerfection, selector, doc, start, limit));
    };
  }
  _my.showLinkToNext = showLinkToNext;
  
  /*############
  Method: showFoundUnlimited(perfection)
    show found result. both for perfection and found (partial match).
    OBSOLETE version of showFound, that shows results without limit.
    maybe, useful for debugging small amount of data, 
    but the browser will crash when given a lot of data (too many uses of ajax).
  ############*/
  
  function showFoundUnlimited(isPerfection, selector) {
    var perfection = isPerfection ? _my.work.result.perfection : _my.work.result.found;
    var ids = Object.keys(perfection);
    var n = ids.length;
    _my.log.v1('showFoundUnlimited: ', n);
    
    var what = _my.work.what;
    
    var deferred = [];
    for(var i = 0; i < ids.length; i++) { // loop by document
      var docId = ids[i];
      var poss = perfection[docId];
      for(var k = 0; k < poss.length; k++) {
        var val = poss[k];
        var pos = val[0];
        var text = val[1];
        if(!text) {
          text = what;
        }
        var hiLen = text.length;
        deferred.push(_my.loadFullText(selector, docId, pos, hiLen, text));
      }
    }
    return(deferred);
  }
  
  /*############
  Method: showFoundByHit(perfection, selector, doc, start, limit)
    show found result as a list of hits
  ############*/
  
  function showFoundByHit(perfection, selector, doc, start, limit) {
    var ids = Object.keys(perfection);
    var docNo = ids.indexOf(doc);
    var docId = ids[docNo];
    _my.log.v1('showFoundByHit: ', docNo, doc);
    _my.log.v2(ids);
    
    var poss = perfection[docId];
    var nposs = poss.length;
    var what = _my.work.what;
    var end = limit + start;
    var counter = 0;
    var deferred = [];
    
    for(var k = 0; k < nposs; k++) {
      if(counter++ < start) {
        continue;
      }
      if(counter > end) {
        _my.log.v1('limit: ', start, counter, k);
        return({'deferred':deferred, 'next':end});
      }
      var val = poss[k];
      var pos = val[0];
      var text = val[1];
      if(!text) {
        text = what;
      }
      var hiLen = text.length;
      deferred.push(_my.loadFullText(selector, docId, pos, hiLen, text));
    }
    
    return({'deferred':deferred});
  }
  _my.showFoundByHit = showFoundByHit;
  
  /*############
  Method: showFoundByDoc(isPerfection, perfection, selector, start, limit)
    show found result as a list of docs
  ############*/
  
  function showFoundByDoc(isPerfection, perfection, selector, start, limit) {
    var ids = Object.keys(perfection);
    var n = ids.length;
    _my.log.v1('showFoundByDoc: ', n);
    
    var what = _my.work.what;
    var end = limit + start;
    var counter = 0;
    var deferred = [];
    
    for(var i = 0; i < n; i++) { // loop by document
      if(counter++ < start) {
        continue;
      }
      if(counter > end) {
        _my.log.v1('limit: ', start, counter, i);
        return({'deferred':deferred, 'next':end});
      }
      
      var docId = ids[i];
      var docSelector = $(_my.makeResultHtml.docbox());
      
      deferred.push($.when(selector.append(docSelector)).done(function(){
        $.when(_my.loadTitleInfo(docSelector, docId)).done(function(){
          _my.log.v2('into hits: ', docId);
          _my.showPage(isPerfection, docSelector, docId, 0, _my.outputLimiter1st);
        });
      }));
    }
    
    return({'deferred':deferred});
  }
  _my.showFoundByDoc = showFoundByDoc;
  
  /*############
  Method: showFound(isPerfection, selector, doc, start, limit)
    show found result. both for perfection and found (partial match).
    selector: resultSelector
    doc: null or docId
    start: number to skip records
    limit: number of limit to show at once
  ############*/
  
  function showFound(isPerfection, selector, doc, start, limit) {
    var perfection = isPerfection ? _my.work.result.perfection : _my.work.result.found;
    if(doc) { // show hits inside a doc
      return(_my.showFoundByHit(perfection, selector, doc, start, limit));
    } else { // show docs in perfection with some hits
      return(_my.showFoundByDoc(isPerfection, perfection, selector, start, limit));
    }
  }
  _my.showFound = showFound;
  
  /*############
  Method: showPage(perfection, selector, doc, start, limit)
    wrapper of showFound to enable pager.
    to put 'more' or something.
  ############*/
  
  function showPage(isPerfection, selector, doc, start, limit) {
    var pager = _my.showFound(isPerfection, selector, doc, start, limit);
    var deferred = pager.deferred;
    var nextStart = pager.next;
    var nextCommand;
    if(nextStart) {
      nextCommand = _my.showLinkToNext(isPerfection, selector, doc, nextStart, _my.outputLimiter);
    } else if(isPerfection && !doc) {
      nextCommand = _my.showLinkToNext(false, _my.resultSelector, null, 0, _my.outputLimiter);
    } else {
      return;
    }
    $.when.apply($, deferred).always(nextCommand);
    // this comes to work with the redundant when block in 'loadFullText'.
  }
  _my.showPage = showPage;
  
  /*############
  Method: sortFoundByDocumentPosition(found)
    rebuild found as document, position sorted, as same as perfection.
  ############*/
  
  function sortFoundByDocumentPosition(found) {
    var bag = {};
    var ids = Object.keys(found);
    for(var i = 0; i < ids.length; i++) { // loop by document
      var docId = ids[i];
      var f2 = found[docId];
      var newF2 = [];
      var seqs = Object.keys(f2);  // N-gram keys in the current document
      for(var j = 0; j < seqs.length; j++) { // loop by key
        var seq = seqs[j];
        var f3 = f2[seq];
        var text = _my.work.texts[seq];
        for(var k = 0; k < f3.length; k++) { // loop by position
          var pos = f3[k];
          newF2.push([pos, text]);
        }
      }
      bag[docId] = newF2.sort();
    }
    return(bag);
  }
  _my.sortFoundByDocumentPosition = sortFoundByDocumentPosition;
  
  /*############
  Method: sortResultsByLocation(results)
    rebuild results as location sorted.
  ############*/
  
  function sortResultsByLocation(results) {
    var log = _my.log;
    var workHits = _my.work.result.hits.found; // hits by [pos, doc]
    var found = {}; // gather results by location.
    
    $.each(results, function(j, result){
      log.v2('j=', j, result);
      if(result == undefined) {
        log.v0('result is undefined. means ajax success with empty result.');
        return(true);
      }
      // result is [data, status_text, jqXHR_object]
      $.each(result[0], function(i, val){
        log.v2('i=', i, val);
        
        var docId = val[0];
        var pos = val[1];
        
        if(!(docId in found)) {
          found[docId] = {};
          workHits[1]++;
        }
        if(!(j in found[docId])) {
          found[docId][j] = [];
        }
        
        found[docId][j].push(pos);
        workHits[0]++;
      });
    });
    return(found);
  }
  _my.sortResultsByLocation = sortResultsByLocation;
  
  /*############
  Method: whenSearchRequestDone(useArgumentsToGetAllAsArray)
    integrate multiple ajax results of N-gram search.
  ############*/
  
  function whenSearchRequestDone(useArgumentsToGetAllAsArray) {
    var log = _my.log;
    var work = _my.work;
    
    // adjust nesting level when length equals 1.
    var results = (work.deferred.length > 1) ? arguments : [arguments];
    log.v1('whole: ', results.length, results);
    
    var found = _my.sortResultsByLocation(results);
    log.v1(JSON.stringify(found));
    
    var perfection = _my.findPerfection(found, work.nText);
    log.v1(JSON.stringify(perfection));
    
    work.result['perfection'] = perfection;
    work.result['found'] = _my.sortFoundByDocumentPosition(found);
    
    var hits = work.result.hits;
    _my.showResultMessage(hits.perfection);
    log.v1('Perfection:', _my.sprintf(_my.resultCount, hits.perfection));
    log.v1('Found:', _my.sprintf(_my.resultCount, hits.found));
    
    $.when(_my.loadHeader()).done(function(){
      _my.showPage(true, _my.resultSelector, null, 0, _my.outputLimiter);
    });
  }
  _my.whenSearchRequestDone = whenSearchRequestDone;
  
  /*############
  Method: appendSearchResult(what)
    perform search and show result.
  ############*/
  
  function appendSearchResult(what) {
    _my.work = _my.startWork(what);
    // wait until all ajax requests done.
    $.when.apply($, _my.work.deferred).done(_my.whenSearchRequestDone);
  }
  _my.appendSearchResult = appendSearchResult;
  
};

/* enable this when you wish to run within Node.js ...
return(JsNgram);
});
*/
