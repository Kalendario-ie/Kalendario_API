!function(){function t(t,n){return function(t){if(Array.isArray(t))return t}(t)||function(t,e){if("undefined"==typeof Symbol||!(Symbol.iterator in Object(t)))return;var n=[],r=!0,i=!1,c=void 0;try{for(var o,a=t[Symbol.iterator]();!(r=(o=a.next()).done)&&(n.push(o.value),!e||n.length!==e);r=!0);}catch(s){i=!0,c=s}finally{try{r||null==a.return||a.return()}finally{if(i)throw c}}return n}(t,n)||e(t,n)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function e(t,e){if(t){if("string"==typeof t)return n(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);return"Object"===r&&t.constructor&&(r=t.constructor.name),"Map"===r||"Set"===r?Array.from(t):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?n(t,e):void 0}}function n(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=t[n];return r}function r(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}function i(t,e,n){return e&&r(t.prototype,e),n&&r(t,n),t}function c(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(window.webpackJsonp=window.webpackJsonp||[]).push([[9],{vfUp:function(n,r,o){"use strict";o.r(r),o.d(r,"CustomersModule",(function(){return st}));var a,s,u=o("ofXK"),l=o("PCNd"),b=o("kt0X"),d=Object(b.n)("[Customers] Initialize Store",Object(b.s)()),f=Object(b.n)("[Customers] Request Entities",Object(b.s)()),h=Object(b.n)("[Customers] Request Entity",Object(b.s)()),m=Object(b.n)("[Customers] Upsert Many",Object(b.s)()),p=Object(b.n)("[Customers] Set All",Object(b.s)()),v=Object(b.n)("[Customers] Add One",Object(b.s)()),y=Object(b.n)("[Customers] Set Error",Object(b.s)()),O=Object(b.n)("[Customers] Set Selected Id",Object(b.s)()),g=o("EVqC"),j=Object(g.a)(),q=Object(b.p)({ids:[],entities:{},selectedRequestId:null,apiError:null},Object(b.r)(p,(function(t,e){var n=e.entities;return j.setAll(n,t)})),Object(b.r)(m,(function(t,e){var n=e.entities;return j.upsertMany(n,t)})),Object(b.r)(v,(function(t,e){var n=e.entity;return j.addOne(n,t)})),Object(b.r)(y,(function(t,e){var n=e.error;return Object.assign(Object.assign({},t),{apiError:n})})),Object(b.r)(O,(function(t,e){var n=e.id;return Object.assign(Object.assign({},t),{selectedRequestId:n})}))),D=Object(b.o)("customers"),w=j.getSelectors(D).selectAll,C=(Object(b.q)(D,(function(t){return t.apiError})),w),S=(Object(b.q)(D,(function(t){return t})),Object(b.q)(D,(function(t){return t.selectedRequestId}))),V=Object(b.q)(C,S,(function(t,e){return t.find((function(t){return t.id===e}))})),k=o("snw9"),E=o("mrSG"),I=o("LRne"),W=o("lJxs"),M=o("5+tZ"),F=o("JIr8"),A=o("fXoL"),$=o("2Sd8"),x=((a=function t(e,n){var r=this;c(this,t),this.actions$=e,this.requestClient=n,this.initializeStore$=this.actions$.pipe(Object(k.e)(d),Object(W.a)((function(t){var e=t.date;return{fromDate:e,toDate:e.clone().endOf("month")}})),Object(M.a)((function(t){var e=t.fromDate,n=t.toDate;return r.requestClient.get({fromDate:e,toDate:n}).pipe(Object(W.a)((function(t){return m({entities:t.results})})),Object(F.a)((function(t){return Object(I.a)(y(t))})))}))),this.requestEntities$=this.actions$.pipe(Object(k.e)(f),Object(W.a)((function(t){var e=t.date;return{fromDate:e,toDate:e.clone().endOf("month")}})),Object(M.a)((function(t){var e=t.fromDate,n=t.toDate;return r.requestClient.get({fromDate:e,toDate:n}).pipe(Object(W.a)((function(t){return p({entities:t.results})})),Object(F.a)((function(t){return Object(I.a)(y(t))})))}))),this.requestEntity$=this.actions$.pipe(Object(k.e)(h),Object(M.a)((function(t){var e=t.id;return r.requestClient.detail(e).pipe(Object(M.a)((function(t){return[v({entity:t}),O({id:e})]})),Object(F.a)((function(t){return Object(I.a)(y(t))})))})))}).\u0275fac=function(t){return new(t||a)(A.ac(k.a),A.ac($.g))},a.\u0275prov=A.Mb({token:a,factory:a.\u0275fac}),Object(E.b)([Object(k.b)()],a.prototype,"initializeStore$",void 0),Object(E.b)([Object(k.b)()],a.prototype,"requestEntities$",void 0),Object(E.b)([Object(k.b)()],a.prototype,"requestEntity$",void 0),a),R=o("LjFu"),L=o("tyNb"),_=o("wd/R"),G=o("iadO"),Y=o("FKr1"),T=o("3lmY"),B=o("6Z0Z"),H=o("Ql4B"),J=o("vqYj"),N=((s=function(){function t(){c(this,t)}return i(t,[{key:"transform",value:function(t){return _.utc(t).format("DD MMMM YYYY")}}]),t}()).\u0275fac=function(t){return new(t||s)},s.\u0275pipe=A.Pb({name:"toMomentDateLong",type:s,pure:!0}),s),P=o("clZe");function Q(t,e){if(1&t&&(A.Wb(0,"div",5),A.Wb(1,"div",6),A.Rb(2,"shared-company-avatar",7),A.Vb(),A.Wb(3,"div",8),A.Gc(4),A.jc(5,"toMomentDateLong"),A.Wb(6,"div",9),A.Gc(7),A.jc(8,"appointmentStatus"),A.Vb(),A.Vb(),A.Vb()),2&t){var n=e.ngIf,r=A.ic(2);A.oc("@fadeIn",r.animationState),A.Db(2),A.oc("address",n.address)("logo",n.avatar)("name",n.name),A.Db(2),A.Ic(" ",A.kc(5,6,r.request.scheduledDate)," "),A.Db(3),A.Ic(" ",A.kc(8,8,r.request.status)," ")}}function U(t,e){if(1&t&&(A.Ub(0),A.Wb(1,"div",15),A.Wb(2,"b"),A.Gc(3),A.Vb(),A.Wb(4,"p",16),A.Gc(5),A.Vb(),A.Vb(),A.Wb(6,"div",17),A.Wb(7,"h6"),A.Gc(8),A.Vb(),A.Vb(),A.Tb()),2&t){var n=e.$implicit;A.Db(3),A.Hc(n.service.name),A.Db(2),A.Jc(" ",n.start.format("DD/MM/YYYY - HH:mm")," (duration: ",n.service.duration,") "),A.Db(3),A.Hc(n.service.price)}}function K(t,e){if(1&t&&(A.Wb(0,"div",10),A.Rb(1,"img",11),A.Wb(2,"div",12),A.Wb(3,"div",13),A.Wb(4,"h4"),A.Gc(5),A.Vb(),A.Vb(),A.Ec(6,U,9,4,"ng-container",14),A.Vb(),A.Vb()),2&t){var n=e.$implicit;A.Db(1),A.pc("src",n.employee.photoUrl,A.zc),A.Db(4),A.Hc(n.employee.name),A.Db(1),A.oc("ngForOf",n.appointments)}}function z(t,e){if(1&t&&(A.Wb(0,"div"),A.Ec(1,Q,9,10,"div",1),A.Wb(2,"p"),A.Gc(3),A.Vb(),A.Wb(4,"h2",2),A.Gc(5,"Summary"),A.Vb(),A.Wb(6,"div"),A.Ec(7,K,7,3,"div",3),A.Vb(),A.Wb(8,"div",4),A.Gc(9),A.jc(10,"currency"),A.Vb(),A.Vb()),2&t){var n=A.ic();A.Db(1),A.oc("ngIf",n.request.owner),A.Db(2),A.Ic(" ",n.request.owner.config.postBookMessage," "),A.Db(1),A.oc("@fadeInDown",n.animationState),A.Db(2),A.oc("@staggeredFadeIn",n.attentionState),A.Db(1),A.oc("ngForOf",n.request.items),A.Db(1),A.oc("@fadeInDown",n.animationState),A.Db(1),A.Ic(" Total: ",A.lc(10,7,n.request.total,"EUR")," ")}}var X,Z=((X=function(){function t(e){c(this,t),this.ref=e,this.animationState=!1,this.attentionState=!1}return i(t,[{key:"animate",value:function(){var t=this;this.attentionState=!this.attentionState,this.animationState=!0,setTimeout((function(){t.animationState=!1,t.ref.detectChanges()}),800)}},{key:"request",set:function(t){this.animate(),this._request=t},get:function(){return this._request}}]),t}()).\u0275fac=function(t){return new(t||X)(A.Qb(A.h))},X.\u0275cmp=A.Kb({type:X,selectors:[["customers-request-card"]],inputs:{request:"request"},decls:1,vars:1,consts:[[4,"ngIf"],["class","row mb-4",4,"ngIf"],[1,"c-primary","mb-4"],["class","d-flex mb-4",4,"ngFor","ngForOf"],[1,"c-primary","text-right","h4"],[1,"row","mb-4"],[1,"col-8"],[3,"address","logo","name"],[1,"col-4","h4","text-right","font-weight-bold"],[1,"c-primary"],[1,"d-flex","mb-4"],[1,"company-circle-img-7",3,"src"],[1,"row","w-100","ml-2"],[1,"col-12"],[4,"ngFor","ngForOf"],[1,"col-9"],[1,"text-small"],[1,"col-3","text-right","c-primary"]],template:function(t,e){1&t&&A.Ec(0,z,11,10,"div",0),2&t&&A.oc("ngIf",e.request)},directives:[u.l,u.k,J.a],pipes:[u.d,N,P.a],styles:[""],data:{animation:[Object(B.a)(),Object(B.b)(),H.b]}}),X);function tt(t,e){if(1&t){var n=A.Xb();A.Wb(0,"div"),A.Wb(1,"div",6),A.ec("click",(function(){A.yc(n);var t=e.$implicit;return A.ic().select.emit(t.id)})),A.Rb(2,"div",7),A.Wb(3,"b"),A.Gc(4),A.Vb(),A.Vb(),A.Vb()}if(2&t){var r=e.$implicit,i=e.index,c=A.ic();A.Db(2),A.Dc("background-color",c.getColor(i)),A.Db(2),A.Jc(" ",r.owner.name," - ",r.owner.address," ")}}var et,nt,rt,it,ct=((et=function(){function n(t){c(this,n),this.adapter=t,this.monthSelected=new A.o,this.select=new A.o,this.currentMonth=null,this._date=_.utc()}return i(n,[{key:"ngAfterViewInit",value:function(){this.currentMonth=this.calendar.monthView._monthLabel}},{key:"ngAfterViewChecked",value:function(){this.loadEvents(),this.paintCalendar()}},{key:"loadEvents",value:function(){if(this.calendar&&this.calendar.monthView&&this.currentMonth!==this.calendar.monthView._monthLabel){this.currentMonth=this.calendar.monthView._monthLabel;var t=this.adapter.getMonthNames("short").map((function(t){return t.toLowerCase()})).indexOf(this.currentMonth.toLowerCase()),e=+this.calendarHeader.periodButtonText.substring(this.currentMonth.length+1),n=this.adapter.createDate(e,t,1);this.monthSelected.emit(n)}}},{key:"paintCalendar",value:function(){var n,r=document.getElementsByClassName("special-date"),i=function(t,n){var r;if("undefined"==typeof Symbol||null==t[Symbol.iterator]){if(Array.isArray(t)||(r=e(t))||n&&t&&"number"==typeof t.length){r&&(t=r);var i=0,c=function(){};return{s:c,n:function(){return i>=t.length?{done:!0}:{done:!1,value:t[i++]}},e:function(t){throw t},f:c}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,s=!1;return{s:function(){r=t[Symbol.iterator]()},n:function(){var t=r.next();return a=t.done,t},e:function(t){s=!0,o=t},f:function(){try{a||null==r.return||r.return()}finally{if(s)throw o}}}}(Array.from(r).entries());try{for(i.s();!(n=i.n()).done;){var c=t(n.value,2),o=c[0],a=c[1];if(1===a.children.length){var s=document.createElement("div");s.classList.add("under-bar"),s.style.backgroundColor=this.getColor(o),a.appendChild(s)}}}catch(u){i.e(u)}finally{i.f()}}},{key:"dateClass",value:function(){var t=this;return function(e){return t.requests.map((function(t){return t.scheduledDate})).some((function(t){return t===e.toISOString().substring(0,10)}))?"special-date":""}}},{key:"getColor",value:function(t){var e=["#0DB4B9","#F2A1A1","#E76D89","#E1621A","#E9422C","#FF0E48","#15D0C5","#FF4EED","#2C57F0","#9A2CF0","#0DB952"];return e[t%e.length]}},{key:"requests",set:function(t){this._requests=t,this.calendar&&this.calendar.updateTodaysDate()},get:function(){return this._requests}},{key:"date",get:function(){return this._date},set:function(t){this._date=t;var e=this.requests.find((function(e){return e.scheduledDate===t.toISOString().substring(0,10)}));e&&this.select.emit(e.id)}}]),n}()).\u0275fac=function(t){return new(t||et)(A.Qb(Y.c))},et.\u0275cmp=A.Kb({type:et,selectors:[["customers-requests"]],viewQuery:function(t,e){var n;1&t&&(A.Lc(G.a,!0),A.Lc(G.b,!0)),2&t&&(A.uc(n=A.fc())&&(e.calendar=n.first),A.uc(n=A.fc())&&(e.calendarHeader=n.first))},inputs:{requests:"requests",selected:"selected"},outputs:{monthSelected:"monthSelected",select:"select"},decls:9,vars:4,consts:[[1,"row"],[1,"col-md-4","col-sm-12","mb-2"],[3,"dateClass","selected","selectedChange"],[4,"ngFor","ngForOf"],[1,"col-md-8","col-sm-12"],[3,"request"],[1,"d-flex","mb-2",3,"click"],[1,"calendar-bar"]],template:function(t,e){1&t&&(A.Wb(0,"div",0),A.Wb(1,"div",1),A.Wb(2,"app-kalendario-card"),A.Wb(3,"mat-calendar",2),A.ec("selectedChange",(function(t){return e.date=t})),A.Rb(4,"mat-calendar-header"),A.Vb(),A.Ec(5,tt,5,4,"div",3),A.Vb(),A.Vb(),A.Wb(6,"div",4),A.Wb(7,"app-kalendario-card"),A.Rb(8,"customers-request-card",5),A.Vb(),A.Vb(),A.Vb()),2&t&&(A.Db(3),A.oc("dateClass",e.dateClass())("selected",e.date),A.Db(2),A.oc("ngForOf",e.requests),A.Db(3),A.oc("request",e.selected))},directives:[T.a,G.a,G.b,u.k,Z],styles:[".container[_ngcontent-%COMP%]{display:flex;flex-direction:column;position:absolute;top:64px;bottom:0;left:0;right:0}.calendar-bar[_ngcontent-%COMP%]{border-radius:10px;width:4px;margin-right:.5rem}"]}),et),ot=[{path:"requests",component:(nt=function(){function t(e,n){c(this,t),this.store=e,this.route=n}return i(t,[{key:"ngOnInit",value:function(){console.log("ngOnInit"),this.store.dispatch(d({date:_.utc().startOf("month")})),this.requests$=this.store.pipe(Object(b.t)(C)),this.selected$=this.store.pipe(Object(b.t)(V));var t=+this.route.snapshot.queryParamMap.get("id");t&&this.store.dispatch(h({id:t}))}},{key:"requestRequests",value:function(t){console.log("requestRequests"),this.store.dispatch(f({date:t}))}},{key:"selectRequest",value:function(t){this.store.dispatch(O({id:t}))}}]),t}(),nt.\u0275fac=function(t){return new(t||nt)(A.Qb(b.h),A.Qb(L.a))},nt.\u0275cmp=A.Kb({type:nt,selectors:[["app-requests-page"]],decls:4,vars:6,consts:[[1,"container","mt-4","mb-4"],[3,"requests","selected","monthSelected","select"]],template:function(t,e){1&t&&(A.Wb(0,"div",0),A.Wb(1,"customers-requests",1),A.ec("monthSelected",(function(t){return e.requestRequests(t)}))("select",(function(t){return e.selectRequest(t)})),A.jc(2,"async"),A.jc(3,"async"),A.Vb(),A.Vb()),2&t&&(A.Db(1),A.oc("requests",A.kc(2,2,e.requests$))("selected",A.kc(3,4,e.selected$)))},directives:[ct],pipes:[u.b],styles:[""],changeDetection:0}),nt),canActivate:[R.a]}],at=((it=function t(){c(this,t)}).\u0275mod=A.Ob({type:it}),it.\u0275inj=A.Nb({factory:function(t){return new(t||it)},imports:[[L.f.forChild(ot)],L.f]}),it),st=((rt=function t(){c(this,t)}).\u0275mod=A.Ob({type:rt}),rt.\u0275inj=A.Nb({factory:function(t){return new(t||rt)},imports:[[u.c,l.a,at,b.j.forFeature("customers",q),k.c.forFeature([x])]]}),rt)}}])}();