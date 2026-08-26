document.body.classList.remove('theme-dark');
applyIndustry('airlines', false);
applyShape('z', false);
fitBoard();
boardPngBlob(2).then(function(r){
  return new Promise(function(res){
    var fr = new FileReader();
    fr.onload = function(){ res(JSON.stringify({w:r.w, h:r.h, data:fr.result})); };
    fr.readAsDataURL(r.blob);
  });
}).then(function(s){
  document.body.innerHTML = '<pre id="OUT">' + s + '</pre>';
});
