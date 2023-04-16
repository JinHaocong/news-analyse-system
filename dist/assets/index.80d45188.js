import{d as N}from"./index.9c04d98c.js";import{l as r,q as p,A as b,y as e,x as n,F as _,G as g,Q as j,P as L,H as z,C as y,N as S,O as I,t as U}from"./element-plus.06a878fd.js";const C={data(){return{text:"",commentList:[],commentForm:{_txts__icontains:null,_positive:null,total:0,page:1,pagesize:50},centerDialogVisible:!1}},beforeMount(){this.search()},methods:{jsonify(l){return JSON.parse(l)},highlight(){if(this.commentForm._txts__icontains){const l=this.commentForm._txts__icontains,o=new RegExp(this.commentForm._txts__icontains,"ig");return this.text.replace(o,`<span style="color:red;font-weight:bold;">${l}</span>`)}return this.text},ellipsis(l,o=50){return l.length>o?`${l.substring(0,o)}...`:l},showDl(l){this.text=l,this.centerDialogVisible=!0},viewNewsDetail(l){this.$router.push({name:"Detail",params:{id:l}})},viewCommentDetail(l,o){localStorage.setItem("text",l.trim()),this.$router.push({name:"AnalyseList",params:{subject:o}})},handleCurrentChange(l){this.commentForm.page=l,this.getlist()},search(){this.commentForm.page=1,this.getlist()},getlist(){N.post("/news/",this.commentForm).then(l=>{this.commentList=l.data.result,this.commentForm.total=l.data.total})}}},B=l=>(S("data-v-76bcde84"),l=l(),I(),l),H={style:{padding:"30px"}},M=_("\u641C\u7D22"),T=B(()=>y("div",{class:"image-slot"},"\u6682\u65E0\u5C01\u9762\u56FE",-1)),q=_("\u5185\u5BB9\u5206\u6790 "),A=["innerHTML"];function E(l,o,O,G,a,i){const d=r("el-input"),c=r("el-form-item"),h=r("el-button"),w=r("el-form"),f=r("el-row"),x=r("el-image"),u=r("el-link"),s=r("el-table-column"),k=r("el-tag"),F=r("el-table"),V=r("el-pagination"),v=r("el-card"),D=r("el-dialog");return p(),b("div",H,[e(f,{type:"flex",justify:"center"},{default:n(()=>[e(w,{model:a.commentForm,inline:!0},{default:n(()=>[e(c,{label:"\u6807\u9898"},{default:n(()=>[e(d,{modelValue:a.commentForm._title__icontains,"onUpdate:modelValue":o[0]||(o[0]=t=>a.commentForm._title__icontains=t),clearable:"",onChange:i.search},null,8,["modelValue","onChange"])]),_:1}),e(c,{label:"\u5185\u5BB9"},{default:n(()=>[e(d,{modelValue:a.commentForm._text__icontains,"onUpdate:modelValue":o[1]||(o[1]=t=>a.commentForm._text__icontains=t),clearable:"",onChange:i.search},null,8,["modelValue","onChange"])]),_:1}),e(c,{label:"\u6807\u7B7E"},{default:n(()=>[e(d,{modelValue:a.commentForm._keywords__icontains,"onUpdate:modelValue":o[2]||(o[2]=t=>a.commentForm._keywords__icontains=t),clearable:"",onChange:i.search},null,8,["modelValue","onChange"])]),_:1}),e(c,{label:"\u6765\u6E90\u5A92\u4F53"},{default:n(()=>[e(d,{modelValue:a.commentForm._media_name__icontains,"onUpdate:modelValue":o[3]||(o[3]=t=>a.commentForm._media_name__icontains=t),clearable:"",onChange:i.search},null,8,["modelValue","onChange"])]),_:1}),e(c,null,{default:n(()=>[e(h,{type:"primary",onClick:i.search},{default:n(()=>[M]),_:1},8,["onClick"])]),_:1})]),_:1},8,["model"])]),_:1}),e(F,{data:a.commentList,style:{width:"100%",margin:"20px 10px"}},{default:n(()=>[e(s,{label:"\u5C01\u9762",prop:"img",align:"center",width:"180"},{default:n(({row:t})=>[e(u,{type:"primary",underline:!1,onClick:m=>i.viewNewsDetail(t.id)},{default:n(()=>[e(x,{src:i.jsonify(t.img).u,style:{width:"180px",height:"150px"}},{error:n(()=>[T]),_:2},1032,["src"])]),_:2},1032,["onClick"])]),_:1}),e(s,{label:"\u6807\u9898",prop:"title",sortable:"",align:"center"},{default:n(({row:t})=>[e(u,{type:"primary",underline:!1,onClick:m=>i.viewNewsDetail(t.id)},{default:n(()=>[_(g(t.title),1)]),_:2},1032,["onClick"])]),_:1}),e(s,{label:"\u7B80\u4ECB",prop:"intro",sortable:""},{default:n(({row:t})=>[e(u,{type:"info",underline:!1,onClick:m=>i.showDl(t.intro)},{default:n(()=>[_(g(i.ellipsis(t.intro)),1)]),_:2},1032,["onClick"])]),_:1}),e(s,{label:"\u6807\u7B7E",prop:"keywords",width:"180",sortable:""},{default:n(({row:t})=>[t.keywords?(p(!0),b(j,{key:0},L(t.keywords.split(","),m=>(p(),U(k,{key:m,type:"info",style:{margin:"0 5px 5px 0",cursor:"pointer"},effect:"plain",size:"mini",onClick:J=>{a.commentForm._keywords__icontains=m,i.search()}},{default:n(()=>[_(g(m),1)]),_:2},1032,["onClick"]))),128)):z("",!0)]),_:1}),e(s,{label:"\u6765\u6E90\u5A92\u4F53",prop:"media_name",width:"150",sortable:""}),e(s,{label:"\u53D1\u5E03\u65E5\u671F",prop:"intime",width:"150",sortable:""}),e(s,{label:"\u70B9\u51FB\u7387",prop:"view_count",width:"150",sortable:""}),e(s,{label:"\u64CD\u4F5C",align:"center",width:"180",sortable:""},{default:n(t=>[e(h,{type:"primary",size:"mini",onClick:m=>i.viewCommentDetail(t.row.text,t.row.subject)},{default:n(()=>[q]),_:2},1032,["onClick"])]),_:1})]),_:1},8,["data"]),e(f,{type:"flex",justify:"center",style:{"margin-top":"30px"}},{default:n(()=>[e(V,{"current-page":a.commentForm.page,"page-size":a.commentForm.pagesize,layout:"prev, pager, next, jumper, total",total:a.commentForm.total,background:"",onCurrentChange:i.handleCurrentChange},null,8,["current-page","page-size","total","onCurrentChange"])]),_:1}),e(D,{modelValue:a.centerDialogVisible,"onUpdate:modelValue":o[4]||(o[4]=t=>a.centerDialogVisible=t),title:"\u7B80\u4ECB",width:"70%","destroy-on-close":"",center:""},{default:n(()=>[e(v,{shadow:"always",style:{"margin-bottom":"20px","background-color":"#f6f6f6"}},{default:n(()=>[y("div",{innerHTML:i.highlight()},null,8,A)]),_:1})]),_:1},8,["modelValue"])])}C.render=E;C.__scopeId="data-v-76bcde84";export{C as default};
