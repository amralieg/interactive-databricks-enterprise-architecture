function names(){
  return [].map.call(document.querySelectorAll(".rail.ppl .rtile .t-name"), function(n){
    return n.textContent;
  }).sort().join("|");
}
applyIndustry("airlines", false);
applyShape("z", false);
fitBoard();
var z = names();
applyShape("h90", false);
fitBoard();
var h90 = names();
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({z:z.split("|"), h90:h90.split("|"), same:z===h90}) + '</pre>';
