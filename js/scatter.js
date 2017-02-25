var margin = { top: 50, right: 300, bottom: 50, left: 50 },
    outerWidth = 1050,
    outerHeight = 500,
    width = outerWidth - margin.left - margin.right,
    height = outerHeight - margin.top - margin.bottom;

var x = d3.scale.linear()
    .range([0, width]).nice();

var y = d3.scale.linear()
    .range([height, 0]).nice();


d3.json("tsne.json", function(data) {
  $('#loading').hide();
  data.forEach(function(d) {
      d['x'] = d['tsne_coords'][0];
      d['y'] = d['tsne_coords'][1];
  });

  var xMax = d3.max(data, function(d) { return d.x; }) * 1.05,
      xMin = d3.min(data, function(d) { return d.x; }),
      xMin = xMin > 0 ? 0 : xMin,
      yMax = d3.max(data, function(d) { return d.y; }) * 1.05,
      yMin = d3.min(data, function(d) { return d.y; }),
      yMin = yMin > 0 ? 0 : yMin;

  x.domain([xMin, xMax]);
  y.domain([yMin, yMax]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickSize(-height);

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickSize(-width);

  var color = d3.scale.category10();

  var tip = d3.tip()
      .attr("class", "d3-tip")
      .offset([-10, 0])
      .html(function(d) {
        return '<i>"' + d['subject'] + '" (' + d['contact_num'] + ' people)</i>';
      });

  var zoomBeh = d3.behavior.zoom()
      .x(x)
      .y(y)
      .scaleExtent([0, 500])
      .on("zoom", zoom);

  var svg = d3.select("#scatter")
    .append("svg")
      .attr("width", outerWidth)
      .attr("height", outerHeight)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .call(zoomBeh);

  svg.call(tip);

  svg.append("rect")
      .attr("width", width)
      .attr("height", height);

  var objects = svg.append("svg")
      .classed("objects", true)
      .attr("width", width)
      .attr("height", height);

  objects.append("svg:line")
      .classed("axisLine hAxisLine", true)
      .attr("x1", 0)
      .attr("y1", 0)
      .attr("x2", width)
      .attr("y2", 0)
      .attr("transform", "translate(0," + height + ")");

  objects.append("svg:line")
      .classed("axisLine vAxisLine", true)
      .attr("x1", 0)
      .attr("y1", 0)
      .attr("x2", 0)
      .attr("y2", height);

  function tooltips(d, i){
      tip.show(d, i);
      $('#emailinfo').html(
        '<b>' + d['date'] + '</b><br>' + 
        '<b>from</b>: ' + d['from'] + '<br>' +
        '<b>to</b>: ' + d['to'] + '<br>' +
        '<b>cc</b>: ' + d['cc'] + '<br>' +
        '<b>Subject:</b> <i>"' + d['subject'] + '" (' + d['contact_num'] + ' people)</i><br>' + 
        '<pre>' + d['body'] + '</pre>'
      )
  }

  objects.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .classed("dot", true)
      //.attr("r", function (d) { return 6 * Math.sqrt(d[rCat] / Math.PI); })
      .attr("transform", transform)
      //.style("fill", function(d) { return color(d[colorCat]); })
      .on("mouseover", tooltips)
      .on("mouseout", tip.hide);

  d3.select("input").on("click", change);

  function change() {
    xMax = d3.max(data, function(d) { return d.x; });
    xMin = d3.min(data, function(d) { return d.x; });

    zoomBeh.x(x.domain([xMin, xMax])).y(y.domain([yMin, yMax]));

    var svg = d3.select("#scatter").transition();
    objects.selectAll(".dot").transition().duration(1000).attr("transform", transform);
  }

  function zoom() {
    svg.select(".x.axis").call(xAxis);
    svg.select(".y.axis").call(yAxis);

    svg.selectAll(".dot")
        .attr("transform", transform);
  }

  function transform(d) {
    return "translate(" + x(d.x) + "," + y(d.y) + ")";
  }
});
