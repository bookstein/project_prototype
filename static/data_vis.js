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
    .attr("cx", function(d, i) {
      // assign a dynamic value that corresponds to i, or each value’s position in the data set
      return i * (w / scores.length);
    })
    .attr("cy", function(d) {
      return d;
    })
    .attr("r", 10)

})();