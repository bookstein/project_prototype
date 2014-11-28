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

    var JSONdata = {"name": "friends", "children": [{"score": 1.0, "size": 100, "name": "maddow"}, {"score": 0.7, "size": 100, "name": "barackobama"}, {"score": 0.5, "size": 150, "name": "rushlimbaugh"}]}

    var margin = {top: 20, right: 20, bottom: 20, left: 20}

    var diameter = $("#viz").width() - margin.right - margin.left,
    format = d3.format(",d");
    // color = d3.scale.category20c();

    var bubble = d3.layout.pack()
        .sort( function(a, b) {
        return -(a.value - b.value);
        })
        .size([diameter, diameter])
        .padding(1.5);

    var svg = d3.select("#viz").append("svg")
        .attr("width", diameter)
        .attr("height", diameter)
        .attr("class", "bubble");


    var root = JSONdata;

    var node = svg.selectAll(".node")
      .data(bubble.nodes(classes(root))
      .filter(function(d) { return !d.children; }))
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

      // node.append("title")
      //     .text(function(d) { return d.className + ": " + format(d.value); });

      node.append("circle")
          .attr("r", function(d) { return d.r; })
          .attr("fill", function(d) {
            return "rgba(0, 0, 255, " + d.score + ")";
          });;

      node.append("text")
        .attr("dy", ".3em")
        .style("text-anchor", "middle")
        .text(function(d) { return d.className.substring(0, d.r / 3);
        });




      // Returns a flattened hierarchy containing all leaf nodes under the root.
      function classes(root) {
        console.log("classes function running");
        var classes = [];

        function recurse(name, node) {
          if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
          else classes.push({packageName: name, className: node.name, value: node.size, score: node.score});
        }

        recurse(null, root);

        console.log({children: classes})
        return {children: classes};
      }

      d3.select(self.frameElement).style("height", diameter + "px");

      // circles.on("mouseover", function(d){

      //             d3.select(this)
      //               .attr("fill", "orange");
      //           })
      //           .on("mouseout", function(d) {
      //             d3.select(this)
      //               .attr("fill", "rgba(0, 0, 255, " + d.score + ")");
      //           })
      //           .on("click", function(d) {
      //             $("#detail ul").empty();
      //             var details = [d.screen_name, d.score, d.followers];
      //             console.log(details);

      //             for (var i = 0; i < details.length; i++) {
      //               console.log("FOR LOOP!");
      //               $("#detail ul").append("<li>" + details[i] + "</li>");
      //             }

      //             showTweets(d.screen_name);

      //           });

    }
  }
})();



