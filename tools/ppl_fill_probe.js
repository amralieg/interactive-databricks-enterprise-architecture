applyIndustry("airlines", false);
applyShape("z", false);
fitBoard();
var pocket = document.querySelector(".pocket.ppl");
var rail = document.querySelector(".rail.ppl");
var head = pocket.querySelector(".pockhead");
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({
  pocketH: pocket.offsetHeight,
  headH: head.offsetHeight,
  railH: rail.offsetHeight,
  railClientH: rail.clientHeight,
  railScrollH: rail.scrollHeight,
  techTileH: rail.querySelector(".rgroup:last-child .rtile").offsetHeight,
  bizGh: rail.querySelector(".rgroup:first-child").offsetHeight,
  techGh: rail.querySelector(".rgroup:last-child").offsetHeight,
  railFlex: getComputedStyle(rail).flex,
  pocketDisplay: getComputedStyle(pocket).display
}) + '</pre>';
