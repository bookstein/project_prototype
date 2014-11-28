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
    .append("g");

var titles = vis.append("title")
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return d.y; })
    .text(function(d) { return d.name +
        (d.children ? "" : ": " + format(d.value)); });

var circles = vis.append("circle")
    .attr("stroke", "black")
    .style("fill", function(d) { return !d.children ? "tan" : "beige"; })
    .attr("cx", function(d) { console.log(d.x); return d.x; })
    .attr("cy", function(d) { console.log(d.y); return d.y; })
    .attr("r", function(d) { console.log(d.r); return d.r; });

//updateVis();



function getData() {
return {"name": "friends", "children": [{"score": 1.0, "followers": 100, "screen_name": "maddow"}, {"score": 0.7, "followers": 100, "screen_name": "barackobama"}, {"score": 0.5, "followers": 150, "screen_name": "rushlimbaugh"}]};

      }
  }
}
}());
