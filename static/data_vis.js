var VIZ = VIZ || (function () {

  var _args = {}; // private

  return {
      init : function(args) {
          _args = args;
          // some other initialising
      },
      helloWorld : function() {
          alert('Hello World!');
      },

      createVisualization: function() {
        var scores = [20, 30, 40, 50, 60, 70, 80, 90, 20, 30, 40, 50, 60,];

        var w = 960,
          h = 600;


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
          .attr("cy", 100)
          .attr("r", function(d) {
            return d;
          })
          .attr("fill", function(d) {
            return "rgb(0, 0, " + (d * 5) + ")";
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
