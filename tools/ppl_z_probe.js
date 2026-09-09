applyIndustry("airlines", false);
applyShape("z", false);
fitBoard();
var groups = [].map.call(document.querySelectorAll(".rail.ppl .rgroup"), function(g){
  return {
    label: g.querySelector(".rg-label").textContent,
    tiles: [].map.call(g.querySelectorAll(".rtile .t-name"), function(n){ return n.textContent; }),
    tileHs: [].map.call(g.querySelectorAll(".rtile"), function(n){ return n.offsetHeight; })
  };
});
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({groups:groups,count:document.querySelectorAll('.rail.ppl .rtile').length}) + '</pre>';
