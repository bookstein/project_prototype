(function () {
    function barchart () {
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

            barchart.append("text")
                .text("Average Values Over Time")
                .attr("x", (width / 2))
                .attr("y", 0 - (margin.top / 2))
                .attr("class", "title")
                .attr("text-anchor", "middle");

            barchart.append("g")
                .attr("class", "xAxis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            barchart.append("g")
                .attr("class", "yAxis")
                .call(yAxis)
              //`.append("text");

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
                .on("mouseover", function (d) { linechart(d); })
                .on("mouseout", remove_linechart) ;
        });
    }

    function linechart (hovered_d) {
        var filename = hovered_d.city.replace(/\s+/g, '_').toLowerCase();

        var margin = {top: 30, right: 40, bottom: 40, left: 40},
            width = 500 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        var x = d3.time.scale()
            .range([0, width]);

        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(6)
            .tickFormat(d3.time.format("%Y"));

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        var line = d3.svg.line()
            .x(function(d) { return x(new Date(parseInt(d.date))); })
            .y(function(d) { return y(d.value); });

        var linechart = d3.select("#linechart")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        d3.csv("data/" + filename + ".csv", function(error, data) {

            x.domain(d3.extent(data, function(d) { return new Date(parseInt(d.date)) }));
            y.domain([0, 110]);

            linechart.append("text")
                .text(hovered_d.city + " Values Over Time")
                .attr("x", (width / 2))
                .attr("y", 0 - (margin.top / 2))
                .attr("class", "title")
                .attr("text-anchor", "middle");

            linechart.append("g")
                .attr("class", "xAxis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            linechart.append("g")
                .attr("class", "yAxis")
                .call(yAxis);

            linechart.append("path")
                .datum(data)
                .attr("class", hovered_d.city.replace(/\s+/g, "-").toLowerCase())
                .attr("d", line);

        });
    }

    function remove_linechart () {
        d3.select("#linechart").html("");
    }

    // Here's where we call the function
    barchart();
})();