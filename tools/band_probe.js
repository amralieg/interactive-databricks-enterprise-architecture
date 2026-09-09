applyIndustry("generic", false);
fitBoard();
function hues(el){
  return [].map.call(el.querySelectorAll(".ctile"), function(t){
    return (t.className.match(/ct-h-(\w+)/) || [])[1] || "none";
  });
}
var top=document.getElementById("topband");
var bot=document.getElementById("cloud");
document.body.innerHTML='<pre id="OUT">'+JSON.stringify({
  topHues:hues(top), topUnique:[...new Set(hues(top))].length,
  botHues:hues(bot), botUnique:[...new Set(hues(bot))].length,
  botCols:[].map.call(bot.querySelectorAll('.cloud-body'),b=>b.style.gridTemplateColumns)
},null,2)+'</pre>';
