document.body.classList.remove("theme-dark");
function biz(ind){
  applyIndustry(ind, false);
  applyShape("h90", false);
  fitBoard();
  var names = [];
  document.querySelectorAll(".rail.ppl .rgroup").forEach(function(g){
    var lbl = g.querySelector(".rg-label");
    var tiles = [].map.call(g.querySelectorAll(".t-name"), function(t){ return t.textContent; });
    names.push({ box: lbl ? lbl.textContent : "?", tiles: tiles });
  });
  return { industry: ind, groups: names };
}
function bizZ(ind){
  applyIndustry(ind, false);
  applyShape("z", false);
  fitBoard();
  var names = [];
  document.querySelectorAll(".rail.ppl .rgroup").forEach(function(g){
    var lbl = g.querySelector(".rg-label");
    var tiles = [].map.call(g.querySelectorAll(".t-name"), function(t){ return t.textContent; });
    names.push({ box: lbl ? lbl.textContent : "?", tiles: tiles });
  });
  return { industry: ind, shape: "z", groups: names };
}
var out = { z: ["airlines","generic"].map(bizZ), h90: ["airlines","generic"].map(biz) };
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify(out, null, 2) + '</pre>';
