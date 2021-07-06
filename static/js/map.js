function d3map() {
  var svg = d3.select("#map").append("svg");
  svg.attr("width", 630).attr("height", 550);
  var width = svg.attr("width");
  var height = svg.attr("height");
  svg
    .append("rect")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("fill", "white");

  var projection = d3
    .geoMercator()
    .scale(width * 90)
    .center([-87.6298, 41.8781])
    .translate([width / 2, height / 2.5]);

  d3.queue()
    .defer(d3.json, "/static/data/Boundaries.geojson")
    .await(function (error, datageo) {
      if (error) {
        console.error("Error: " + error);
      } else {
        drawMap(datageo);
      }
    });

  d3.queue()
    .defer(d3.json, "/api/coords/crime_type")
    .await(function (error, points) {
      if (error) {
        console.error("Error: " + error);
      } else {
        plot_points(points);
      }
    });
  var path = d3.geoPath(projection);

  function plot_points(points) {
    var circles = svg
      .selectAll("circle")
      .data(points["ARSON"])
      .enter()
      .append("circle")
      .attr("cx", function (d) {
          /* console.log('x = '+d[0]+'y = '+d[1]) */
          /* console.log(projection([d[0], d[1]])) */
        /* console.log(projection([d[0], d[1]])[0]); */
        return projection([d[0], d[1]])[0];
      })
      .attr("cy", function (d) {
        /* console.log(projection([d[0], d[1]])[1]); */
        return projection([d[0], d[1]])[1];
      })
      .attr("r", 2)
      .style("fill", "green");
  }

  function drawMap(datageo) {
    var enterNodes = svg
      .append("g")
      .selectAll("path")
      .data(datageo.features)
      .enter()
      .append("path")
      .attr("fill", "blue")
      .attr("d", (d) => {
        return path(d);
      })
      .style("stroke", "white")
      .style("stroke-width", 1.2)
      .on("mouseover", function (d) {
        /* console.log(d); */
        d3.select(this).style("cursor", "pointer").attr("fill", "red");
      })
      .on("mouseout", function (d) {
        d3.select(this).attr("fill", "blue");
      })
      .on("click", function (d) {
        d3.select("p").text(
          "Ward " + d.properties.ward + ": " + d.properties.shape_area
        );
      });
  }
}
