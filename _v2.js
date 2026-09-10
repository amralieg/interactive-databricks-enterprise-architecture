const { chromium } = require("playwright");
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1700,height:1050}});
  await p.addInitScript(()=>{try{localStorage.setItem("dbx-arch-tour-v1","1")}catch(e){}});
  await p.goto("http://localhost:8035/app/index.html",{waitUntil:"networkidle"});
  await p.waitForTimeout(1400);
  const R={};
  // highlights default: fresh storage -> all on -> label "Highlights", and menu rows all 'on'
  R.hl = await p.evaluate(()=>{
    document.getElementById("hl-btn").click();
    const rows=[...document.querySelectorAll("#hl-menu button")].filter(x=>x.dataset.hl);
    const onCount=rows.filter(x=>x.classList.contains("on")).length;
    const lbl=document.getElementById("hl-lbl").textContent;
    document.getElementById("hl-btn").click();
    return {total:rows.length, on:onCount, label:lbl};
  });
  // compute tiles present with subtexts
  R.compute = await p.evaluate(()=>{
    const out=[];
    document.querySelectorAll(".atom").forEach(e=>{
      const n=(e.innerText||"").split("\n")[0].trim();
      if(n==="Serverless Compute"||n==="Classic Compute") out.push((e.innerText||"").replace(/\n/g," | ").trim());
    });
    return out;
  });
  R.region = await p.evaluate(()=>document.getElementById("region-lbl").textContent);
  // screenshot the cloud services band + toolbar
  const band = await p.$(".band-row, .band");
  await p.screenshot({path:"/tmp/board_full.png"});
  // toolbar close-up
  const tb = await p.$("#hl-btn");
  if(tb){ const box=await tb.boundingBox(); await p.screenshot({path:"/tmp/hlbtn.png", clip:{x:Math.max(0,box.x-10),y:Math.max(0,box.y-10),width:260,height:box.height+20}}); }
  console.log(JSON.stringify(R,null,1));
  await b.close();
})();
