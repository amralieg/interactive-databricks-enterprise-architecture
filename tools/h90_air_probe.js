applyIndustry("airlines", false);
applyShape("h90", false);
fitBoard();
var ppl = [].map.call(document.querySelectorAll(".rail.ppl .rgroup"), function(g){
  return {
    label: g.querySelector(".rg-label").textContent,
    tiles: [].map.call(g.querySelectorAll(".rtile .t-name"), function(n){ return n.textContent; }),
    gh: g.offsetHeight
  };
});
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({
  board: document.getElementById("board").offsetHeight,
  ref: 1402,
  scale: Math.round(document.getElementById("board").getBoundingClientRect().width / 2200 * 1000) / 1000,
  ppl: ppl,
  srcH: document.querySelector(".rail.src").offsetHeight
}) + '</pre>';
