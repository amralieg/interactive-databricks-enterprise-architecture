applyIndustry("generic", false);
applyShape("z", false);
fitBoard();
var work = document.querySelector(".band.b-work");
var top = document.querySelector(".plat-top");
var body = work && work.querySelector(".band-body");
var mixed = work && work.querySelector(".band-row.mixed");
var foot = work && work.querySelector(".band-foot");
function gapBelow(el, parent){
  if(!el || !parent) return -1;
  var er = el.getBoundingClientRect(), pr = parent.getBoundingClientRect();
  return Math.round(pr.bottom - er.bottom);
}
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({
  workH: work ? Math.round(work.offsetHeight) : 0,
  topH: top ? Math.round(top.offsetHeight) : 0,
  gapWorkToTop: gapBelow(work, top),
  gapMixedToFoot: body && mixed && foot ? Math.round(foot.getBoundingClientRect().top - mixed.getBoundingClientRect().bottom) : -1,
  gapFootToWork: gapBelow(foot, work)
}, null, 2) + '</pre>';
