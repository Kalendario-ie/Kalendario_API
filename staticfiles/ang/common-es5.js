!function(){function t(t,n){for(var e=0;e<n.length;e++){var i=n[e];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}function n(t,n){if(!(t instanceof n))throw new TypeError("Cannot call a class as a function")}function e(t,n){var e;if("undefined"==typeof Symbol||null==t[Symbol.iterator]){if(Array.isArray(t)||(e=r(t))||n&&t&&"number"==typeof t.length){e&&(t=e);var i=0,o=function(){};return{s:o,n:function(){return i>=t.length?{done:!0}:{done:!1,value:t[i++]}},e:function(t){throw t},f:o}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var u,s=!0,a=!1;return{s:function(){e=t[Symbol.iterator]()},n:function(){var t=e.next();return s=t.done,t},e:function(t){a=!0,u=t},f:function(){try{s||null==e.return||e.return()}finally{if(a)throw u}}}}function i(t){return function(t){if(Array.isArray(t))return o(t)}(t)||function(t){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(t))return Array.from(t)}(t)||r(t)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function r(t,n){if(t){if("string"==typeof t)return o(t,n);var e=Object.prototype.toString.call(t).slice(8,-1);return"Object"===e&&t.constructor&&(e=t.constructor.name),"Map"===e||"Set"===e?Array.from(t):"Arguments"===e||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e)?o(t,n):void 0}}function o(t,n){(null==n||n>t.length)&&(n=t.length);for(var e=0,i=new Array(n);e<n;e++)i[e]=t[e];return i}(window.webpackJsonp=window.webpackJsonp||[]).push([[1],{EVqC:function(t,n,r){"use strict";r.d(n,"a",(function(){return l}));var o=r("kt0X"),u=r("fXoL"),s=function(){var t={EntitiesOnly:0,Both:1,None:2};return t[t.EntitiesOnly]="EntitiesOnly",t[t.Both]="Both",t[t.None]="None",t}();function a(t){return function(n,e){var r={ids:i(e.ids),entities:Object.assign({},e.entities)},o=t(n,r);return o===s.Both?Object.assign({},e,r):o===s.EntitiesOnly?Object.assign(Object.assign({},e),{entities:r.entities}):e}}function c(t,n){var e=n(t);return Object(u.X)()&&void 0===e&&console.warn("@ngrx/entity: The entity passed to the `selectId` implementation returned undefined.","You should probably provide your own `selectId` implementation.","The entity that was passed:",t,"The `selectId` implementation:",n.toString()),e}function f(t){function n(n,e){var i=c(n,t);return i in e.entities?s.None:(e.ids.push(i),e.entities[i]=n,s.Both)}function i(t,i){var r,o=!1,u=e(t);try{for(u.s();!(r=u.n()).done;){o=n(r.value,i)!==s.None||o}}catch(a){u.e(a)}finally{u.f()}return o?s.Both:s.None}function r(t,n){return n.ids=[],n.entities={},i(t,n),s.Both}function o(t,n){var e=(t instanceof Array?t:n.ids.filter((function(e){return t(n.entities[e])}))).filter((function(t){return t in n.entities})).map((function(t){return delete n.entities[t]})).length>0;return e&&(n.ids=n.ids.filter((function(t){return t in n.entities}))),e?s.Both:s.None}function u(n,e){var i={};return(n=n.filter((function(t){return t.id in e.entities}))).length>0?n.filter((function(n){return function(n,e,i){var r=Object.assign({},i.entities[e.id],e.changes),o=c(r,t),u=o!==e.id;return u&&(n[e.id]=o,delete i.entities[e.id]),i.entities[o]=r,u}(i,n,e)})).length>0?(e.ids=e.ids.map((function(t){return i[t]||t})),s.Both):s.EntitiesOnly:s.None}function f(n,r){var o,a=[],f=[],l=e(n);try{for(l.s();!(o=l.n()).done;){var d=o.value,h=c(d,t);h in r.entities?f.push({id:h,changes:d}):a.push(d)}}catch(y){l.e(y)}finally{l.f()}var p=u(f,r),v=i(a,r);switch(!0){case v===s.None&&p===s.None:return s.None;case v===s.Both||p===s.Both:return s.Both;default:return s.EntitiesOnly}}return{removeAll:function(t){return Object.assign({},t,{ids:[],entities:{}})},addOne:a(n),addMany:a(i),addAll:a(r),setAll:a(r),setOne:a((function(n,e){var i=c(n,t);return i in e.entities?(e.entities[i]=n,s.EntitiesOnly):(e.ids.push(i),e.entities[i]=n,s.Both)})),updateOne:a((function(t,n){return u([t],n)})),updateMany:a(u),upsertOne:a((function(t,n){return f([t],n)})),upsertMany:a(f),removeOne:a((function(t,n){return o([t],n)})),removeMany:a(o),map:a((function(t,n){return u(n.ids.reduce((function(e,i){var r=t(n.entities[i]);return r!==n.entities[i]&&e.push({id:i,changes:r}),e}),[]).filter((function(t){return t.id in n.entities})),n)}))}}function l(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},n=Object.assign({sortComparer:!1,selectId:function(t){return t.id}},t),i=n.selectId,r=n.sortComparer,u={getInitialState:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object.assign({ids:[],entities:{}},t)}},l={getSelectors:function(t){var n=function(t){return t.ids},e=function(t){return t.entities},i=Object(o.q)(n,e,(function(t,n){return t.map((function(t){return n[t]}))})),r=Object(o.q)(n,(function(t){return t.length}));return t?{selectIds:Object(o.q)(t,n),selectEntities:Object(o.q)(t,e),selectAll:Object(o.q)(t,i),selectTotal:Object(o.q)(t,r)}:{selectIds:n,selectEntities:e,selectAll:i,selectTotal:r}}},d=r?function(t,n){var i=f(t);function r(t,n){return o([t],n)}function o(n,e){var i=n.filter((function(n){return!(c(n,t)in e.entities)}));return 0===i.length?s.None:(h(i,e),s.Both)}function u(t,n){return n.entities={},n.ids=[],o(t,n),s.Both}function l(n,e){var i=[],r=n.filter((function(n){return function(n,e,i){if(!(e.id in i.entities))return!1;var r=Object.assign({},i.entities[e.id],e.changes),o=c(r,t);return delete i.entities[e.id],n.push(r),o!==e.id}(i,n,e)})).length>0;if(0===i.length)return s.None;var o=e.ids,u=[];return e.ids=e.ids.filter((function(t,n){return t in e.entities||(u.push(n),!1)})),h(i,e),!r&&u.every((function(t){return e.ids[t]===o[t]}))?s.EntitiesOnly:s.Both}function d(n,i){var r,u=[],a=[],f=e(n);try{for(f.s();!(r=f.n()).done;){var d=r.value,h=c(d,t);h in i.entities?a.push({id:h,changes:d}):u.push(d)}}catch(y){f.e(y)}finally{f.f()}var p=l(a,i),v=o(u,i);switch(!0){case v===s.None&&p===s.None:return s.None;case v===s.Both||p===s.Both:return s.Both;default:return s.EntitiesOnly}}function h(e,i){e.sort(n);for(var r=[],o=0,u=0;o<e.length&&u<i.ids.length;){var s=e[o],a=c(s,t),f=i.ids[u];n(s,i.entities[f])<=0?(r.push(a),o++):(r.push(f),u++)}i.ids=r.concat(o<e.length?e.slice(o).map(t):i.ids.slice(u)),e.forEach((function(n,e){i.entities[t(n)]=n}))}return{removeOne:i.removeOne,removeMany:i.removeMany,removeAll:i.removeAll,addOne:a(r),updateOne:a((function(t,n){return l([t],n)})),upsertOne:a((function(t,n){return d([t],n)})),addAll:a(u),setAll:a(u),setOne:a((function(n,e){var i=c(n,t);return i in e.entities?(e.ids=e.ids.filter((function(t){return t!==i})),h([n],e),s.Both):r(n,e)})),addMany:a(o),updateMany:a(l),upsertMany:a(d),map:a((function(t,n){return l(n.ids.reduce((function(e,i){var r=t(n.entities[i]);return r!==n.entities[i]&&e.push({id:i,changes:r}),e}),[]),n)}))}}(i,r):f(i);return Object.assign(Object.assign(Object.assign({selectId:i,sortComparer:r},u),l),d)}},O51e:function(t,e,i){"use strict";i.d(e,"a",(function(){return u}));var r=i("PCNd"),o=i("fXoL"),u=function(){var t=function t(){n(this,t)};return t.\u0275mod=o.Ob({type:t}),t.\u0275inj=o.Nb({factory:function(n){return new(n||t)},imports:[[r.a]]}),t}()},clZe:function(e,i,r){"use strict";r.d(i,"a",(function(){return u}));var o=r("fXoL"),u=function(){var e=function(){function e(){n(this,e)}var i,r,o;return i=e,(r=[{key:"transform",value:function(t){switch(t){case"A":return"Accepted";case"M":return"Rejected";default:return"Pending"}}}])&&t(i.prototype,r),o&&t(i,o),e}();return e.\u0275fac=function(t){return new(t||e)},e.\u0275pipe=o.Pb({name:"appointmentStatus",type:e,pure:!0}),e}()},r32Y:function(t,e,i){"use strict";i.d(e,"a",(function(){return u}));var r=i("kt0X"),o=i("YZpF"),u=function t(e){n(this,t),this.store=e,this.isMobile$=this.store.pipe(Object(r.t)(o.m)),this.isTablet$=this.store.pipe(Object(r.t)(o.n)),this.user$=this.store.pipe(o.j),this.leftPaneOpen$=this.store.pipe(Object(r.t)(o.k))}}}])}();