var VIZ = VIZ || (function () {


  return {
      test : function(scores_json) {
          console.log(scores_json);
      },

      createVisualization: function(scores) {

        var margin = {top: 20, right: 20, bottom: 20, left: 60},
          padding = {top: 60, right: 60, bottom: 60, left: 120},
          outerWidth = 960,
          outerHeight = 500,
          innerWidth = outerWidth - margin.left - margin.right,
          innerHeight = outerHeight - margin.top - margin.bottom,
          w = innerWidth - padding.left - padding.right,
          h = innerHeight - padding.top - padding.bottom;

        // create SVG elem
        var svg = d3.select("#viz")
                    .append("svg")
                    .attr("width", outerWidth)
                    .attr("height", outerHeight)
                  .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var max_followers = d3.max(scores, function(d) {
          // references "followers" property of each object in scores
          return d.followers
        });

        var rScale = d3.scale.linear()
                      .domain([0, max_followers])
                      .range([10, 60])


        var circles = svg.selectAll("circle")
          .data(scores)
          .enter()
          .append("circle");


        circles.attr("cx", function(d, i) {
            // assign a dynamic value that corresponds to i, or each value’s position in the data set
            console.log("CX " + ((i+1) * (w / scores.length)))
            return (i+1) * (w / scores.length);
          })
          .attr("cy", function(d) {
            console.log("CY " + (1 - d.score) * h)
            return (1 - d.score) * h;
          })
          .attr("r", function(d) {
            return rScale(d.followers);
          })
          .attr("stroke", "gray")
          .attr("fill", function(d) {
              return "rgba(0, 0, 255, " + d.score + ")"
          });

        circles.on("mouseover", function(d){
            console.log(d);

            var screenName = d.screen_name;
            var xPosition = parseFloat(d3.select(this).attr("cx"));
            var yPosition = parseFloat(d3.select(this).attr("cy")) - parseFloat(d3.select(this).attr("r") + 3);
            svg.append("text")
                .attr("id", "tooltip")
                .attr("x", xPosition)
                .attr("y", yPosition)
                .attr("text-anchor", "middle")
                .attr("font-family", "sans-serif")
                .attr("font-size", "11px")
                .attr("font-weight", "bold")
                .attr("fill", "black")
                .text(screenName);

            d3.select(this)
              .attr("fill", "orange");
          })
          .on("mouseout", function(d) {
            d3.select("#tooltip").remove();
            d3.select(this)
              .attr("fill", "rgba(0, 0, 255, " + d.score + ")");
          });

      }
    };
}());
