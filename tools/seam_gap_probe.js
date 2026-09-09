document.body.classList.remove("theme-dark");
function measure(ind){
  applyIndustry(ind, false);
  applyShape("z", false);
  fitBoard();
  var top = document.getElementById("plat-top");
  var body = document.getElementById("platform");
  var work = document.querySelector(".band.b-work");
  var foot = work && work.querySelector(".band-foot");
  var ppl = document.querySelector(".pocket.ppl") || document.querySelector(".rail.ppl");
  var r = function(a,b){ return a&&b ? Math.round(b.getBoundingClientRect().top - a.getBoundingClientRect().bottom) : -1; };
  return {
    industry: ind,
    topH: top ? Math.round(top.getBoundingClientRect().height) : -1,
    bodyH: body ? Math.round(body.getBoundingClientRect().height) : -1,
    seam: r(top, body),
    workToTopBottom: work && top ? Math.round(top.getBoundingClientRect().bottom - work.getBoundingClientRect().bottom) : -1,
    footToTopBottom: foot && top ? Math.round(top.getBoundingClientRect().bottom - foot.getBoundingClientRect().bottom) : -1,
    pplH: ppl ? Math.round(ppl.getBoundingClientRect().height) : -1,
    fitH: document.getElementById("fit-in").offsetHeight
  };
}
var out = ["airlines","generic"].map(function(i){
  try { return measure(i); } catch(e){ return {industry:i, err:String(e)}; }
});
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify(out, null, 2) + '</pre>';
