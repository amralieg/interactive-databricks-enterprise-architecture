applyIndustry("generic", false);
applyShape("z", false);
fitBoard();
var chips = [].map.call(document.querySelectorAll(".band.b-work .side-col .schip"), function(c){
  var r = c.getBoundingClientRect();
  var scale = c.offsetWidth ? (r.width / c.offsetWidth) : 1;
  return { n: c.textContent.trim(), w: c.offsetWidth, h: c.offsetHeight, square: c.offsetWidth === c.offsetHeight };
});
var gaps = [];
var col = document.querySelector(".band.b-work .side-col");
if(col){
  var kids = col.querySelectorAll(".schip");
  for(var i = 0; i < kids.length - 1; i++){
    gaps.push(Math.round(kids[i+1].getBoundingClientRect().top - kids[i].getBoundingClientRect().bottom));
  }
}
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({ chips: chips, gaps: gaps }, null, 2) + '</pre>';
