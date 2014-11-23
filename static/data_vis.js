(function () {

  var scores = [20, 30, 40, 50]

  var w = 960,
    h = 600

  // set radius proportional to num of followers

  // create SVG elem
  var svg = d3.select("body")
              .append("svg")
              .attr("width", w)
              .attr("height", h);

  svg.selectAll("circle")
    .data(scores)
    .enter()
    .append("circle")
    .attr("cx", 200)
    .attr("cy", 200)
    .attr("r", 10)

})();