import{a as A}from"./chunk-FNLJE7QV.js";import{Aa as P,Ea as R,Fa as j,G as l,H as d,J as B,N as x,P as D,b as u,d as h,f as I,h as b,j as v,n as S,na as E,pa as M,q as c,qa as w,r as f,ra as T,t as p,u as y,v as g,w as a,wa as k,x as s,xa as F,y as C}from"./chunk-XX3QOINY.js";import"./chunk-FVSUARKE.js";import"./chunk-NA2OGXLT.js";import"./chunk-GHOA5HSF.js";import"./chunk-SZCERZCG.js";import"./chunk-G3CV3VGG.js";import"./chunk-GFTFUPMB.js";import"./chunk-C4ZWKFGK.js";import"./chunk-F6OOB4LP.js";import"./chunk-4U6PRYVA.js";import"./chunk-6O5TN2LV.js";import"./chunk-JWIEPCRG.js";import"./chunk-QPVVTFFW.js";import"./chunk-J6ICYO4L.js";import"./chunk-LF5XB4YN.js";import{e as r}from"./chunk-PG5KTQWO.js";var N={revision:"Raspberry Pi revision",model:"Raspberry Pi model",pcb_revision:"Printed Circuit Board (PCB) revision",released:"Release date",soc:"System On a Chip (SoC)",manufacturer:"Manufacturer",memory:"Memory (SDRAM)",storage:"Storage type",usb:"Number of USB ports",usb3:"Number of USB3 ports",ethernet:"Number of ethernet ports",eth_speed:"Ethernet speed",wifi:"Wifi available",bluetooth:"Bluetooth available",csi:"Number of Camera Serial Interfaces (CSI)",dsi:"Number of Display Serial Interfaces (DSI)"};var _="/v1/info",$=(()=>{let e=class e extends A{getInfo(){return this.getAppConfig().pipe(I(o=>{let t=new URL(`${o.api.host}${_}`);return this.httpClient.get(t.toString()).pipe(h(n=>(this.showToast("There was an error retrieving the board info!","danger"),u(()=>n))))}))}};r(e,"\u0275fac",(()=>{let o;return function(n){return(o||(o=S(e)))(n||e)}})()),r(e,"\u0275prov",b({token:e,factory:e.\u0275fac,providedIn:"root"}));let i=e;return i})();var O=(i,e)=>e.key;function V(i,e){if(i&1&&(a(0,"ion-item")(1,"ion-label"),l(2),s(),a(3,"ion-label",3),l(4),s()()),i&2){let m=e.$implicit;c(2),d(m.key),c(2),d(m.value)}}var X=(()=>{let e=class e{constructor(o,t){r(this,"infoService");r(this,"cdr");r(this,"fields",[]);this.infoService=o,this.cdr=t}ionViewDidEnter(){this.loadInfo()}loadInfo(){this.infoService.getInfo().subscribe(o=>{let t=[];for(let[n,L]of Object.entries(o))t.push({key:N[n],value:L});this.fields=t,this.cdr.detectChanges()})}};r(e,"\u0275fac",function(t){return new(t||e)(f($),f(x))}),r(e,"\u0275cmp",v({type:e,selectors:[["app-board-info-list"]],standalone:!0,features:[B],decls:10,vars:2,consts:[[3,"translucent"],["slot","start"],[3,"fullscreen"],[1,"ion-text-right"]],template:function(t,n){t&1&&(a(0,"ion-header",0)(1,"ion-toolbar")(2,"ion-buttons",1),C(3,"ion-menu-button"),s(),a(4,"ion-title"),l(5,"Board Info"),s()()(),a(6,"ion-content",2)(7,"ion-list"),y(8,V,5,2,"ion-item",null,O),s()()),t&2&&(p("translucent",!0),c(6),p("fullscreen",!0),c(2),g(n.fields))},dependencies:[D,w,j,E,P,R,M,F,T,k],changeDetection:0}));let i=e;return i})();export{X as BoardInfoPage};