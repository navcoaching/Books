// يبني PDF الدليل المجاني ولقطات الصفحات
import { createRequire } from 'module'; import path from 'path'; import fs from 'fs'; import { fileURLToPath } from 'url';
const require=createRequire(import.meta.url); const pw=require('/opt/node-tools/node_modules/playwright');
const here=path.dirname(fileURLToPath(import.meta.url)); const shots=process.argv[2];
const b=await pw.chromium.launch(); const p=await b.newPage({viewport:{width:900,height:1200},deviceScaleFactor:1.5});
await p.goto('file://'+path.join(here,'guide.html'));
await p.evaluate(()=>Promise.all([...document.fonts].map(f=>f.load().catch(()=>0))));
await p.evaluate(()=>document.fonts.ready);
const over=await p.evaluate(()=>[...document.querySelectorAll('.page')].map((pg,i)=>{const r=pg.getBoundingClientRect();const bad=[...pg.querySelectorAll('.in > *')].some(e=>e.getBoundingClientRect().bottom>r.bottom-22*3.78);return bad?i+1:0}).filter(Boolean));
console.log('overflow pages:',JSON.stringify(over));
if(shots){fs.mkdirSync(shots,{recursive:true});const els=await p.$$('.page');for(let i=0;i<els.length;i++)await els[i].screenshot({path:path.join(shots,`g${String(i+1).padStart(2,'0')}.png`)});}
const out=path.join(here,'..','output','navcoaching-28-day-challenge.pdf');
await p.emulateMedia({media:'print'}); await p.pdf({path:out,preferCSSPageSize:true,printBackground:true,tagged:true});
console.log(out); await b.close();
