var margin = {top: 30, right: 40, bottom: 40, left: 40},
    width = 500 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .2, .15);

var y = d3.scale.linear()
        .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var barchart = d3.select("#barchart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("data/data.csv", function(error, data) {
    x.domain(data.map(function(d) { return d.city }));
    y.domain([0, 110]);

    barchart.append("g")
        .attr("class", "xAxis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    barchart.append("g")
        .attr("class", "yAxis")
        .call(yAxis)
      .append("text");
    
    barchart.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", function (d) {
            var city = d.city.replace(/\s+/g, '-').toLowerCase();
            return "bar " + city   
        })
        .attr("x", function(d) { return x(d.city); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.average) })
        .attr("height", function (d) { return height - y(d.average); })
        .on("mouseover", function() {
            d3.select(this)
            .attr("stroke", "black")
            .attr("stroke-width", "3px");
        })
        .on("mouseout", function() {
            d3.select(this)
            .attr("stroke", null)
            .attr("stroke-width", "0px")
        });

    barchart.append("text")
        .text("Average Values Over Time")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("class", "title")
        .attr("text-anchor", "middle");
});