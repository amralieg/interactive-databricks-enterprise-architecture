applyIndustry("airlines", false);
applyShape("z", false);
fitBoard();
function voidPx(parent, child){
  if(!parent || !child) return -1;
  var pr = parent.getBoundingClientRect(), cr = child.getBoundingClientRect();
  return Math.round(pr.bottom - cr.bottom);
}
function gapBelow(el){
  if(!el || !el.parentElement) return -1;
  var er = el.getBoundingClientRect(), pr = el.parentElement.getBoundingClientRect();
  return Math.round(pr.bottom - er.bottom);
}
var panel = document.querySelector(".band.b-work .panel");
var panelCols = panel && panel.querySelector(".panel-cols");
var mixed = document.querySelector(".band.b-work .band-row.mixed");
var work = document.querySelector(".band.b-work");
var platTop = document.querySelector(".plat-top");
var platBody = document.querySelector(".plat-body");
var ingestCards = [].map.call(document.querySelectorAll(".arm.left .pcard"), function(c){
  return { n: c.querySelector(".p-name").textContent, h: c.offsetHeight };
});
var bodyBands = [].map.call(document.querySelectorAll(".plat-body .plat-stack > .band"), function(b){
  return { id: b.className.match(/b-(\w+)/)[1], h: b.offsetHeight, gapIn: gapBelow(b.querySelector(".band-body") || b) };
});
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({
  fitH: document.getElementById("fit-in").offsetHeight,
  platTopH: platTop.offsetHeight,
  platBodyH: platBody.offsetHeight,
  workH: work.offsetHeight,
  panelH: panel ? panel.offsetHeight : 0,
  panelVoidBelowCols: panelCols ? voidPx(panel, panelCols) : -1,
  mixedVoidBelow: mixed ? gapBelow(mixed) : -1,
  ingestCards: ingestCards,
  bodyBands: bodyBands
}, null, 2) + '</pre>';
