(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{PgJR:function(t,e,n){"use strict";n.r(e),n.d(e,"EmployeeModule",(function(){return A}));var c=n("PCNd"),i=n("tyNb"),o=n("fXoL");let r=(()=>{class t{constructor(){}ngOnInit(){}}return t.\u0275fac=function(e){return new(e||t)},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-home"]],decls:2,vars:0,template:function(t,e){1&t&&(o.Wb(0,"p"),o.Gc(1,"home works!"),o.Vb())},styles:[""]}),t})();var a=n("wd/R"),s=n("eJuo"),p=n("eIep"),d=n("lJxs"),l=n("vyqY"),u=n("YZpF"),m=n("kt0X"),b=n("ofXK"),h=n("Nls1"),f=n("3Pt+"),D=n("iadO"),y=n("Qu3c");function v(t,e){if(1&t){const t=o.Xb();o.Wb(0,"p"),o.Wb(1,"i",11),o.ec("click",(function(){return o.yc(t),o.ic().edit()})),o.Vb(),o.Vb()}}let g=(()=>{class t{constructor(t){this.store=t}customerDetails(){return this.appointment.customer.email+"\n"+this.appointment.customer.phone}edit(){this.store.dispatch(l.b.openAppointmentEventDialog({id:this.appointment.id,employeeMode:!0}))}}return t.\u0275fac=function(e){return new(e||t)(o.Qb(m.h))},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-schedule-appointment"]],inputs:{appointment:"appointment",showEdit:"showEdit"},decls:17,vars:7,consts:[[1,"schedule-appointment-container"],[1,"row"],[1,"col-2","text-center","m-auto","c-medium-gray"],[4,"ngIf"],[1,"col-6","m-auto"],[1,"m-auto"],[1,"col-4","c-medium-gray"],[1,"fa","fa-clock","c-primary","mr-2"],[1,"c-primary",3,"matTooltip","matTooltipClass"],[1,"fa","fa-address-card","mr-2"],[1,"col-12"],[1,"fa","fa-pen","c-primary","c-pointer",3,"click"]],template:function(t,e){1&t&&(o.Wb(0,"div",0),o.Wb(1,"div",1),o.Wb(2,"div",2),o.Gc(3),o.Ec(4,v,2,0,"p",3),o.Vb(),o.Wb(5,"div",4),o.Wb(6,"p",5),o.Gc(7),o.Vb(),o.Vb(),o.Wb(8,"div",6),o.Wb(9,"p"),o.Rb(10,"i",7),o.Gc(11),o.Vb(),o.Wb(12,"p",8),o.Rb(13,"i",9),o.Gc(14),o.Vb(),o.Vb(),o.Wb(15,"div",10),o.Rb(16,"hr"),o.Vb(),o.Vb(),o.Vb()),2&t&&(o.Db(3),o.Ic(" ",e.appointment.start.format("HH:mm")," "),o.Db(1),o.oc("ngIf",e.showEdit),o.Db(3),o.Ic(" ",e.appointment.service.name," "),o.Db(4),o.Ic(" ",e.appointment.service.duration," "),o.Db(1),o.oc("matTooltip",e.customerDetails())("matTooltipClass","tooltip-ws"),o.Db(2),o.Ic("",e.appointment.customer.name," "))},directives:[b.l,y.a],styles:[".schedule-appointment-container[_ngcontent-%COMP%]{font-weight:600;margin:0 15px}p[_ngcontent-%COMP%]{margin:0}"]}),t})();function V(t,e){if(1&t){const t=o.Xb();o.Wb(0,"div",19),o.Wb(1,"p"),o.Gc(2),o.Vb(),o.Wb(3,"div",20),o.ec("click",(function(){o.yc(t);const n=e.$implicit;return o.ic().emitDate(n)})),o.Wb(4,"div",21),o.Gc(5),o.Vb(),o.Vb(),o.Vb()}if(2&t){const t=e.$implicit,n=o.ic();o.Db(2),o.Hc(t.format("ddd").toUpperCase()),o.Db(1),o.Hb("bg-primary",n.isCurrent(t)),o.Db(2),o.Ic(" ",t.format("DD")," ")}}function W(t,e){if(1&t){const t=o.Xb();o.Ub(0),o.Wb(1,"button",22),o.ec("click",(function(){o.yc(t);const e=o.ic();return e.add.emit(e.currentDate)})),o.Gc(2," New appointment "),o.Vb(),o.Rb(3,"hr"),o.Tb()}}function w(t,e){if(1&t&&o.Rb(0,"employee-schedule-appointment",23),2&t){const t=e.$implicit,n=o.ic();o.oc("appointment",t)("showEdit",n.permissions.change)}}let C=(()=>{class t{constructor(){this.updateCurrent=new o.o,this.add=new o.o}dates(){const t=[];let e=a.utc(this.startDate.toISOString());for(;e.isBefore(this.endDate)||e.isSame(this.endDate);)t.push(a.utc(e.toISOString())),e=e.clone().add(1,"day");return t}isCurrent(t){return this.currentDate.format("DDMMYYYY")===t.format("DDMMYYYY")}emitDate(t){this.updateCurrent.emit(t)}nextDay(){this.emitDate(this.currentDate.clone().add(1,"day"))}previousDay(){this.emitDate(this.currentDate.clone().subtract(1,"day"))}availability(){const t=Object(h.c)(this.employee.scheduleModel,this.currentDate);return t.frames.length>0?t.frames.map(t=>t.name).reduce((t,e)=>t+" | "+e):"No Availability"}}return t.\u0275fac=function(e){return new(e||t)},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-schedule"]],inputs:{currentDate:"currentDate",startDate:"startDate",endDate:"endDate",appointments:"appointments",permissions:"permissions",employee:"employee"},outputs:{updateCurrent:"updateCurrent",add:"add"},decls:29,vars:9,consts:[[1,"schedule-container"],[1,"row"],[1,"col-12","h4","text-center"],[1,"col-12"],[1,"d-flex","c-primary","h3","text-center","mr-4","ml-4"],[1,"fa","fa-chevron-left","c-pointer",3,"click"],[1,"w-100"],[1,"fa","fa-chevron-right","c-pointer",3,"click"],[1,"d-flex","h4","text-center"],["class","date-box",4,"ngFor","ngForOf"],[1,"col-12","h5","text-center"],[1,"c-pointer",3,"click"],[1,"fa","fa-calendar","mr-2"],[1,"visually-hidden"],[3,"ngModel","matDatepicker","ngModelChange","click"],["dp",""],[4,"ngIf"],[1,"pretty-scroll"],[3,"appointment","showEdit",4,"ngFor","ngForOf"],[1,"date-box"],[1,"day-round","c-pointer",3,"click"],[1,"inner"],[1,"btn","btn-primary",3,"click"],[3,"appointment","showEdit"]],template:function(t,e){if(1&t){const t=o.Xb();o.Wb(0,"div",0),o.Wb(1,"div",1),o.Wb(2,"div",2),o.Gc(3),o.Vb(),o.Wb(4,"div",3),o.Wb(5,"div",4),o.Wb(6,"i",5),o.ec("click",(function(){return e.previousDay()})),o.Vb(),o.Wb(7,"span",6),o.Gc(8),o.Vb(),o.Wb(9,"i",7),o.ec("click",(function(){return e.nextDay()})),o.Vb(),o.Vb(),o.Vb(),o.Wb(10,"div",3),o.Wb(11,"div",8),o.Ec(12,V,6,4,"div",9),o.Vb(),o.Rb(13,"hr"),o.Vb(),o.Wb(14,"div",10),o.Wb(15,"div",11),o.ec("click",(function(){return o.yc(t),o.vc(21).open()})),o.Rb(16,"i",12),o.Gc(17),o.Vb(),o.Wb(18,"div",13),o.Wb(19,"input",14),o.ec("ngModelChange",(function(t){return e.emitDate(t)}))("click",(function(){return o.yc(t),o.vc(21).open()})),o.Vb(),o.Vb(),o.Rb(20,"mat-datepicker",null,15),o.Rb(22,"hr"),o.Gc(23),o.Rb(24,"hr"),o.Ec(25,W,4,0,"ng-container",16),o.Vb(),o.Wb(26,"div",3),o.Wb(27,"div",17),o.Ec(28,w,1,2,"employee-schedule-appointment",18),o.Vb(),o.Vb(),o.Vb(),o.Vb()}if(2&t){const t=o.vc(21);o.Db(3),o.Ic(" ",e.employee.name," "),o.Db(5),o.Hc(e.currentDate.format("MMMM YYYY")),o.Db(4),o.oc("ngForOf",e.dates()),o.Db(5),o.Ic(" ",e.currentDate.format("dddd, DD MMMM YYYY")," "),o.Db(2),o.oc("ngModel",e.currentDate)("matDatepicker",t),o.Db(4),o.Ic(" ",e.availability()," "),o.Db(2),o.oc("ngIf",e.permissions.add),o.Db(3),o.oc("ngForOf",e.appointments)}},directives:[b.k,f.c,D.d,f.n,f.q,D.c,b.l,g],styles:[".schedule-container[_ngcontent-%COMP%]{max-width:650px}.date-box[_ngcontent-%COMP%]{flex:1}.pretty-scroll[_ngcontent-%COMP%]{overflow-y:scroll;max-height:30rem}.day-round[_ngcontent-%COMP%]{position:relative;margin:auto;width:4rem;height:4rem;border-radius:2rem}.inner[_ngcontent-%COMP%]{margin:0;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)}"]}),t})();function k(t,e){if(1&t){const t=o.Xb();o.Wb(0,"div",1),o.Wb(1,"employee-schedule",2),o.ec("updateCurrent",(function(e){return o.yc(t),o.ic().updateCurrent(e)}))("add",(function(n){o.yc(t);const c=e.ngIf;return o.ic().openCreateDialog(n,c)})),o.jc(2,"async"),o.jc(3,"async"),o.jc(4,"async"),o.Vb(),o.Vb()}if(2&t){const t=e.ngIf,n=o.ic();o.Db(1),o.oc("currentDate",o.kc(2,6,n.currentDate$))("appointments",o.kc(3,8,n.appointments$))("permissions",o.kc(4,10,n.permissions$))("employee",t)("startDate",n.startDate)("endDate",n.endDate)}}let M=(()=>{class t{constructor(t){this.store=t}ngOnInit(){this.initialize(),this.employee$=this.store.select(u.t),this.appointments$=this.employee$.pipe(Object(p.a)(t=>this.store.select(l.d.selectCurrentDateEmployeeAppointments,{employeeId:t.id}))),this.permissions$=this.store.select(u.r,{model:s.a.modelType}),this.currentDate$=this.store.select(l.d.selectCurrentDate).pipe(Object(d.a)(t=>a.utc(t)))}initialize(){this.updateCurrent(a().utc().startOf("day")),this.startDate=a().utc().startOf("day").subtract(3,"day"),this.endDate=a().utc().startOf("day").add(3,"day"),this.loadAppointments()}updateCurrent(t){this.store.dispatch(l.b.setCurrentDate({date:t})),t.isAfter(this.endDate)&&(this.startDate=t,this.endDate=a.utc(t.toISOString()).add(6,"day")),t.isBefore(this.startDate)&&(this.startDate=a.utc(t.toISOString()).subtract(6,"day"),this.endDate=t),this.loadAppointments()}loadAppointments(){this.store.dispatch(l.b.requestEntities({params:{fromDate:this.startDate,toDate:this.endDate}}))}openCreateDialog(t,e){this.store.dispatch(l.b.openCreateAppointmentDialog({date:t,employee:e,employeeMode:!0}))}}return t.\u0275fac=function(e){return new(e||t)(o.Qb(m.h))},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-schedule-page"]],decls:2,vars:3,consts:[["class","container mt-4",4,"ngIf"],[1,"container","mt-4"],[3,"currentDate","appointments","permissions","employee","startDate","endDate","updateCurrent","add"]],template:function(t,e){1&t&&(o.Ec(0,k,5,12,"div",0),o.jc(1,"async")),2&t&&o.oc("ngIf",o.kc(1,1,e.employee$))},directives:[b.l,C],pipes:[b.b],styles:[""],changeDetection:0}),t})(),O=(()=>{class t{constructor(t){this.store=t}canActivate(t,e){return this.store.pipe(u.k,Object(d.a)(t=>!!t.employee))}}return t.\u0275fac=function(e){return new(e||t)(o.ac(m.h))},t.\u0275prov=o.Mb({token:t,factory:t.\u0275fac,providedIn:"root"}),t})();const I=[{path:"home",icon:"home",component:r,canActivate:[O]},{path:"schedule",icon:"book",component:M,canActivate:[O]},{path:"",icon:"",component:M,canActivate:[O]}];var x=n("7Qvi");const Y=[{path:"",icon:"",component:(()=>{class t{constructor(){this.routes=I}}return t.\u0275fac=function(e){return new(e||t)},t.\u0275cmp=o.Kb({type:t,selectors:[["employee-dashboard"]],decls:2,vars:1,consts:[[3,"routes"]],template:function(t,e){1&t&&(o.Wb(0,"shared-dashboard-container-shell",0),o.Rb(1,"router-outlet"),o.Vb()),2&t&&o.oc("routes",e.routes)},directives:[x.a,i.g],styles:[""]}),t})(),children:I}];let E=(()=>{class t{}return t.\u0275mod=o.Ob({type:t}),t.\u0275inj=o.Nb({factory:function(e){return new(e||t)},imports:[[i.f.forChild(Y)],i.f]}),t})();var R=n("QiP+");let A=(()=>{class t{}return t.\u0275mod=o.Ob({type:t}),t.\u0275inj=o.Nb({factory:function(e){return new(e||t)},imports:[[c.a,E,R.a]]}),t})()}}]);