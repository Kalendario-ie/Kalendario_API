(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{PgJR:function(t,e,n){"use strict";n.r(e),n.d(e,"EmployeeModule",(function(){return Y}));var i=n("PCNd"),c=n("tyNb"),o=n("fXoL");let r=(()=>{class t{constructor(){}ngOnInit(){}}return t.\u0275fac=function(e){return new(e||t)},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-home"]],decls:2,vars:0,template:function(t,e){1&t&&(o.Wb(0,"p"),o.Gc(1,"home works!"),o.Vb())},styles:[""]}),t})();var s=n("wd/R"),a=n("eJuo"),p=n("eIep"),d=n("lJxs"),u=n("vyqY"),m=n("YZpF"),l=n("kt0X"),b=n("ofXK"),h=n("Qu3c");function f(t,e){if(1&t){const t=o.Xb();o.Wb(0,"p"),o.Wb(1,"i",11),o.ec("click",(function(){return o.yc(t),o.ic().edit()})),o.Vb(),o.Vb()}}let D=(()=>{class t{constructor(t){this.store=t}customerDetails(){return this.appointment.customer.email+"\n"+this.appointment.customer.phone}edit(){this.store.dispatch(u.b.openFormDialog({id:this.appointment.id}))}}return t.\u0275fac=function(e){return new(e||t)(o.Qb(l.h))},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-schedule-appointment"]],inputs:{appointment:"appointment",showEdit:"showEdit"},decls:17,vars:7,consts:[[1,"schedule-appointment-container"],[1,"row"],[1,"col-2","text-center","m-auto","c-medium-gray"],[4,"ngIf"],[1,"col-6","m-auto"],[1,"m-auto"],[1,"col-4","c-medium-gray"],[1,"fa","fa-clock","c-primary","mr-2"],[1,"c-primary",3,"matTooltip","matTooltipClass"],[1,"fa","fa-address-card","mr-2"],[1,"col-12"],[1,"fa","fa-pen","c-primary","c-pointer",3,"click"]],template:function(t,e){1&t&&(o.Wb(0,"div",0),o.Wb(1,"div",1),o.Wb(2,"div",2),o.Gc(3),o.Ec(4,f,2,0,"p",3),o.Vb(),o.Wb(5,"div",4),o.Wb(6,"p",5),o.Gc(7),o.Vb(),o.Vb(),o.Wb(8,"div",6),o.Wb(9,"p"),o.Rb(10,"i",7),o.Gc(11),o.Vb(),o.Wb(12,"p",8),o.Rb(13,"i",9),o.Gc(14),o.Vb(),o.Vb(),o.Wb(15,"div",10),o.Rb(16,"hr"),o.Vb(),o.Vb(),o.Vb()),2&t&&(o.Db(3),o.Ic(" ",e.appointment.start.format("HH:mm")," "),o.Db(1),o.oc("ngIf",e.showEdit),o.Db(3),o.Ic(" ",e.appointment.service.name," "),o.Db(4),o.Ic(" ",e.appointment.service.duration," "),o.Db(1),o.oc("matTooltip",e.customerDetails())("matTooltipClass","tooltip-ws"),o.Db(2),o.Ic("",e.appointment.customer.name," "))},directives:[b.m,h.a],styles:[".schedule-appointment-container[_ngcontent-%COMP%]{font-weight:600;margin:0 15px}p[_ngcontent-%COMP%]{margin:0}"]}),t})();function y(t,e){if(1&t){const t=o.Xb();o.Wb(0,"div",16),o.Wb(1,"p"),o.Gc(2),o.Vb(),o.Wb(3,"div",17),o.ec("click",(function(){o.yc(t);const n=e.$implicit;return o.ic().emitDate(n)})),o.Wb(4,"div",18),o.Gc(5),o.Vb(),o.Vb(),o.Vb()}if(2&t){const t=e.$implicit,n=o.ic();o.Db(2),o.Hc(t.format("ddd").toUpperCase()),o.Db(1),o.Hb("bg-primary",n.isCurrent(t)),o.Db(2),o.Ic(" ",t.format("DD")," ")}}function v(t,e){if(1&t){const t=o.Xb();o.Wb(0,"button",19),o.ec("click",(function(){o.yc(t);const e=o.ic();return e.add.emit(e.currentDate)})),o.Gc(1," New appointment "),o.Vb()}}function g(t,e){if(1&t&&o.Rb(0,"employee-schedule-appointment",20),2&t){const t=e.$implicit,n=o.ic();o.oc("appointment",t)("showEdit",n.permissions.change)}}let V=(()=>{class t{constructor(){this.updateCurrent=new o.o,this.add=new o.o}dates(){const t=[];let e=s.utc(this.startDate.toISOString());for(;e.isBefore(this.endDate)||e.isSame(this.endDate);)t.push(s.utc(e.toISOString())),e=e.clone().add(1,"day");return t}isCurrent(t){return this.currentDate.format("DDMMYYYY")===t.format("DDMMYYYY")}emitDate(t){this.updateCurrent.emit(t)}nextDay(){this.emitDate(this.currentDate.clone().add(1,"day"))}previousDay(){this.emitDate(this.currentDate.clone().subtract(1,"day"))}}return t.\u0275fac=function(e){return new(e||t)},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-schedule"]],inputs:{currentDate:"currentDate",startDate:"startDate",endDate:"endDate",appointments:"appointments",permissions:"permissions",employee:"employee"},outputs:{updateCurrent:"updateCurrent",add:"add"},decls:26,vars:6,consts:[[1,"schedule-container"],[1,"row"],[1,"col-12","h4","text-center"],[1,"col-12"],[1,"d-flex","c-primary","h3","text-center","mr-4","ml-4"],[1,"fa","fa-chevron-left","c-pointer",3,"click"],[1,"w-100"],[1,"fa","fa-chevron-right","c-pointer",3,"click"],[1,"d-flex","h4","text-center"],["class","date-box",4,"ngFor","ngForOf"],[1,"col-2"],[1,"col-8","h5","text-center"],[1,"col-12","text-center"],["class","btn btn-primary",3,"click",4,"ngIf"],[1,"pretty-scroll"],[3,"appointment","showEdit",4,"ngFor","ngForOf"],[1,"date-box"],[1,"day-round","c-pointer",3,"click"],[1,"inner"],[1,"btn","btn-primary",3,"click"],[3,"appointment","showEdit"]],template:function(t,e){1&t&&(o.Wb(0,"div",0),o.Wb(1,"div",1),o.Wb(2,"div",2),o.Gc(3),o.Vb(),o.Wb(4,"div",3),o.Wb(5,"div",4),o.Wb(6,"i",5),o.ec("click",(function(){return e.previousDay()})),o.Vb(),o.Wb(7,"span",6),o.Gc(8),o.Vb(),o.Wb(9,"i",7),o.ec("click",(function(){return e.nextDay()})),o.Vb(),o.Vb(),o.Vb(),o.Wb(10,"div",3),o.Wb(11,"div",8),o.Ec(12,y,6,4,"div",9),o.Vb(),o.Vb(),o.Wb(13,"div",3),o.Rb(14,"hr"),o.Vb(),o.Rb(15,"div",10),o.Wb(16,"div",11),o.Gc(17),o.Vb(),o.Rb(18,"div",10),o.Wb(19,"div",12),o.Rb(20,"hr"),o.Ec(21,v,2,0,"button",13),o.Rb(22,"hr"),o.Vb(),o.Wb(23,"div",3),o.Wb(24,"div",14),o.Ec(25,g,1,2,"employee-schedule-appointment",15),o.Vb(),o.Vb(),o.Vb(),o.Vb()),2&t&&(o.Db(3),o.Ic(" ",e.employee.name," "),o.Db(5),o.Hc(e.currentDate.format("MMMM YYYY")),o.Db(4),o.oc("ngForOf",e.dates()),o.Db(5),o.Ic(" ",e.currentDate.format("dddd, DD MMMM YYYY")," "),o.Db(4),o.oc("ngIf",e.permissions.add),o.Db(4),o.oc("ngForOf",e.appointments))},directives:[b.l,b.m,D],styles:[".schedule-container[_ngcontent-%COMP%]{max-width:650px}.date-box[_ngcontent-%COMP%]{flex:1}.pretty-scroll[_ngcontent-%COMP%]{overflow-y:scroll;max-height:30rem}.day-round[_ngcontent-%COMP%]{position:relative;margin:auto;width:4rem;height:4rem;border-radius:2rem}.inner[_ngcontent-%COMP%]{margin:0;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)}"]}),t})();function W(t,e){if(1&t){const t=o.Xb();o.Wb(0,"div",1),o.Wb(1,"employee-schedule",2),o.ec("updateCurrent",(function(e){return o.yc(t),o.ic().updateCurrent(e)}))("add",(function(n){o.yc(t);const i=e.ngIf;return o.ic().openCreateDialog(n,i)})),o.jc(2,"async"),o.jc(3,"async"),o.jc(4,"async"),o.Vb(),o.Vb()}if(2&t){const t=e.ngIf,n=o.ic();o.Db(1),o.oc("currentDate",o.kc(2,6,n.currentDate$))("appointments",o.kc(3,8,n.appointments$))("permissions",o.kc(4,10,n.permissions$))("employee",t)("startDate",n.startDate)("endDate",n.endDate)}}let w=(()=>{class t{constructor(t){this.store=t}ngOnInit(){this.initialize(),this.employee$=this.store.select(m.r),this.appointments$=this.employee$.pipe(Object(p.a)(t=>this.store.select(u.d.selectCurrentDateEmployeeAppointments,{employeeId:t.id}))),this.permissions$=this.store.select(m.q,{model:a.a.modelType}),this.currentDate$=this.store.select(u.d.selectCurrentDate).pipe(Object(d.a)(t=>s.utc(t)))}initialize(){this.updateCurrent(s().utc().startOf("day")),this.startDate=s().utc().startOf("day").subtract(3,"day"),this.endDate=s().utc().startOf("day").add(3,"day"),this.loadAppointments()}updateCurrent(t){this.store.dispatch(u.b.setCurrentDate({date:t})),t.isAfter(this.endDate)&&(this.startDate=t,this.endDate=s.utc(t.toISOString()).add(6,"day")),t.isBefore(this.startDate)&&(this.startDate=s.utc(t.toISOString()).subtract(6,"day"),this.endDate=t),this.loadAppointments()}loadAppointments(){this.store.dispatch(u.b.requestEntities({params:{fromDate:this.startDate,toDate:this.endDate}}))}openCreateDialog(t,e){this.store.dispatch(u.b.openCreateAppointmentDialog({date:t,employee:e}))}}return t.\u0275fac=function(e){return new(e||t)(o.Qb(l.h))},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-schedule-page"]],decls:2,vars:3,consts:[["class","container mt-4",4,"ngIf"],[1,"container","mt-4"],[3,"currentDate","appointments","permissions","employee","startDate","endDate","updateCurrent","add"]],template:function(t,e){1&t&&(o.Ec(0,W,5,12,"div",0),o.jc(1,"async")),2&t&&o.oc("ngIf",o.kc(1,1,e.employee$))},directives:[b.m,V],pipes:[b.b],styles:[""],changeDetection:0}),t})(),C=(()=>{class t{constructor(t){this.store=t}canActivate(t,e){return this.store.pipe(m.j,Object(d.a)(t=>!!t.employee))}}return t.\u0275fac=function(e){return new(e||t)(o.ac(l.h))},t.\u0275prov=o.Mb({token:t,factory:t.\u0275fac,providedIn:"root"}),t})();const O=[{path:"home",icon:"home",component:r,canActivate:[C]},{path:"schedule",icon:"book",component:w,canActivate:[C]},{path:"",icon:"",component:w,canActivate:[C]}];var I=n("7Qvi");const k=[{path:"",icon:"",component:(()=>{class t{constructor(){this.routes=O}}return t.\u0275fac=function(e){return new(e||t)},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-dashboard"]],decls:2,vars:1,consts:[[3,"routes"]],template:function(t,e){1&t&&(o.Wb(0,"shared-dashboard-container-shell",0),o.Rb(1,"router-outlet"),o.Vb()),2&t&&o.oc("routes",e.routes)},directives:[I.a,c.g],styles:[""]}),t})(),children:O}];let M=(()=>{class t{}return t.\u0275mod=o.Ob({type:t}),t.\u0275inj=o.Nb({factory:function(e){return new(e||t)},imports:[[c.f.forChild(k)],c.f]}),t})();var x=n("QiP+");let Y=(()=>{class t{}return t.\u0275mod=o.Ob({type:t}),t.\u0275inj=o.Nb({factory:function(e){return new(e||t)},imports:[[i.a,M,x.a]]}),t})()}}]);