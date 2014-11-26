var VIZ = VIZ || (function () {


  return {
      test : function(scores_json) {
          console.log(scores_json);
      },

      createVisualization: function(scores) {

        var margin = {top: 20, right: 20, bottom: 20, left: 20},
          padding = {top: 60, right: 60, bottom: 60, left: 60},
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
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");;

        var max_followers = d3.max(scores, function(d) {
          // references "followers" property of each object in scores
          return d.followers
        });

        // var x = d3.scale.linear()
        //     .range([0, w]);

        // var y = d3.scale.linear()
        //     .range([h, 0]);

        var rScale = d3.scale.linear()
                      .domain([0, max_followers])
                      .range([2, 30])


        var circles = svg.selectAll("circle")
          .data(scores)
          .enter()
          .append("circle");


        circles.attr("cx", function(d, i) {
            // assign a dynamic value that corresponds to i, or each value’s position in the data set
            console.log("CX " + (i * (w / scores.length)))
            return i * (w / scores.length);
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
            console.log(d.score*255)
            return "rgb(0, 0, " + (d.score * 255) + ")";
          });

        // add svg "text" elements
        svg.selectAll("text")
         .data(scores)
         .enter()
         .append("text")
         .text(function(d) {
              return d;
         })
         .attr("x", function(d, i) {
              return i * (w / scores.length);
         })
         .attr("y", 100)
         .attr("font-family", "sans-serif")
         .attr("font-size", "11px")
         .attr("fill", "white")
         // center the text horizontally at the assigned x value
         .attr("text-anchor", "middle");


      }

    };
}());


// var scores = [20, 30, 40, 50, 60, 70, 80, 90, 20, 30, 40, 50, 60,];

// var w = 960,
//   h = 600;


// // set radius proportional to num of followers

// // create SVG elem
// var svg = d3.select("body")
//             .append("svg")
//             .attr("width", w)
//             .attr("height", h);

// svg.selectAll("circle")
//   .data(scores)
//   .enter()
//   .append("circle")
//   .attr("cx", function(d, i) {
//     // assign a dynamic value that corresponds to i, or each value’s position in the data set
//     return i * (w / scores.length);
//   })
//   .attr("cy", 100)
//   .attr("r", function(d) {
//     return d;
//   })
//   .attr("fill", function(d) {
//     return "rgb(0, 0, " + (d * 5) + ")";
//   });

// // add svg "text" elements
// svg.selectAll("text")
//  .data(scores)
//  .enter()
//  .append("text")
//  .text(function(d) {
//       return d;
//  })
//  .attr("x", function(d, i) {
//       return i * (w / scores.length);
//  })
//  .attr("y", 100)
//  .attr("font-family", "sans-serif")
//  .attr("font-size", "11px")
//  .attr("fill", "white")
//  // center the text horizontally at the assigned x value
//  .attr("text-anchor", "middle");
