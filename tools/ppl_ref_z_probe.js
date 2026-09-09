applyIndustry("generic", false);
applyShape("z", false);
fitBoard();
var groups = [].map.call(document.querySelectorAll(".rail.ppl .rgroup"), function(g){
  return {
    label: g.querySelector(".rg-label").textContent,
    tiles: [].map.call(g.querySelectorAll(".rtile .t-name"), function(n){ return n.textContent; }),
    gh: g.offsetHeight
  };
});
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({
  groups: groups,
  pocketH: document.querySelector(".pocket.ppl").offsetHeight,
  railH: document.querySelector(".rail.ppl").offsetHeight,
  gap: document.querySelector(".pocket.ppl").offsetHeight - document.querySelector(".rail.ppl").offsetHeight
}) + '</pre>';
