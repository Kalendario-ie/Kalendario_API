(window.webpackJsonp=window.webpackJsonp||[]).push([[8],{EVqC:function(t,e,n){"use strict";n.d(e,"a",(function(){return u}));var s=n("kt0X"),i=n("fXoL");const r=function(){var t={EntitiesOnly:0,Both:1,None:2};return t[t.EntitiesOnly]="EntitiesOnly",t[t.Both]="Both",t[t.None]="None",t}();function c(t){return function(e,n){const s={ids:[...n.ids],entities:Object.assign({},n.entities)},i=t(e,s);return i===r.Both?Object.assign({},n,s):i===r.EntitiesOnly?Object.assign(Object.assign({},n),{entities:s.entities}):n}}function o(t,e){const n=e(t);return Object(i.X)()&&void 0===n&&console.warn("@ngrx/entity: The entity passed to the `selectId` implementation returned undefined.","You should probably provide your own `selectId` implementation.","The entity that was passed:",t,"The `selectId` implementation:",e.toString()),n}function a(t){function e(e,n){const s=o(e,t);return s in n.entities?r.None:(n.ids.push(s),n.entities[s]=e,r.Both)}function n(t,n){let s=!1;for(const i of t)s=e(i,n)!==r.None||s;return s?r.Both:r.None}function s(t,e){return e.ids=[],e.entities={},n(t,e),r.Both}function i(t,e){const n=(t instanceof Array?t:e.ids.filter(n=>t(e.entities[n]))).filter(t=>t in e.entities).map(t=>delete e.entities[t]).length>0;return n&&(e.ids=e.ids.filter(t=>t in e.entities)),n?r.Both:r.None}function a(e,n){const s={};return(e=e.filter(t=>t.id in n.entities)).length>0?e.filter(e=>function(e,n,s){const i=Object.assign({},s.entities[n.id],n.changes),r=o(i,t),c=r!==n.id;return c&&(e[n.id]=r,delete s.entities[n.id]),s.entities[r]=i,c}(s,e,n)).length>0?(n.ids=n.ids.map(t=>s[t]||t),r.Both):r.EntitiesOnly:r.None}function u(e,s){const i=[],c=[];for(const n of e){const e=o(n,t);e in s.entities?c.push({id:e,changes:n}):i.push(n)}const u=a(c,s),d=n(i,s);switch(!0){case d===r.None&&u===r.None:return r.None;case d===r.Both||u===r.Both:return r.Both;default:return r.EntitiesOnly}}return{removeAll:function(t){return Object.assign({},t,{ids:[],entities:{}})},addOne:c(e),addMany:c(n),addAll:c(s),setAll:c(s),setOne:c((function(e,n){const s=o(e,t);return s in n.entities?(n.entities[s]=e,r.EntitiesOnly):(n.ids.push(s),n.entities[s]=e,r.Both)})),updateOne:c((function(t,e){return a([t],e)})),updateMany:c(a),upsertOne:c((function(t,e){return u([t],e)})),upsertMany:c(u),removeOne:c((function(t,e){return i([t],e)})),removeMany:c(i),map:c((function(t,e){return a(e.ids.reduce((n,s)=>{const i=t(e.entities[s]);return i!==e.entities[s]&&n.push({id:s,changes:i}),n},[]).filter(({id:t})=>t in e.entities),e)}))}}function u(t={}){const{selectId:e,sortComparer:n}=Object.assign({sortComparer:!1,selectId:t=>t.id},t),i={getInitialState:function(t={}){return Object.assign({ids:[],entities:{}},t)}},u={getSelectors:function(t){const e=t=>t.ids,n=t=>t.entities,i=Object(s.q)(e,n,(t,e)=>t.map(t=>e[t])),r=Object(s.q)(e,t=>t.length);return t?{selectIds:Object(s.q)(t,e),selectEntities:Object(s.q)(t,n),selectAll:Object(s.q)(t,i),selectTotal:Object(s.q)(t,r)}:{selectIds:e,selectEntities:n,selectAll:i,selectTotal:r}}},d=n?function(t,e){const{removeOne:n,removeMany:s,removeAll:i}=a(t);function u(t,e){return d([t],e)}function d(e,n){const s=e.filter(e=>!(o(e,t)in n.entities));return 0===s.length?r.None:(f(s,n),r.Both)}function l(t,e){return e.entities={},e.ids=[],d(t,e),r.Both}function b(e,n){const s=[],i=e.filter(e=>function(e,n,s){if(!(n.id in s.entities))return!1;const i=Object.assign({},s.entities[n.id],n.changes),r=o(i,t);return delete s.entities[n.id],e.push(i),r!==n.id}(s,e,n)).length>0;if(0===s.length)return r.None;{const t=n.ids,e=[];return n.ids=n.ids.filter((t,s)=>t in n.entities||(e.push(s),!1)),f(s,n),!i&&e.every(e=>n.ids[e]===t[e])?r.EntitiesOnly:r.Both}}function h(e,n){const s=[],i=[];for(const r of e){const e=o(r,t);e in n.entities?i.push({id:e,changes:r}):s.push(r)}const c=b(i,n),a=d(s,n);switch(!0){case a===r.None&&c===r.None:return r.None;case a===r.Both||c===r.Both:return r.Both;default:return r.EntitiesOnly}}function f(n,s){n.sort(e);const i=[];let r=0,c=0;for(;r<n.length&&c<s.ids.length;){const a=n[r],u=o(a,t),d=s.ids[c];e(a,s.entities[d])<=0?(i.push(u),r++):(i.push(d),c++)}s.ids=i.concat(r<n.length?n.slice(r).map(t):s.ids.slice(c)),n.forEach((e,n)=>{s.entities[t(e)]=e})}return{removeOne:n,removeMany:s,removeAll:i,addOne:c(u),updateOne:c((function(t,e){return b([t],e)})),upsertOne:c((function(t,e){return h([t],e)})),addAll:c(l),setAll:c(l),setOne:c((function(e,n){const s=o(e,t);return s in n.entities?(n.ids=n.ids.filter(t=>t!==s),f([e],n),r.Both):u(e,n)})),addMany:c(d),updateMany:c(b),upsertMany:c(h),map:c((function(t,e){return b(e.ids.reduce((n,s)=>{const i=t(e.entities[s]);return i!==e.entities[s]&&n.push({id:s,changes:i}),n},[]),e)}))}}(e,n):a(e);return Object.assign(Object.assign(Object.assign({selectId:e,sortComparer:n},i),u),d)}},vfUp:function(t,e,n){"use strict";n.r(e),n.d(e,"CustomersModule",(function(){return U}));var s=n("ofXK"),i=n("PCNd"),r=n("kt0X");const c=Object(r.n)("[Customers] Initialize Store",Object(r.s)()),o=Object(r.n)("[Customers] Request Entities",Object(r.s)()),a=Object(r.n)("[Customers] Request Entity",Object(r.s)()),u=Object(r.n)("[Customers] Upsert Many",Object(r.s)()),d=Object(r.n)("[Customers] Set All",Object(r.s)()),l=Object(r.n)("[Customers] Add One",Object(r.s)()),b=Object(r.n)("[Customers] Set Error",Object(r.s)()),h=Object(r.n)("[Customers] Set Selected Id",Object(r.s)());var f=n("EVqC");const m=Object(f.a)(),p=Object(r.p)({ids:[],entities:{},selectedRequestId:null,apiError:null},Object(r.r)(d,(t,{entities:e})=>m.setAll(e,t)),Object(r.r)(u,(t,{entities:e})=>m.upsertMany(e,t)),Object(r.r)(l,(t,{entity:e})=>m.addOne(e,t)),Object(r.r)(b,(t,{error:e})=>Object.assign(Object.assign({},t),{apiError:e})),Object(r.r)(h,(t,{id:e})=>Object.assign(Object.assign({},t),{selectedRequestId:e}))),O=Object(r.o)("customers"),{selectAll:g}=m.getSelectors(O),j=(Object(r.q)(O,t=>t.apiError),g),y=(Object(r.q)(O,t=>t),Object(r.q)(O,t=>t.selectedRequestId)),q=Object(r.q)(j,y,(t,e)=>t.find(t=>t.id===e));var v=n("snw9"),D=n("mrSG"),C=n("LRne"),w=n("lJxs"),E=n("5+tZ"),V=n("JIr8"),S=n("fXoL"),M=n("2Sd8");let I=(()=>{class t{constructor(t,e){this.actions$=t,this.requestClient=e,this.initializeStore$=this.actions$.pipe(Object(v.e)(c),Object(w.a)(({date:t})=>({fromDate:t,toDate:t.clone().endOf("month")})),Object(E.a)(({fromDate:t,toDate:e})=>this.requestClient.get({fromDate:t,toDate:e}).pipe(Object(w.a)(t=>u({entities:t.results})),Object(V.a)(t=>Object(C.a)(b({error:t})))))),this.requestEntities$=this.actions$.pipe(Object(v.e)(o),Object(w.a)(({date:t})=>({fromDate:t,toDate:t.clone().endOf("month")})),Object(E.a)(({fromDate:t,toDate:e})=>this.requestClient.get({fromDate:t,toDate:e}).pipe(Object(w.a)(t=>d({entities:t.results})),Object(V.a)(t=>Object(C.a)(b({error:t})))))),this.requestEntity$=this.actions$.pipe(Object(v.e)(a),Object(E.a)(({id:t})=>this.requestClient.detail(t).pipe(Object(E.a)(e=>[l({entity:e}),h({id:t})]),Object(V.a)(t=>Object(C.a)(b({error:t}))))))}}return t.\u0275fac=function(e){return new(e||t)(S.ac(v.a),S.ac(M.g))},t.\u0275prov=S.Mb({token:t,factory:t.\u0275fac}),Object(D.b)([Object(v.b)()],t.prototype,"initializeStore$",void 0),Object(D.b)([Object(v.b)()],t.prototype,"requestEntities$",void 0),Object(D.b)([Object(v.b)()],t.prototype,"requestEntity$",void 0),t})();var W=n("PC/O"),B=n("tyNb"),A=n("wd/R"),N=n("iadO"),F=n("FKr1"),k=n("3lmY"),$=n("6Z0Z"),x=n("Ql4B"),R=n("vqYj");let _=(()=>{class t{transform(t,...e){return A.utc(t).format("DD MMMM YYYY")}}return t.\u0275fac=function(e){return new(e||t)},t.\u0275pipe=S.Pb({name:"toMomentDateLong",type:t,pure:!0}),t})();var G=n("clZe");function L(t,e){if(1&t&&(S.Wb(0,"div",5),S.Wb(1,"div",6),S.Rb(2,"shared-company-avatar",7),S.Vb(),S.Wb(3,"div",8),S.Gc(4),S.jc(5,"toMomentDateLong"),S.Wb(6,"div",9),S.Gc(7),S.jc(8,"appointmentStatus"),S.Vb(),S.Vb(),S.Vb()),2&t){const t=e.ngIf,n=S.ic(2);S.oc("@fadeIn",n.animationState),S.Db(2),S.oc("address",t.address)("logo",t.avatar)("name",t.name),S.Db(2),S.Ic(" ",S.kc(5,6,n.request.scheduledDate)," "),S.Db(3),S.Ic(" ",S.kc(8,8,n.request.status)," ")}}function Y(t,e){if(1&t&&(S.Ub(0),S.Wb(1,"div",15),S.Wb(2,"b"),S.Gc(3),S.Vb(),S.Wb(4,"p",16),S.Gc(5),S.Vb(),S.Vb(),S.Wb(6,"div",17),S.Wb(7,"h6"),S.Gc(8),S.Vb(),S.Vb(),S.Tb()),2&t){const t=e.$implicit;S.Db(3),S.Hc(t.service.name),S.Db(2),S.Jc(" ",t.start.format("DD/MM/YYYY - HH:mm")," (duration: ",t.service.duration,") "),S.Db(3),S.Hc(t.service.price)}}function T(t,e){if(1&t&&(S.Wb(0,"div",10),S.Rb(1,"img",11),S.Wb(2,"div",12),S.Wb(3,"div",13),S.Wb(4,"h4"),S.Gc(5),S.Vb(),S.Vb(),S.Ec(6,Y,9,4,"ng-container",14),S.Vb(),S.Vb()),2&t){const t=e.$implicit;S.Db(1),S.pc("src",t.employee.photoUrl,S.zc),S.Db(4),S.Hc(t.employee.name),S.Db(1),S.oc("ngForOf",t.appointments)}}function H(t,e){if(1&t&&(S.Wb(0,"div"),S.Ec(1,L,9,10,"div",1),S.Wb(2,"p"),S.Gc(3),S.Vb(),S.Wb(4,"h2",2),S.Gc(5,"Summary"),S.Vb(),S.Wb(6,"div"),S.Ec(7,T,7,3,"div",3),S.Vb(),S.Wb(8,"div",4),S.Gc(9),S.jc(10,"currency"),S.Vb(),S.Vb()),2&t){const t=S.ic();S.Db(1),S.oc("ngIf",t.request.owner),S.Db(2),S.Ic(" ",t.request.owner.config.postBookMessage," "),S.Db(1),S.oc("@fadeInDown",t.animationState),S.Db(2),S.oc("@staggeredFadeIn",t.attentionState),S.Db(1),S.oc("ngForOf",t.request.items),S.Db(1),S.oc("@fadeInDown",t.animationState),S.Db(1),S.Ic(" Total: ",S.lc(10,7,t.request.total,"EUR")," ")}}let X=(()=>{class t{constructor(t){this.ref=t,this.animationState=!1,this.attentionState=!1}set request(t){this.animate(),this._request=t}get request(){return this._request}animate(){this.attentionState=!this.attentionState,this.animationState=!0,setTimeout(()=>{this.animationState=!1,this.ref.detectChanges()},800)}}return t.\u0275fac=function(e){return new(e||t)(S.Qb(S.h))},t.\u0275cmp=S.Kb({type:t,selectors:[["customers-request-card"]],inputs:{request:"request"},decls:1,vars:1,consts:[[4,"ngIf"],["class","row mb-4",4,"ngIf"],[1,"c-primary","mb-4"],["class","d-flex mb-4",4,"ngFor","ngForOf"],[1,"c-primary","text-right","h4"],[1,"row","mb-4"],[1,"col-8"],[3,"address","logo","name"],[1,"col-4","h4","text-right","font-weight-bold"],[1,"c-primary"],[1,"d-flex","mb-4"],[1,"company-circle-img-7",3,"src"],[1,"row","w-100","ml-2"],[1,"col-12"],[4,"ngFor","ngForOf"],[1,"col-9"],[1,"text-small"],[1,"col-3","text-right","c-primary"]],template:function(t,e){1&t&&S.Ec(0,H,11,10,"div",0),2&t&&S.oc("ngIf",e.request)},directives:[s.l,s.k,R.a],pipes:[s.d,_,G.a],styles:[""],data:{animation:[Object($.b)(),Object($.c)(),x.c]}}),t})();function J(t,e){if(1&t){const t=S.Xb();S.Wb(0,"div"),S.Wb(1,"div",6),S.ec("click",(function(){S.yc(t);const n=e.$implicit;return S.ic().select.emit(n.id)})),S.Rb(2,"div",7),S.Wb(3,"b"),S.Gc(4),S.Vb(),S.Vb(),S.Vb()}if(2&t){const t=e.$implicit,n=e.index,s=S.ic();S.Db(2),S.Dc("background-color",s.getColor(n)),S.Db(2),S.Jc(" ",t.owner.name," - ",t.owner.address," ")}}let P=(()=>{class t{constructor(t){this.adapter=t,this.monthSelected=new S.o,this.select=new S.o,this.currentMonth=null,this._date=A.utc()}set requests(t){this._requests=t,this.calendar&&this.calendar.updateTodaysDate()}get requests(){return this._requests}get date(){return this._date}set date(t){this._date=t;const e=this.requests.find(e=>e.scheduledDate===t.toISOString().substring(0,10));e&&this.select.emit(e.id)}ngAfterViewInit(){this.currentMonth=this.calendar.monthView._monthLabel}ngAfterViewChecked(){this.loadEvents(),this.paintCalendar()}loadEvents(){if(this.calendar&&this.calendar.monthView&&this.currentMonth!==this.calendar.monthView._monthLabel){this.currentMonth=this.calendar.monthView._monthLabel;const t=this.adapter.getMonthNames("short").map(t=>t.toLowerCase()).indexOf(this.currentMonth.toLowerCase()),e=+this.calendarHeader.periodButtonText.substring(this.currentMonth.length+1),n=this.adapter.createDate(e,t,1);this.monthSelected.emit(n)}}paintCalendar(){const t=document.getElementsByClassName("special-date"),e=Array.from(t);for(const[n,s]of e.entries())if(1===s.children.length){const t=document.createElement("div");t.classList.add("under-bar"),t.style.backgroundColor=this.getColor(n),s.appendChild(t)}}dateClass(){return t=>this.requests.map(t=>t.scheduledDate).some(e=>e===t.toISOString().substring(0,10))?"special-date":""}getColor(t){const e=["#0DB4B9","#F2A1A1","#E76D89","#E1621A","#E9422C","#FF0E48","#15D0C5","#FF4EED","#2C57F0","#9A2CF0","#0DB952"];return e[t%e.length]}}return t.\u0275fac=function(e){return new(e||t)(S.Qb(F.c))},t.\u0275cmp=S.Kb({type:t,selectors:[["customers-requests"]],viewQuery:function(t,e){var n;1&t&&(S.Mc(N.a,!0),S.Mc(N.b,!0)),2&t&&(S.uc(n=S.fc())&&(e.calendar=n.first),S.uc(n=S.fc())&&(e.calendarHeader=n.first))},inputs:{requests:"requests",selected:"selected"},outputs:{monthSelected:"monthSelected",select:"select"},decls:9,vars:4,consts:[[1,"row"],[1,"col-md-4","col-sm-12","mb-2"],[3,"dateClass","selected","selectedChange"],[4,"ngFor","ngForOf"],[1,"col-md-8","col-sm-12"],[3,"request"],[1,"d-flex","mb-2",3,"click"],[1,"calendar-bar"]],template:function(t,e){1&t&&(S.Wb(0,"div",0),S.Wb(1,"div",1),S.Wb(2,"app-kalendario-card"),S.Wb(3,"mat-calendar",2),S.ec("selectedChange",(function(t){return e.date=t})),S.Rb(4,"mat-calendar-header"),S.Vb(),S.Ec(5,J,5,4,"div",3),S.Vb(),S.Vb(),S.Wb(6,"div",4),S.Wb(7,"app-kalendario-card"),S.Rb(8,"customers-request-card",5),S.Vb(),S.Vb(),S.Vb()),2&t&&(S.Db(3),S.oc("dateClass",e.dateClass())("selected",e.date),S.Db(2),S.oc("ngForOf",e.requests),S.Db(3),S.oc("request",e.selected))},directives:[k.a,N.a,N.b,s.k,X],styles:[".container[_ngcontent-%COMP%]{display:flex;flex-direction:column;position:absolute;top:64px;bottom:0;left:0;right:0}.calendar-bar[_ngcontent-%COMP%]{border-radius:10px;width:4px;margin-right:.5rem}"]}),t})();const Q=[{path:"requests",component:(()=>{class t{constructor(t,e){this.store=t,this.route=e}ngOnInit(){this.store.dispatch(c({date:A.utc().startOf("month")})),this.requests$=this.store.pipe(Object(r.t)(j)),this.selected$=this.store.pipe(Object(r.t)(q));const t=+this.route.snapshot.queryParamMap.get("id");t&&this.store.dispatch(a({id:t}))}requestRequests(t){this.store.dispatch(o({date:t}))}selectRequest(t){this.store.dispatch(h({id:t}))}}return t.\u0275fac=function(e){return new(e||t)(S.Qb(r.h),S.Qb(B.a))},t.\u0275cmp=S.Kb({type:t,selectors:[["app-requests-page"]],decls:4,vars:6,consts:[[1,"container","mt-4","mb-4"],[3,"requests","selected","monthSelected","select"]],template:function(t,e){1&t&&(S.Wb(0,"div",0),S.Wb(1,"customers-requests",1),S.ec("monthSelected",(function(t){return e.requestRequests(t)}))("select",(function(t){return e.selectRequest(t)})),S.jc(2,"async"),S.jc(3,"async"),S.Vb(),S.Vb()),2&t&&(S.Db(1),S.oc("requests",S.kc(2,2,e.requests$))("selected",S.kc(3,4,e.selected$)))},directives:[P],pipes:[s.b],styles:[""],changeDetection:0}),t})(),canActivate:[W.a]}];let K=(()=>{class t{}return t.\u0275mod=S.Ob({type:t}),t.\u0275inj=S.Nb({factory:function(e){return new(e||t)},imports:[[B.f.forChild(Q)],B.f]}),t})(),U=(()=>{class t{}return t.\u0275mod=S.Ob({type:t}),t.\u0275inj=S.Nb({factory:function(e){return new(e||t)},imports:[[s.c,i.a,K,r.j.forFeature("customers",p),v.c.forFeature([I])]]}),t})()}}]);