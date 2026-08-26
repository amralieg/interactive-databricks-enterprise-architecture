function ingDetail(id){
  applyIndustry(id, false);
  applyShape("h90", false);
  fitBoard();
  return [].map.call(document.querySelectorAll(".rail.ing .rgroup"), function(g){
    return {
      label: g.querySelector(".rg-label").textContent,
      gh: Math.round(g.getBoundingClientRect().height),
      tiles: g.querySelectorAll(".rtile").length
    };
  });
}
document.body.innerHTML = '<pre id="OUT">' + JSON.stringify({generic:ingDetail("generic"),airlines:ingDetail("airlines")}) + '</pre>';
