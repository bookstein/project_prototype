var VIZ = VIZ || (function () {

  function showTweets(screenName) {
    console.log("loading tweets");
    $("#tweets").empty()

    // embeds a timeline in #tweets div
      twttr.ready(
        function (twttr) {
          twttr.widgets.createTimeline(
            '538087329949548544',
            // $ returns jQuery obj, get first elem [0] in obj
            $('#tweets')[0],
            {
            tweetLimit: 3,
            screenName: screenName,
            showReplies: "false",
            })
            .then(function (el) {
              // success callback
                console.log("Embedded " +  screenName + " timeline.");
              },
              function(el) {
                // failure callback
                console.log("Failed to embed " + screenName + " timeline.");
            });
      });
  }

  return {
      test : function(scores_json) {
          console.log(scores_json);
      },

      createVisualization: function(scores) {
    var margin = {top: 20, right: 20, bottom: 20, left: 20}
    var diameter = $("#viz").width(),
    format = d3.format(",d"),
    dataSource = 0;

var pack = d3.layout.pack()
//default children accessor assumes each input data is an object with a children array
    .size([diameter - margin.top, diameter - margin.left])
    .sort( function(a, b) {
        return -(a.value - b.value);
    })
    .value(function(d) { return d.followers; });

var svg = d3.select("body").append("svg")
    .attr("width", diameter)
    .attr("height", diameter);

var data = getData();

var vis = svg.datum(data).selectAll(".node")
    .data(pack.nodes)
   .enter()
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var titles = vis.append("title")
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return d.y; })
    .text(function(d) { return d.name +
        (d.children ? "" : ": " + format(d.value)); });

var circles = vis.append("circle")
    .attr("stroke", "black")
    .style("fill", function(d) {
              return "rgba(0, 0, 255, " + d.score + ")"
          })
    .attr("cx", function(d) { console.log(d.x); return d.x; })
    .attr("cy", function(d) { console.log(d.y); return d.y; })
    .attr("r", function(d) { console.log(d.r); return d.r; });

circles.on("mouseover", function(d){
            // console.log(d);

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
          })
          .on("click", function(d) {
            $("#detail ul").empty();
            var details = [d.screen_name, d.score, d.followers];
            console.log(details);

            for (var i = 0; i < details.length; i++) {
              console.log("FOR LOOP!");
              $("#detail ul").append("<li>" + details[i] + "</li>");
            }

            showTweets(d.screen_name);

          });



function getData() {
return {"name": "friends", "children": [{"score": 1.0, "followers": 100, "screen_name": "maddow"}, {"score": 0.7, "followers": 100, "screen_name": "barackobama"}, {"score": 0.5, "followers": 150, "screen_name": "rushlimbaugh"}]};

      }
  }
}
}());




        // // create SVG elem
        // var svg = d3.select("#viz")
        //             .append("svg")
        //             .attr("width", w + margin.left + margin.right)
        //             .attr("height", h + margin.top + margin.bottom)
        //           .append("g")
        //             .attr("transform", "translate(" + margin.left + "," + margin.top + ")");;


        // var max_followers = d3.max(scores, function(d) {
        //   // references "followers" property of each object in scores
        //   return d.followers
        // });

        // var rScale = d3.scale.linear()
        //               .domain([0, max_followers])
        //               .range([10, 60])


        // var circles = svg.selectAll("circle")
        //   .data(scores)
        //   .enter()
        //   .append("circle");


        // circles.attr("cx", function(d, i) {
        //     // assign a dynamic value that corresponds to i, or each value’s position in the data set
        //     console.log("CX " + ((i+1) * (w / scores.length)))
        //     return (i+1) * (w / scores.length);
        //   })
        //   .attr("cy", function(d) {
        //     console.log("CY " + (1 - d.score) * h)
        //     return (1 - d.score) * h;
        //   })
        //   .attr("r", function(d) {
        //     return rScale(d.followers);
        //   })
        //   .attr("stroke", "gray")
        //   .attr("fill", function(d) {
        //       return "rgba(0, 0, 255, " + d.score + ")"
        //   });

        // circles.on("mouseover", function(d){
        //     // console.log(d);

        //     var screenName = d.screen_name;
        //     var xPosition = parseFloat(d3.select(this).attr("cx"));
        //     var yPosition = parseFloat(d3.select(this).attr("cy")) - parseFloat(d3.select(this).attr("r") + 3);
        //     svg.append("text")
        //         .attr("id", "tooltip")
        //         .attr("x", xPosition)
        //         .attr("y", yPosition)
        //         .attr("text-anchor", "middle")
        //         .attr("font-family", "sans-serif")
        //         .attr("font-size", "11px")
        //         .attr("font-weight", "bold")
        //         .attr("fill", "black")
        //         .text(screenName);

        //     d3.select(this)
        //       .attr("fill", "orange");
        //   })
        //   .on("mouseout", function(d) {
        //     d3.select("#tooltip").remove();
        //     d3.select(this)
        //       .attr("fill", "rgba(0, 0, 255, " + d.score + ")");
        //   })
        //   .on("click", function(d) {
        //     $("#detail ul").empty();
        //     var details = [d.screen_name, d.score, d.followers];
        //     console.log(details);

        //     for (var i = 0; i < details.length; i++) {
        //       console.log("FOR LOOP!");
        //       $("#detail ul").append("<li>" + details[i] + "</li>");
        //     }

        //     showTweets(d.screen_name);

        //   });
