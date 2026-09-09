function srcDetail(id){
  applyIndustry(id, false);
  applyShape("h90", false);
  fitBoard();
  return {
    railH: document.querySelector(".rail.src").offsetHeight,
    groups: [].map.call(document.querySelectorAll(".rail.src .rgroup"), function(g){
      return { label: g.querySelector(".rg-label").textContent, gh: g.offsetHeight, tiles: g.querySelectorAll(".rtile").length };
    })
  };
}
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({generic:srcDetail("generic"),airlines:srcDetail("airlines")}) + '</pre>';
