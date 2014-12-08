(function(e){function t(t,r,i){var s=this;return this.on("click.pjax",t,function(t){var o=e.extend({},m(r,i));if(!o.container)o.container=e(this).attr("data-pjax")||s;n(t,o)})}function n(t,n,r){r=m(n,r);var s=t.currentTarget;if(s.tagName.toUpperCase()!=="A")throw"$.fn.pjax or $.pjax.click requires an anchor element";if(t.which>1||t.metaKey||t.ctrlKey||t.shiftKey||t.altKey)return;if(location.protocol!==s.protocol||location.hostname!==s.hostname)return;if(s.href.indexOf("#")>-1&&v(s)==v(location))return;if(t.isDefaultPrevented())return;var o={url:s.href,container:e(s).attr("data-pjax"),target:s};var u=e.extend({},o,r);var a=e.Event("pjax:click");e(s).trigger(a,[u]);if(!a.isDefaultPrevented()){i(u);t.preventDefault();e(s).trigger("pjax:clicked",[u])}}function r(t,n,r){r=m(n,r);var s=t.currentTarget;if(s.tagName.toUpperCase()!=="FORM")throw"$.pjax.submit requires a form element";var o={type:s.method.toUpperCase(),url:s.action,container:e(s).attr("data-pjax"),target:s};if(o.type!=="GET"&&window.FormData!==undefined){o.data=new FormData(s);o.processData=false;o.contentType=false}else{if(e(s).find(":file").length){return}o.data=e(s).serializeArray()}i(e.extend({},o,r));t.preventDefault()}function i(t){function u(t,r,i){if(!i)i={};i.relatedTarget=n;var o=e.Event(t,i);s.trigger(o,r);return!o.isDefaultPrevented()}t=e.extend(true,{},e.ajaxSettings,i.defaults,t);if(e.isFunction(t.url)){t.url=t.url()}var n=t.target;var r=d(t.url).hash;var s=t.context=g(t.container);if(!t.data)t.data={};if(e.isArray(t.data)){t.data.push({name:"_pjax",value:s.selector})}else{t.data._pjax=s.selector}var a;t.beforeSend=function(e,n){if(n.type!=="GET"){n.timeout=0}e.setRequestHeader("X-PJAX","true");e.setRequestHeader("X-PJAX-Container",s.selector);if(!u("pjax:beforeSend",[e,n]))return false;if(n.timeout>0){a=setTimeout(function(){if(u("pjax:timeout",[e,t]))e.abort("timeout")},n.timeout);n.timeout=0}t.requestUrl=d(n.url).href};t.complete=function(e,n){if(a)clearTimeout(a);u("pjax:complete",[e,n,t]);u("pjax:end",[e,t])};t.error=function(e,n,r){var i=w("",e,t);var s=u("pjax:error",[e,n,r,t]);if(t.type=="GET"&&n!=="abort"&&s){o(i.url)}};t.success=function(n,a,f){var l=i.state;var c=typeof e.pjax.defaults.version==="function"?e.pjax.defaults.version():e.pjax.defaults.version;var p=f.getResponseHeader("X-PJAX-Version");var v=w(n,f,t);if(c&&p&&c!==p){o(v.url);return}if(!v.contents){o(v.url);return}i.state={id:t.id||h(),url:v.url,title:v.title,container:s.selector,fragment:t.fragment,timeout:t.timeout};if(t.push||t.replace){window.history.replaceState(i.state,v.title,v.url)}try{document.activeElement.blur()}catch(m){}if(v.title)document.title=v.title;u("pjax:beforeReplace",[v.contents,t],{state:i.state,previousState:l});s.html(v.contents);var g=s.find("input[autofocus], textarea[autofocus]").last()[0];if(g&&document.activeElement!==g){g.focus()}E(v.scripts);if(typeof t.scrollTo==="number")e(window).scrollTop(t.scrollTo);if(r!==""){var y=d(v.url);y.hash=r;i.state.url=y.href;window.history.replaceState(i.state,v.title,y.href);var b=document.getElementById(y.hash.slice(1));if(b)e(window).scrollTop(e(b).offset().top)}u("pjax:success",[n,a,f,t])};if(!i.state){i.state={id:h(),url:window.location.href,title:document.title,container:s.selector,fragment:t.fragment,timeout:t.timeout};window.history.replaceState(i.state,document.title)}var f=i.xhr;if(f&&f.readyState<4){f.onreadystatechange=e.noop;f.abort()}i.options=t;var f=i.xhr=e.ajax(t);if(f.readyState>0){if(t.push&&!t.replace){N(i.state.id,s.clone().contents());window.history.pushState(null,"",p(t.requestUrl))}u("pjax:start",[f,t]);u("pjax:send",[f,t])}return i.xhr}function s(t,n){var r={url:window.location.href,push:false,replace:true,scrollTo:false};return i(e.extend(r,m(t,n)))}function o(e){window.history.replaceState(null,"",i.state.url);window.location.replace(e)}function l(t){var n=i.state;var r=t.state;if(r&&r.container){if(u&&a==r.url)return;if(i.state&&i.state.id===r.id)return;var s=e(r.container);if(s.length){var f,l=S[r.id];if(i.state){f=i.state.id<r.id?"forward":"back";C(f,i.state.id,s.clone().contents())}var c=e.Event("pjax:popstate",{state:r,direction:f});s.trigger(c);var h={id:r.id,url:r.url,container:s,push:false,fragment:r.fragment,timeout:r.timeout,scrollTo:false};if(l){s.trigger("pjax:start",[null,h]);i.state=r;if(r.title)document.title=r.title;var p=e.Event("pjax:beforeReplace",{state:r,previousState:n});s.trigger(p,[l,h]);s.html(l);s.trigger("pjax:end",[null,h])}else{i(h)}s[0].offsetHeight}else{o(location.href)}}u=false}function c(t){var n=e.isFunction(t.url)?t.url():t.url,r=t.type?t.type.toUpperCase():"GET";var i=e("<form>",{method:r==="GET"?"GET":"POST",action:n,style:"display:none"});if(r!=="GET"&&r!=="POST"){i.append(e("<input>",{type:"hidden",name:"_method",value:r.toLowerCase()}))}var s=t.data;if(typeof s==="string"){e.each(s.split("&"),function(t,n){var r=n.split("=");i.append(e("<input>",{type:"hidden",name:r[0],value:r[1]}))})}else if(typeof s==="object"){for(key in s)i.append(e("<input>",{type:"hidden",name:key,value:s[key]}))}e(document.body).append(i);i.submit()}function h(){return(new Date).getTime()}function p(e){return e.replace(/\?_pjax=[^&]+&?/,"?").replace(/_pjax=[^&]+&?/,"").replace(/[\?&]$/,"")}function d(e){var t=document.createElement("a");t.href=e;return t}function v(e){return e.href.replace(/#.*/,"")}function m(t,n){if(t&&n)n.container=t;else if(e.isPlainObject(t))n=t;else n={container:t};if(n.container)n.container=g(n.container);return n}function g(t){t=e(t);if(!t.length){throw"no pjax container for "+t.selector}else if(t.selector!==""&&t.context===document){return t}else if(t.attr("id")){return e("#"+t.attr("id"))}else{throw"cant get selector for pjax container!"}}function y(e,t){return e.filter(t).add(e.find(t))}function b(t){return e.parseHTML(t,document,true)}function w(t,n,r){var i={},s=/<html/i.test(t);i.url=p(n.getResponseHeader("X-PJAX-URL")||r.requestUrl);if(s){var o=e(b(t.match(/<head[^>]*>([\s\S.]*)<\/head>/i)[0]));var u=e(b(t.match(/<body[^>]*>([\s\S.]*)<\/body>/i)[0]))}else{var o=u=e(b(t))}if(u.length===0)return i;i.title=y(o,"title").last().text();if(r.fragment){if(r.fragment==="body"){var a=u}else{var a=y(u,r.fragment).first()}if(a.length){i.contents=r.fragment==="body"?a:a.contents();if(!i.title)i.title=a.attr("title")||a.data("title")}}else if(!s){i.contents=u}if(i.contents){i.contents=i.contents.not(function(){return e(this).is("title")});i.contents.find("title").remove();i.scripts=y(i.contents,"script[src]").remove();i.contents=i.contents.not(i.scripts)}if(i.title)i.title=e.trim(i.title);return i}function E(t){if(!t)return;var n=e("script[src]");t.each(function(){var t=this.src;var r=n.filter(function(){return this.src===t});if(r.length)return;var i=document.createElement("script");var s=e(this).attr("type");if(s)i.type=s;i.src=e(this).attr("src");document.head.appendChild(i)})}function N(e,t){S[e]=t;T.push(e);k(x,0);k(T,i.defaults.maxCacheLength)}function C(e,t,n){var r,s;S[t]=n;if(e==="forward"){r=T;s=x}else{r=x;s=T}r.push(t);if(t=s.pop())delete S[t];k(r,i.defaults.maxCacheLength)}function k(e,t){while(e.length>t)delete S[e.shift()]}function L(){return e("meta").filter(function(){var t=e(this).attr("http-equiv");return t&&t.toUpperCase()==="X-PJAX-VERSION"}).attr("content")}function A(){e.fn.pjax=t;e.pjax=i;e.pjax.enable=e.noop;e.pjax.disable=O;e.pjax.click=n;e.pjax.submit=r;e.pjax.reload=s;e.pjax.defaults={timeout:650,push:true,replace:false,type:"GET",dataType:"html",scrollTo:0,maxCacheLength:20,version:L};e(window).on("popstate.pjax",l)}function O(){e.fn.pjax=function(){return this};e.pjax=c;e.pjax.enable=A;e.pjax.disable=e.noop;e.pjax.click=e.noop;e.pjax.submit=e.noop;e.pjax.reload=function(){window.location.reload()};e(window).off("popstate.pjax",l)}var u=true;var a=window.location.href;var f=window.history.state;if(f&&f.container){i.state=f}if("state"in window.history){u=false}var S={};var x=[];var T=[];if(e.inArray("state",e.event.props)<0)e.event.props.push("state");e.support.pjax=window.history&&window.history.pushState&&window.history.replaceState&&!navigator.userAgent.match(/((iPod|iPhone|iPad).+\bOS\s+[1-4]\D|WebApps\/.+CFNetwork)/);e.support.pjax?A():O()})(jQuery)