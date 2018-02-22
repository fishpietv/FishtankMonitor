AmCharts.translations.dataLoader={};AmCharts.addInitHandler(function(chart){if(undefined===chart.dataLoader||!isObject(chart.dataLoader))
chart.dataLoader={};var version=chart.version.split('.');if((Number(version[0])<3)||(3===Number(version[0])&&(Number(version[1])<13)))
return;var l=chart.dataLoader;l.remaining=0;l.percentLoaded={};var defaults={'async':true,'format':'json','showErrors':true,'showCurtain':true,'noStyles':false,'reload':0,'timestamp':false,'delimiter':',','skip':0,'skipEmpty':true,'emptyAs':undefined,'useColumnNames':false,'init':false,'progress':false,'reverse':false,'reloading':false,'complete':false,'error':false,'headers':[],'chart':chart};l.loadData=function(){if('stock'===chart.type){setTimeout(function(){if(0>chart.panelsSettings.startDuration){l.startDuration=chart.panelsSettings.startDuration;chart.panelsSettings.startDuration=0;}
for(var x=0;x<chart.dataSets.length;x++){var ds=chart.dataSets[x];if(undefined!==ds.dataLoader&&undefined!==ds.dataLoader.url){callFunction(ds.dataLoader.init,ds.dataLoader,chart);ds.dataProvider=[];applyDefaults(ds.dataLoader);loadFile(ds.dataLoader.url,ds,ds.dataLoader,'dataProvider');}
if(undefined!==ds.eventDataLoader&&undefined!==ds.eventDataLoader.url){callFunction(ds.eventDataLoader.init,ds.eventDataLoader,chart);ds.events=[];applyDefaults(ds.eventDataLoader);loadFile(ds.eventDataLoader.url,ds,ds.eventDataLoader,'stockEvents');}}},100);}else{callFunction(l.init,l,chart);applyDefaults(l);if(undefined===l.url)
return;if(undefined!==chart.startDuration&&(0<chart.startDuration)){l.startDuration=chart.startDuration;chart.startDuration=0;}
if('gauge'===chart.type){if(undefined===chart.arrows)
chart.arrows=[];loadFile(l.url,chart,l,'arrows');}else{if(undefined===chart.dataProvider)
chart.dataProvider=chart.type==='map'?{}:[];loadFile(l.url,chart,l,'dataProvider');}}};l.loadData();function loadFile(url,holder,options,providerKey){if(undefined===providerKey)
providerKey='dataProvider';if(options.showCurtain)
showCurtain(undefined,options.noStyles);l.remaining++;l.percentLoaded[url]=0;if(options.progress!==undefined&&typeof(options.progress)==='function'&&options._progress===undefined){options._progress=options.progress;options.progress=function(percent){l.percentLoaded[url]=percent;var totalPercent=0;var fileCount=0;for(var x in l.percentLoaded){if(l.percentLoaded.hasOwnProperty(x)){fileCount++;totalPercent+=l.percentLoaded[x];}}
var globalPercent=Math.round((totalPercent/fileCount)*100)/ 100;options._progress.call(this,globalPercent,Math.round(percent*100)/ 100, url );};}
AmCharts.loadFile(url,options,function(response){if(false===response){callFunction(options.error,options,chart);raiseError(AmCharts.__('Error loading the file',chart.language)+': '+ url,false,options);}else{if(undefined===options.format){options.format='json';}
options.format=options.format.toLowerCase();switch(options.format){case'json':holder[providerKey]=AmCharts.parseJSON(response);if(false===holder[providerKey]){callFunction(options.error,options,chart);raiseError(AmCharts.__('Error parsing JSON file',chart.language)+': '+ l.url,false,options);holder[providerKey]=[];return;}else{holder[providerKey]=postprocess(holder[providerKey],options);callFunction(options.load,options,chart);}
break;case'csv':holder[providerKey]=AmCharts.parseCSV(response,options);if(false===holder[providerKey]){callFunction(options.error,options,chart);raiseError(AmCharts.__('Error parsing CSV file',chart.language)+': '+ l.url,false,options);holder[providerKey]=[];return;}else{holder[providerKey]=postprocess(holder[providerKey],options);callFunction(options.load,options,chart);}
break;default:callFunction(options.error,options,chart);raiseError(AmCharts.__('Unsupported data format',chart.language)+': '+ options.format,false,options.noStyles);return;}
l.remaining--;if(0===l.remaining){callFunction(options.complete,chart);if(options.async){if('map'===chart.type){chart.validateNow(true);removeCurtain();}else{if('gauge'!==chart.type){chart.addListener('dataUpdated',function(event){if('stock'===chart.type&&!options.reloading&&undefined!==chart.periodSelector){chart.periodSelector.setDefaultPeriod();}
removeCurtain();chart.events.dataUpdated.pop();});}
chart.validateData();if('gauge'===chart.type)
removeCurtain();if(l.startDuration){if('stock'===chart.type){chart.panelsSettings.startDuration=l.startDuration;for(var x=0;x<chart.panels.length;x++){chart.panels[x].startDuration=l.startDuration;chart.panels[x].animateAgain();}}else{chart.startDuration=l.startDuration;if(chart.animateAgain!==undefined)
chart.animateAgain();}}}}}
if(options.reload){if(options.timeout)
clearTimeout(options.timeout);options.timeout=setTimeout(loadFile,1000*options.reload,url,holder,options);options.reloading=true;}}});}
function postprocess(data,options){if(undefined!==options.postProcess&&isFunction(options.postProcess))
try{return options.postProcess.call(l,data,options,chart);}catch(e){raiseError(AmCharts.__('Error loading file',chart.language)+': '+ options.url,false,options);return data;}else
return data;}
function isObject(obj){return'object'===typeof(obj);}
function isFunction(obj){return'function'===typeof(obj);}
function applyDefaults(obj){for(var x in defaults){if(defaults.hasOwnProperty(x))
setDefault(obj,x,defaults[x]);}}
function setDefault(obj,key,value){if(undefined===obj[key])
obj[key]=value;}
function raiseError(msg,error,options){if(options.showErrors)
showCurtain(msg,options.noStyles);else{removeCurtain();console.log(msg);}}
function showCurtain(msg,noStyles){removeCurtain();if(undefined===msg)
msg=AmCharts.__('Loading data...',chart.language);var curtain=document.createElement('div');curtain.setAttribute('id',chart.div.id+'-curtain');curtain.className='amcharts-dataloader-curtain';if(true!==noStyles){curtain.style.position='absolute';curtain.style.top=0;curtain.style.left=0;curtain.style.width=(undefined!==chart.realWidth?chart.realWidth:chart.divRealWidth)+'px';curtain.style.height=(undefined!==chart.realHeight?chart.realHeight:chart.divRealHeight)+'px';curtain.style.textAlign='center';curtain.style.display='table';curtain.style.fontSize='20px';try{curtain.style.background='rgba(255, 255, 255, 0.3)';}catch(e){curtain.style.background='rgb(255, 255, 255)';}
curtain.innerHTML='<div style="display: table-cell; vertical-align: middle;">'+ msg+'</div>';}else{curtain.innerHTML=msg;}
chart.containerDiv.appendChild(curtain);l.curtain=curtain;}
function removeCurtain(){try{if(undefined!==l.curtain)
chart.containerDiv.removeChild(l.curtain);}catch(e){}
l.curtain=undefined;}
function callFunction(func,param1,param2,param3){if('function'===typeof func)
func.call(l,param1,param2,param3);}},['pie','serial','xy','funnel','radar','gauge','gantt','stock','map']);if(undefined===AmCharts.__){AmCharts.__=function(msg,language){if(undefined!==language&&undefined!==AmCharts.translations.dataLoader[language]&&undefined!==AmCharts.translations.dataLoader[language][msg])
return AmCharts.translations.dataLoader[language][msg];else
return msg;};}
AmCharts.loadFile=function(url,options,handler){if(typeof(options)!=='object')
options={};if(options.async===undefined)
options.async=true;var request;if(window.XMLHttpRequest){request=new XMLHttpRequest();}else{request=new ActiveXObject('Microsoft.XMLHTTP');}
try{request.open('GET',options.timestamp?AmCharts.timestampUrl(url):url,options.async);}catch(e){handler.call(this,false);}
if(options.headers!==undefined&&options.headers.length){for(var i=0;i<options.headers.length;i++){var header=options.headers[i];request.setRequestHeader(header.key,header.value);}}
if(options.progress!==undefined&&typeof(options.progress)==='function'){request.onprogress=function(e){var complete=(e.loaded/e.total)*100;options.progress.call(this,complete);}}
request.onreadystatechange=function(){if(4===request.readyState&&404===request.status)
handler.call(this,false);else if(4===request.readyState&&200===request.status)
handler.call(this,request.responseText);};try{request.send();}catch(e){handler.call(this,false);}};AmCharts.parseJSON=function(response){try{if(undefined!==JSON)
return JSON.parse(response);else
return eval(response);}catch(e){return false;}};AmCharts.parseCSV=function(response,options){var data=AmCharts.CSVToArray(response,options.delimiter);var res=[];var cols=[];var col,i;if(options.useColumnNames){cols=data.shift();for(var x=0;x<cols.length;x++){col=cols[x].replace(/^\s+|\s+$/gm,'');if(''===col)
col='col'+ x;cols[x]=col;}
if(0<options.skip)
options.skip--;}
for(i=0;i<options.skip;i++)
data.shift();var row;while((row=options.reverse?data.pop():data.shift())){if(options.skipEmpty&&row.length===1&&row[0]==='')
continue;var dataPoint={};for(i=0;i<row.length;i++){col=undefined===cols[i]?'col'+ i:cols[i];dataPoint[col]=row[i]===""?options.emptyAs:row[i];}
res.push(dataPoint);}
return res;};AmCharts.CSVToArray=function(strData,strDelimiter){strDelimiter=(strDelimiter||',');var objPattern=new RegExp(("(\\"+ strDelimiter+"|\\r?\\n|\\r|^)"+"(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|"+"([^\"\\"+ strDelimiter+"\\r\\n]*))"),"gi");var arrData=[[]];var arrMatches=null;while((arrMatches=objPattern.exec(strData))){var strMatchedDelimiter=arrMatches[1];if(strMatchedDelimiter.length&&(strMatchedDelimiter!==strDelimiter)){arrData.push([]);}
var strMatchedValue;if(arrMatches[2]){strMatchedValue=arrMatches[2].replace(new RegExp("\"\"","g"),"\"");}else{strMatchedValue=arrMatches[3];}
arrData[arrData.length- 1].push(strMatchedValue);}
return(arrData);};AmCharts.timestampUrl=function(url){var p=url.split('?');if(1===p.length)
p[1]=new Date().getTime();else
p[1]+='&'+ new Date().getTime();return p.join('?');};