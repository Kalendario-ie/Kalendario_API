!function(){function e(e){return function(e){if(Array.isArray(e))return t(e)}(e)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(e)||function(e,n){if(!e)return;if("string"==typeof e)return t(e,n);var a=Object.prototype.toString.call(e).slice(8,-1);"Object"===a&&e.constructor&&(a=e.constructor.name);if("Map"===a||"Set"===a)return Array.from(e);if("Arguments"===a||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(a))return t(e,n)}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function t(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,a=new Array(t);n<t;n++)a[n]=e[n];return a}(window.webpackJsonp=window.webpackJsonp||[]).push([[3],{"6Z0Z":function(t,n,a){"use strict";a.d(n,"a",(function(){return b})),a.d(n,"b",(function(){return l})),a.d(n,"c",(function(){return d})),a.d(n,"d",(function(){return s})),a.d(n,"e",(function(){return O})),a.d(n,"f",(function(){return p})),a.d(n,"g",(function(){return i})),a.d(n,"h",(function(){return h}));var r=a("R0Ic"),c=Object(r.g)([Object(r.e)("{{duration}}ms {{delay}}ms",Object(r.i)([Object(r.n)({visibility:r.a,transform:"scale3d(1, 1, 1)",easing:"ease",offset:0}),Object(r.n)({transform:"scale3d({{scale}}, {{scale}}, {{scale}})",easing:"ease",offset:.5}),Object(r.n)({transform:"scale3d(1, 1, 1)",easing:"ease",offset:1})]))]);function i(t){return Object(r.p)(t&&t.anchor||"pulse",[Object(r.o)("0 ".concat(t&&t.direction||"<=>"," 1"),[].concat(e(t&&"before"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[]),[Object(r.h)([Object(r.q)(c)].concat(e(t&&t.animateChildren&&"together"!==t.animateChildren?[]:[Object(r.j)("@*",Object(r.f)(),{optional:!0})])))],e(t&&"after"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[])),{params:{delay:t&&t.delay||0,duration:t&&t.duration||1e3,scale:t&&t.scale||1.05}})])}var o=Object(r.g)([Object(r.e)("{{duration}}ms {{delay}}ms",Object(r.i)([Object(r.n)({visibility:"visible",opacity:0,easing:"ease",offset:0}),Object(r.n)({opacity:1,easing:"ease",offset:1})]))]);function b(t){return Object(r.p)(t&&t.anchor||"fadeIn",[Object(r.o)("0 => 1",[].concat(e(t&&"before"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[]),[Object(r.h)([Object(r.q)(o)].concat(e(t&&t.animateChildren&&"together"!==t.animateChildren?[]:[Object(r.j)("@*",Object(r.f)(),{optional:!0})])))],e(t&&"after"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[])),{params:{delay:t&&t.delay||0,duration:t&&t.duration||1e3}})])}function s(t){return Object(r.p)(t&&t.anchor||"fadeInOnEnter",[Object(r.o)(":enter",[Object(r.n)({visibility:"hidden"})].concat(e(t&&"before"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[]),[Object(r.h)([Object(r.q)(o)].concat(e(t&&t.animateChildren&&"together"!==t.animateChildren?[]:[Object(r.j)("@*",Object(r.f)(),{optional:!0})])))],e(t&&"after"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[])),{params:{delay:t&&t.delay||0,duration:t&&t.duration||1e3}})])}var j=Object(r.g)([Object(r.e)("{{duration}}ms {{delay}}ms",Object(r.i)([Object(r.n)({visibility:"visible",opacity:0,transform:"translate3d(0, -{{translate}}, 0)",easing:"ease",offset:0}),Object(r.n)({opacity:1,transform:"translate3d(0, 0, 0)",easing:"ease",offset:1})]))]);function l(t){return Object(r.p)(t&&t.anchor||"fadeInDown",[Object(r.o)("0 => 1",[].concat(e(t&&"before"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[]),[Object(r.h)([Object(r.q)(j)].concat(e(t&&t.animateChildren&&"together"!==t.animateChildren?[]:[Object(r.j)("@*",Object(r.f)(),{optional:!0})])))],e(t&&"after"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[])),{params:{delay:t&&t.delay||0,duration:t&&t.duration||1e3,translate:t&&t.translate||"100%"}})])}function d(t){return Object(r.p)(t&&t.anchor||"fadeInDownOnEnter",[Object(r.o)(":enter",[Object(r.n)({visibility:"hidden"})].concat(e(t&&"before"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[]),[Object(r.h)([Object(r.q)(j)].concat(e(t&&t.animateChildren&&"together"!==t.animateChildren?[]:[Object(r.j)("@*",Object(r.f)(),{optional:!0})])))],e(t&&"after"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[])),{params:{delay:t&&t.delay||0,duration:t&&t.duration||1e3,translate:t&&t.translate||"100%"}})])}var f=Object(r.g)([Object(r.e)("{{duration}}ms {{delay}}ms",Object(r.i)([Object(r.n)({opacity:1,easing:"ease",offset:0}),Object(r.n)({opacity:0,easing:"ease",offset:1})]))]);function O(t){return Object(r.p)(t&&t.anchor||"fadeOutOnLeave",[Object(r.o)(":leave",[].concat(e(t&&"before"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[]),[Object(r.h)([Object(r.q)(f)].concat(e(t&&t.animateChildren&&"together"!==t.animateChildren?[]:[Object(r.j)("@*",Object(r.f)(),{optional:!0})])))],e(t&&"after"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[])),{params:{delay:t&&t.delay||0,duration:t&&t.duration||1e3}})])}var u=Object(r.g)([Object(r.e)("{{duration}}ms {{delay}}ms",Object(r.i)([Object(r.n)({visibility:"visible",transform:"perspective(400px) rotate3d(0, 1, 0, {{degrees}}deg)",opacity:0,easing:"ease-in",offset:0}),Object(r.n)({transform:"perspective(400px) rotate3d(0, 1, 0, -20deg)",opacity:.5,easing:"ease-in",offset:.4}),Object(r.n)({transform:"perspective(400px) rotate3d(0, 1, 0, 10deg)",opacity:1,easing:"ease-in",offset:.6}),Object(r.n)({transform:"perspective(400px) rotate3d(0, 1, 0, -5deg)",easing:"ease",offset:.8}),Object(r.n)({transform:"perspective(400px)",easing:"ease",offset:1})]))]);function p(t){return Object(r.p)(t&&t.anchor||"flipInYOnEnter",[Object(r.o)(":enter",[Object(r.n)({visibility:"hidden"})].concat(e(t&&"before"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[]),[Object(r.h)([Object(r.n)({"backface-visibility":"visible"}),Object(r.q)(u)].concat(e(t&&t.animateChildren&&"together"!==t.animateChildren?[]:[Object(r.j)("@*",Object(r.f)(),{optional:!0})])))],e(t&&"after"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[])),{params:{delay:t&&t.delay||0,duration:t&&t.duration||1e3,degrees:t&&t.degrees||90}})])}var m=Object(r.g)([Object(r.e)("{{duration}}ms {{delay}}ms",Object(r.i)([Object(r.n)({transform:"translate3d(0, 0, 0)",easing:"ease",offset:0}),Object(r.n)({transform:"translate3d(-{{translate}}, 0, 0)",visibility:"hidden",easing:"ease",offset:1})]))]);function h(t){return Object(r.p)(t&&t.anchor||"slideOutLeftOnLeave",[Object(r.o)(":leave",[].concat(e(t&&"before"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[]),[Object(r.h)([Object(r.q)(m)].concat(e(t&&t.animateChildren&&"together"!==t.animateChildren?[]:[Object(r.j)("@*",Object(r.f)(),{optional:!0})])))],e(t&&"after"===t.animateChildren?[Object(r.j)("@*",Object(r.f)(),{optional:!0})]:[])),{params:{delay:t&&t.delay||0,duration:t&&t.duration||1e3,translate:t&&t.translate||"100%"}})])}},Ql4B:function(e,t,n){"use strict";n.d(t,"b",(function(){return r})),n.d(t,"a",(function(){return c}));var a=n("R0Ic"),r=Object(a.p)("staggeredFadeIn",[Object(a.o)("0 <=> 1, :enter",[Object(a.j)(":enter",Object(a.n)({opacity:0}),{optional:!0}),Object(a.j)(":enter",Object(a.l)("100ms",[Object(a.e)(".5s ease-in",Object(a.n)({opacity:1}))]),{optional:!0})])]),c=Object(a.p)("expandCollapse",[Object(a.m)("0",Object(a.n)({height:0,overflow:"hidden"})),Object(a.m)("1",Object(a.n)({height:"*",overflow:"auto"})),Object(a.o)("0 => 1",[Object(a.e)("0.3s ease-out")]),Object(a.o)("1 => 0",[Object(a.e)("0.3s ease-in")])])},vqYj:function(e,t,n){"use strict";n.d(t,"a",(function(){return i}));var a=n("fXoL"),r=n("tyNb"),c=n("dV/U"),i=function(){var e=function e(){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e)};return e.\u0275fac=function(t){return new(t||e)},e.\u0275cmp=a.Kb({type:e,selectors:[["shared-company-avatar"]],inputs:{logo:"logo",name:"name",address:"address"},decls:8,vars:7,consts:[[1,"logo-avatar-container"],[1,"company-circle-img-7","c-pointer",3,"src","routerLink"],[1,"logo-avatar-content"],[1,"pb-0","c-pointer",3,"routerLink"],[1,"c-accent"]],template:function(e,t){1&e&&(a.Wb(0,"div",0),a.Rb(1,"img",1),a.Wb(2,"div",2),a.Wb(3,"h1",3),a.Gc(4),a.jc(5,"removeHyphen"),a.Vb(),a.Wb(6,"div",4),a.Gc(7),a.Vb(),a.Vb(),a.Vb()),2&e&&(a.Db(1),a.pc("src",t.logo,a.zc),a.qc("routerLink","/c/",t.name,""),a.Db(2),a.qc("routerLink","/c/",t.name,""),a.Db(1),a.Hc(a.kc(5,5,t.name)),a.Db(3),a.Ic(" ",t.address," "))},directives:[r.c],pipes:[c.a],styles:[".logo-avatar-container[_ngcontent-%COMP%]{display:flex}.logo-avatar-content[_ngcontent-%COMP%]{margin-left:.5rem}"]}),e}()}}])}();