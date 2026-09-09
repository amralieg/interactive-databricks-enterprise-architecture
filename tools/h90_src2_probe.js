function srcH(id){
  applyIndustry(id, false);
  applyShape("h90", false);
  fitBoard();
  return {
    board: document.getElementById("board").offsetHeight,
    srcH: document.querySelector(".rail.src").offsetHeight,
    srcCols: getComputedStyle(document.querySelector(".rail.src")).flexDirection
  };
}
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({generic:srcH("generic"),airlines:srcH("airlines")}) + '</pre>';
