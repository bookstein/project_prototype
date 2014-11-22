<!DOCTYPE html>
    <head>
        <title>Twitter Test</title>
        <meta charset="UTF-8">
        <link rel="stylesheet" type="text/css" href="static/bootstrap/css/bootstrap-theme.min.css">

     <style>

        .chart div {
          font: 10px sans-serif;
          background-color: steelblue;
          text-align: right;
          padding: 3px;
          margin: 1px;
          color: white;
        }

        </style>
    </head>
    <body>
        <div class="chart">
        </div>

        <script>
        var data = [4, 8, 15, 16, 23, 42];

        d3.select(".chart")
          .selectAll("div")
            .data(data)
          .enter().append("div")
            .style("width", function(d) { return d * 10 + "px"; })
            .text(function(d) { return d; });

        </script>
    </body>
</html>