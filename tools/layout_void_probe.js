applyIndustry("airlines", false);
applyShape("z", false);
document.body.classList.remove("theme-dark");
fitBoard();
function gapBelow(el){
  if(!el || !el.parentElement) return -1;
  var er = el.getBoundingClientRect(), pr = el.parentElement.getBoundingClientRect();
  return Math.round(pr.bottom - er.bottom);
}
var work = document.querySelector(".band.b-work");
var workBody = work && work.querySelector(".band-body");
var mixed = work && work.querySelector(".band-row.mixed");
var cards = work && work.querySelector(".band-row.cards");
var foot = work && work.querySelector(".band-foot");
function gapBetween(a, b){
  if(!a || !b) return -1;
  return Math.round(b.getBoundingClientRect().top - a.getBoundingClientRect().bottom);
}
function gapBelowEl(el){
  if(!el || !el.parentElement) return -1;
  var er = el.getBoundingClientRect(), pr = el.parentElement.getBoundingClientRect();
  return Math.round(pr.bottom - er.bottom);
}
var arm = document.querySelector(".arm.left .band");
var armCards = document.querySelector(".arm.left .band-row.cards");
var infra = document.querySelector(".band.b-infra");
var infraBody = infra && infra.querySelector(".band-body");
var cloud = document.getElementById("cloud");
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({
  fitH: document.getElementById("fit-in").offsetHeight,
  workH: work ? work.offsetHeight : 0,
  workBodyVoid: workBody && foot ? gapBelowEl(foot) : -1,
  mixedToCards: mixed && cards ? gapBetween(mixed, cards) : -1,
  contentToFoot: mixed && foot ? gapBetween(mixed, foot) : -1,
  armVoid: arm && armCards ? gapBelow(armCards) : -1,
  infraH: infra ? infra.offsetHeight : 0,
  infraVoid: infraBody ? gapBelow(infraBody) : -1,
  cloudBg: cloud ? getComputedStyle(cloud).backgroundColor : ""
}, null, 2) + '</pre>';
