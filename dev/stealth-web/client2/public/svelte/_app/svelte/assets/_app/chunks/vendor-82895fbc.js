function t(){}function e(t,e){for(const n in e)t[n]=e[n];return t}function n(t){return t()}function s(){return Object.create(null)}function r(t){t.forEach(n)}function o(t){return"function"==typeof t}function i(t,e){return t!=t?e==e:t!==e||t&&"object"==typeof t||"function"==typeof t}function c(t,e,n,s){if(t){const r=l(t,e,n,s);return t[0](r)}}function l(t,n,s,r){return t[1]&&r?e(s.ctx.slice(),t[1](r(n))):s.ctx}function u(t,e,n,s,r,o,i){const c=function(t,e,n,s){if(t[2]&&s){const r=t[2](s(n));if(void 0===e.dirty)return r;if("object"==typeof r){const t=[],n=Math.max(e.dirty.length,r.length);for(let s=0;s<n;s+=1)t[s]=e.dirty[s]|r[s];return t}return e.dirty|r}return e.dirty}(e,s,r,o);if(c){const r=l(e,n,s,i);t.p(r,c)}}function a(t){return null==t?"":t}function f(e){return e&&o(e.destroy)?e.destroy:t}function d(t,e){t.appendChild(e)}function h(t,e,n){t.insertBefore(e,n||null)}function p(t){t.parentNode.removeChild(t)}function m(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}function g(t){return document.createElement(t)}function $(t){return document.createElementNS("http://www.w3.org/2000/svg",t)}function b(t){return document.createTextNode(t)}function v(){return b(" ")}function y(){return b("")}function w(t,e,n){null==n?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}function x(t){return Array.from(t.childNodes)}function k(t,e,n,s){for(let r=0;r<t.length;r+=1){const s=t[r];if(s.nodeName===e){let e=0;const o=[];for(;e<s.attributes.length;){const t=s.attributes[e++];n[t.name]||o.push(t.name)}for(let t=0;t<o.length;t++)s.removeAttribute(o[t]);return t.splice(r,1)[0]}}return s?$(e):g(e)}function _(t,e){for(let n=0;n<t.length;n+=1){const s=t[n];if(3===s.nodeType)return s.data=""+e,t.splice(n,1)[0]}return b(e)}function E(t){return _(t," ")}function z(t,e){e=""+e,t.wholeText!==e&&(t.data=e)}function j(t,e,n,s){t.style.setProperty(e,n,s?"important":"")}let O;function I(t){O=t}function M(){if(!O)throw new Error("Function called outside component initialization");return O}function C(t){M().$$.on_mount.push(t)}function q(t){M().$$.after_update.push(t)}function A(t,e){M().$$.context.set(t,e)}const N=[],R=[],S=[],T=[],L=Promise.resolve();let P=!1;function G(){P||(P=!0,L.then(F))}function U(t){S.push(t)}let B=!1;const D=new Set;function F(){if(!B){B=!0;do{for(let t=0;t<N.length;t+=1){const e=N[t];I(e),H(e.$$)}for(I(null),N.length=0;R.length;)R.pop()();for(let t=0;t<S.length;t+=1){const e=S[t];D.has(e)||(D.add(e),e())}S.length=0}while(N.length);for(;T.length;)T.pop()();P=!1,B=!1,D.clear()}}function H(t){if(null!==t.fragment){t.update(),r(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(U)}}const J=new Set;let K;function V(){K={r:0,c:[],p:K}}function Q(){K.r||r(K.c),K=K.p}function W(t,e){t&&t.i&&(J.delete(t),t.i(e))}function X(t,e,n,s){if(t&&t.o){if(J.has(t))return;J.add(t),K.c.push((()=>{J.delete(t),s&&(n&&t.d(1),s())})),t.o(e)}}function Y(t,e){const n=e.token={};function s(t,s,r,o){if(e.token!==n)return;e.resolved=o;let i=e.ctx;void 0!==r&&(i=i.slice(),i[r]=o);const c=t&&(e.current=t)(i);let l=!1;e.block&&(e.blocks?e.blocks.forEach(((t,n)=>{n!==s&&t&&(V(),X(t,1,1,(()=>{e.blocks[n]===t&&(e.blocks[n]=null)})),Q())})):e.block.d(1),c.c(),W(c,1),c.m(e.mount(),e.anchor),l=!0),e.block=c,e.blocks&&(e.blocks[s]=c),l&&F()}if((r=t)&&"object"==typeof r&&"function"==typeof r.then){const n=M();if(t.then((t=>{I(n),s(e.then,1,e.value,t),I(null)}),(t=>{if(I(n),s(e.catch,2,e.error,t),I(null),!e.hasCatch)throw t})),e.current!==e.pending)return s(e.pending,0),!0}else{if(e.current!==e.then)return s(e.then,1,e.value,t),!0;e.resolved=t}var r}function Z(t,e,n){const s=e.slice(),{resolved:r}=t;t.current===t.then&&(s[t.value]=r),t.current===t.catch&&(s[t.error]=r),t.block.p(s,n)}function tt(t,e){const n={},s={},r={$$scope:1};let o=t.length;for(;o--;){const i=t[o],c=e[o];if(c){for(const t in i)t in c||(s[t]=1);for(const t in c)r[t]||(n[t]=c[t],r[t]=1);t[o]=c}else for(const t in i)r[t]=1}for(const i in s)i in n||(n[i]=void 0);return n}function et(t){return"object"==typeof t&&null!==t?t:{}}function nt(t){t&&t.c()}function st(t,e){t&&t.l(e)}function rt(t,e,s,i){const{fragment:c,on_mount:l,on_destroy:u,after_update:a}=t.$$;c&&c.m(e,s),i||U((()=>{const e=l.map(n).filter(o);u?u.push(...e):r(e),t.$$.on_mount=[]})),a.forEach(U)}function ot(t,e){const n=t.$$;null!==n.fragment&&(r(n.on_destroy),n.fragment&&n.fragment.d(e),n.on_destroy=n.fragment=null,n.ctx=[])}function it(e,n,o,i,c,l,u=[-1]){const a=O;I(e);const f=e.$$={fragment:null,ctx:null,props:l,update:t,not_equal:c,bound:s(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(a?a.$$.context:n.context||[]),callbacks:s(),dirty:u,skip_bound:!1};let d=!1;if(f.ctx=o?o(e,n.props||{},((t,n,...s)=>{const r=s.length?s[0]:n;return f.ctx&&c(f.ctx[t],f.ctx[t]=r)&&(!f.skip_bound&&f.bound[t]&&f.bound[t](r),d&&function(t,e){-1===t.$$.dirty[0]&&(N.push(t),G(),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}(e,t)),n})):[],f.update(),d=!0,r(f.before_update),f.fragment=!!i&&i(f.ctx),n.target){if(n.hydrate){const t=x(n.target);f.fragment&&f.fragment.l(t),t.forEach(p)}else f.fragment&&f.fragment.c();n.intro&&W(e.$$.fragment),rt(e,n.target,n.anchor,n.customElement),F()}I(a)}class ct{$destroy(){ot(this,1),this.$destroy=t}$on(t,e){const n=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return n.push(e),()=>{const t=n.indexOf(e);-1!==t&&n.splice(t,1)}}$set(t){var e;this.$$set&&(e=t,0!==Object.keys(e).length)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}const lt=[];function ut(e,n=t){let s;const r=[];function o(t){if(i(e,t)&&(e=t,s)){const t=!lt.length;for(let n=0;n<r.length;n+=1){const t=r[n];t[1](),lt.push(t,e)}if(t){for(let t=0;t<lt.length;t+=2)lt[t][0](lt[t+1]);lt.length=0}}}return{set:o,update:function(t){o(t(e))},subscribe:function(i,c=t){const l=[i,c];return r.push(l),1===r.length&&(s=n(o)||t),i(e),()=>{const t=r.indexOf(l);-1!==t&&r.splice(t,1),0===r.length&&(s(),s=null)}}}}function at(t){let e,n;return{c(){e=g("source"),this.h()},l(t){e=k(t,"SOURCE",{type:!0,srcset:!0,sizes:!0}),this.h()},h(){w(e,"type","image/avif"),w(e,"srcset",n=t[15]?t[4]:void 0),w(e,"sizes",t[12])},m(t,n){h(t,e,n)},p(t,s){32784&s&&n!==(n=t[15]?t[4]:void 0)&&w(e,"srcset",n),4096&s&&w(e,"sizes",t[12])},d(t){t&&p(e)}}}function ft(t){let e,n;return{c(){e=g("source"),this.h()},l(t){e=k(t,"SOURCE",{type:!0,srcset:!0,sizes:!0}),this.h()},h(){w(e,"type","image/webp"),w(e,"srcset",n=t[15]?t[3]:void 0),w(e,"sizes",t[12])},m(t,n){h(t,e,n)},p(t,s){32776&s&&n!==(n=t[15]?t[3]:void 0)&&w(e,"srcset",n),4096&s&&w(e,"sizes",t[12])},d(t){t&&p(e)}}}function dt(t){let e,n;return{c(){e=g("img"),this.h()},l(t){e=k(t,"IMG",{class:!0,src:!0,alt:!0,width:!0,height:!0}),this.h()},h(){w(e,"class","placeholder svelte-2nujil"),e.src!==(n=t[5])&&w(e,"src",n),w(e,"alt",t[0]),w(e,"width",t[11]),w(e,"height",t[14])},m(t,n){h(t,e,n)},p(t,s){32&s&&e.src!==(n=t[5])&&w(e,"src",n),1&s&&w(e,"alt",t[0]),2048&s&&w(e,"width",t[11]),16384&s&&w(e,"height",t[14])},d(t){t&&p(e)}}}function ht(e){let n,s,r,o,i,c,l,u,a,f,m,$,b,y,_=e[4]&&at(e),z=e[3]&&ft(e),j=!e[7]&&dt(e);return{c(){n=g("div"),s=g("picture"),_&&_.c(),r=v(),z&&z.c(),o=v(),i=g("img"),f=v(),j&&j.c(),this.h()},l(t){n=k(t,"DIV",{style:!0,class:!0});var e=x(n);s=k(e,"PICTURE",{class:!0});var c=x(s);_&&_.l(c),r=E(c),z&&z.l(c),o=E(c),i=k(c,"IMG",{srcset:!0,sizes:!0,alt:!0,width:!0,height:!0,loading:!0,class:!0}),c.forEach(p),f=E(e),j&&j.l(e),e.forEach(p),this.h()},h(){w(i,"srcset",c=e[15]?e[2]:void 0),w(i,"sizes",e[12]),w(i,"alt",l=e[16]?e[0]:void 0),w(i,"width",e[11]),w(i,"height",e[14]),w(i,"loading",u=e[7]?void 0:"lazy"),w(i,"class",a="image "+(e[16]?"loaded":"")+" svelte-2nujil"),w(s,"class","svelte-2nujil"),w(n,"style",m=(e[10]?`max-width:${e[6]}px;`:"")+" --svimg-blur:"+e[8]+"px"),w(n,"class",$="wrapper "+e[1]+" svelte-2nujil")},m(t,c){var l,u,a,p;h(t,n,c),d(n,s),_&&_.m(s,null),d(s,r),z&&z.m(s,null),d(s,o),d(s,i),d(n,f),j&&j.m(n,null),e[25](n),b||(l=i,u="load",a=e[24],l.addEventListener(u,a,p),y=()=>l.removeEventListener(u,a,p),b=!0)},p(t,[e]){t[4]?_?_.p(t,e):(_=at(t),_.c(),_.m(s,r)):_&&(_.d(1),_=null),t[3]?z?z.p(t,e):(z=ft(t),z.c(),z.m(s,o)):z&&(z.d(1),z=null),32772&e&&c!==(c=t[15]?t[2]:void 0)&&w(i,"srcset",c),4096&e&&w(i,"sizes",t[12]),65537&e&&l!==(l=t[16]?t[0]:void 0)&&w(i,"alt",l),2048&e&&w(i,"width",t[11]),16384&e&&w(i,"height",t[14]),128&e&&u!==(u=t[7]?void 0:"lazy")&&w(i,"loading",u),65536&e&&a!==(a="image "+(t[16]?"loaded":"")+" svelte-2nujil")&&w(i,"class",a),t[7]?j&&(j.d(1),j=null):j?j.p(t,e):(j=dt(t),j.c(),j.m(n,null)),1344&e&&m!==(m=(t[10]?`max-width:${t[6]}px;`:"")+" --svimg-blur:"+t[8]+"px")&&w(n,"style",m),2&e&&$!==($="wrapper "+t[1]+" svelte-2nujil")&&w(n,"class",$)},i:t,o:t,d(t){t&&p(n),_&&_.d(),z&&z.d(),j&&j.d(),e[25](null),b=!1,y()}}}function pt(t,e,n){let s,r,o,i,c,l,u,a,{src:f}=e,{alt:d}=e,{class:h=""}=e,{srcset:p}=e,{srcsetwebp:m}=e,{srcsetavif:g}=e,{placeholder:$=""}=e,{width:b}=e,{aspectratio:v}=e,{immediate:y=!1}=e,{blur:w=40}=e,{quality:x=""}=e,k=!1,_=!1,E=!1,z=!0;C((()=>{(G(),L).then((()=>{let t;if(window.ResizeObserver?(t=new ResizeObserver((t=>{n(20,u=t[0].contentRect.width)})),t.observe(a)):n(23,z=!1),n(22,_="loading"in HTMLImageElement.prototype),_||y)return()=>{t&&t.unobserve(a)};const e=new IntersectionObserver((t=>{n(21,k=t[0].isIntersecting),k&&e.unobserve(a)}),{rootMargin:"100px"});return e.observe(a),()=>{e.unobserve(a),t&&t.unobserve(a)}}))}));return t.$$set=t=>{"src"in t&&n(17,f=t.src),"alt"in t&&n(0,d=t.alt),"class"in t&&n(1,h=t.class),"srcset"in t&&n(2,p=t.srcset),"srcsetwebp"in t&&n(3,m=t.srcsetwebp),"srcsetavif"in t&&n(4,g=t.srcsetavif),"placeholder"in t&&n(5,$=t.placeholder),"width"in t&&n(6,b=t.width),"aspectratio"in t&&n(18,v=t.aspectratio),"immediate"in t&&n(7,y=t.immediate),"blur"in t&&n(8,w=t.blur),"quality"in t&&n(19,x=t.quality)},t.$$.update=()=>{64&t.$$.dirty&&n(10,s=!(!b||!/^[0-9]+$/.test(b))),1049664&t.$$.dirty&&n(11,r=s&&u?Math.min(u,b):s?b:u),264192&t.$$.dirty&&n(14,o=r/v),2048&t.$$.dirty&&n(12,i=r?`${r}px`:void 0),14684288&t.$$.dirty&&n(15,c=(k||_||y)&&(i||!z)),640&t.$$.dirty&&n(16,l=E||y)},[d,h,p,m,g,$,b,y,w,E,s,r,i,a,o,c,l,f,v,x,u,k,_,z,()=>n(9,E=!0),function(t){R[t?"unshift":"push"]((()=>{a=t,n(13,a)}))}]}class mt extends ct{constructor(t){super(),it(this,t,pt,ht,i,{src:17,alt:0,class:1,srcset:2,srcsetwebp:3,srcsetavif:4,placeholder:5,width:6,aspectratio:18,immediate:7,blur:8,quality:19})}}export{e as A,V as B,ut as C,d as D,t as E,$ as F,c as G,u as H,f as I,o as J,a as K,j as L,Z as M,m as N,Y as O,mt as P,ct as S,x as a,w as b,k as c,p as d,g as e,h as f,_ as g,z as h,it as i,nt as j,v as k,y as l,st as m,E as n,rt as o,tt as p,et as q,X as r,i as s,b as t,Q as u,W as v,ot as w,A as x,q as y,C as z};
