<!DOCTYPE html>



<html lang="en">

<head>
	<title>EleNa</title>

	<style type="text/css">
		.marker_start {
	  background-image: url('/static/marker-black.png');
	  background-size: cover;
	  width: 30px;
	  height: 30px;
	  border-radius: 50%;
	  cursor: pointer;
	}
	.marker_end {
	  background-image: url('/static/marker-red.png');
	  background-size: cover;
	  width: 30px;
	  height: 30px;
	  border-radius: 50%;
	  cursor: pointer;
	}

	</style>

 	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

	<!-- Flatly theme -->
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/flatly/bootstrap.min.css">

	<!-- Latest compiled and minified JQuery -->
	<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>

	<!-- Latest compiled and minified Popper.js -->
	<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>

	<!-- Latest compiled and minified Bootstrap -->
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

	<!-- MapBox -->
	<script src="https://api.mapbox.com/mapbox-gl-js/v1.9.1/mapbox-gl.js"></script>
	<link href="https://api.mapbox.com/mapbox-gl-js/v1.9.1/mapbox-gl.css" rel="stylesheet" />

</head>

<body>

	<div class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a href="../" class="navbar-brand">EleNa: Elevation-based Navigation - CRAGS</a>    
       </div>
    </div>

    <div class="container" style="margin-top: 40px;">

    	<div class="page-header" id="banner">
    	    <div class="row">
    	      <div class="col-lg-12 col-md-7 col-sm-6">
    	        <h3>About</h3>
    	        <p class="lead">A software system that determines, given a start and an end location, a route that maximizes or minimizes elevation gain, while limiting the total distance between the two locations to x% of the shortest path.</p>
    	      </div>
    	    </div>
    	</div>

	    <div class="bs-docs-section" style="margin-top: 30px;">
	        <div class="row">
	          <div class="col-lg-12">
	            <div class="page-header">
	              <h3 id="forms">Navigation</h3>
	            </div>
	          </div>
	        </div>

	        <div class="row">
		        <div class="col-lg-3">
		            <div class="bs-component">
		            	<p><img src="/static/marker-black.png" height="15" width="15"> - Start marker <br><img src="/static/marker-red.png" height="15" width="15"> - Destination marker </p>
						<form action="/" method="post">
						  <div class="form-group">
						    <label for="startPoint">Start Point</label>
						    <input type="text" name="startPoint" class="form-control" id="startPoint" value="42.394, -72.597">
						  </div>
						  <div class="form-group">
						    <label for="destinationPoint">Destination Point</label>
						    <input type="text" name="destinationPoint" class="form-control" id="destinationPoint" value=" 42.394, -72.47">
						  </div>
						  <div class="form-group">
						    <label for="elevType">Type of Elevation Gain</label>
						    <select class="form-control" name="elevType" id="elevType">
						    % if 'elevType' in data:
						      <option ${'selected' if data['elevType'] == 'Maximize' else ''}>Maximize</option>
						      <option ${'selected' if data['elevType'] == 'Minimize' else ''}>Minimize</option>
						    % else:
						      <option>Maximize</option>
						      <option>Minimize</option>	
						    % endif
						    </select>
						  </div>
						  <div class="form-group">
						    <label for="distanceLimit">Distance limit %</label>
						    % if 'distanceLimit' in data:
						    <input type="number" name="distanceLimit" class="form-control" id="distanceLimit" value="${data['distanceLimit']}">
						    % else:
						    <input type="number" name="distanceLimit" class="form-control" id="distanceLimit" value="10">
						    % endif
						  </div>
						  <div class="form-group">
						    <label for="algoType">Algorithm</label>
						    <select class="form-control" name="algoType" id="algoType">
						    % if 'algoType' in data:
						      <option ${'selected' if data['algoType'][0] == 'D' else ''}>Djikstras Shortest Path</option>
						      <option ${'selected' if data['algoType'][0] == 'Y' else ''}>Yens elevation path</option>	
						      <option ${'selected' if data['algoType'][0] == 'A' else ''}>A* elevation path</option>
						    % else:
						      <option>Djikstras Shortest Path</option>
						      <option>Yens elevation path</option>	
						      <option>A* elevation path</option>
						    % endif
						    </select>	
						  </div>
						  <button type="submit" class="btn btn-info">Submit</button>
						</form>
					</div>
				</div>
				<div class="col-lg-8 offset-lg-1">
		            <div class="bs-component">
		            	<div id="map" style="width: 100%; height: 450px; position: absolute;"></div>
		            </div>
		        </div>
	    	</div>
	    	 <div class="row">
    	      <div class="col-lg-4 offset-lg-4">
    	        <h5>Data:</h5>
    	        <p>
    	        	% if 'route_shortest' in data:
    	        	<svg width="20" height="20">
    	        		<rect width="20" height="20" style="fill:#03a5fc;stroke-width:3;stroke:rgb(0,0,0)" />
					</svg> - Djikstras shortest Path <br>
					Total Elevation = ${"%.2f" % data['shortest_elevation']} feet <br>
					Total Distance = ${"%.2f" % data['shortest_distance']}
					% elif 'route_yens' in data:
					<svg width="20" height="20">
    	        		<rect width="20" height="20" style="fill:#42f58a;stroke-width:3;stroke:rgb(0,0,0)" />
					</svg> - Yens elevation path <br>
					Total Elevation = ${"%.2f" % data['yens_elevation']} feet <br>
					Total Distance = ${"%.2f" % data['yens_distance']}
					% elif 'route_astar' in data:
					<svg width="20" height="20">
    	        		<rect width="20" height="20" style="fill:#fcbe03;stroke-width:3;stroke:rgb(0,0,0)" />
					</svg> - A* elevation path <br>
					Total Elevation = ${"%.2f" % data['astar_elevation']} feet <br>
					Total Distance = ${"%.2f" % data['astar_distance']} 
					% endif
				</p>
    	     </div>
    	    </div>
	    </div>
	</div>
		
</body>
<script>
	var bounds = [
		[-72.8034, 42.2823], // SW 
		[-72.2745, 42.5140]//NE
	]

	var api_key = "${data['MAP_API_KEY']}";
	mapboxgl.accessToken = api_key;
	var map = new mapboxgl.Map({
		container: 'map', // container id
		style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
		center: [-72.537, 42.394], // starting position [lng, lat]
		zoom: 10, // starting zoom
		maxBounds: bounds // Sets bounds as max
	});

	% if 'route_shortest' in data:
		var route = ${data['route_shortest']}
		map.on('load', function() {
			map.addSource('route', {
				'type': 'geojson',
				'data': {
					'type': 'Feature',
					'properties': {},
					'geometry': {
						'type': 'LineString',
						'coordinates': route
					}
				}
			});
			map.addLayer({
				'id': 'route',
				'type': 'line',
				'source': 'route',
				'layout': {
					'line-join': 'round',
					'line-cap': 'round'
				},
				'paint': {
					'line-color': '#03a5fc',
					'line-width': 4
				}
			});
		});
	% endif

	% if 'route_yens' in data:
		var route_yens = ${data['route_yens']}
		map.on('load', function() {
			map.addSource('route_yens', {
				'type': 'geojson',
				'data': {
					'type': 'Feature',
					'properties': {},
					'geometry': {
						'type': 'LineString',
						'coordinates': route_yens
					}
				}
			});
			map.addLayer({
				'id': 'route_yens',
				'type': 'line',
				'source': 'route_yens',
				'layout': {
					'line-join': 'round',
					'line-cap': 'round'
				},
				'paint': {
					'line-color': '#42f58a',
					'line-width': 4
				}
			});
		});
	% endif

	% if 'route_astar' in data:
		var route_astar = ${data['route_astar']}
		map.on('load', function() {
			map.addSource('route_astar', {
				'type': 'geojson',
				'data': {
					'type': 'Feature',
					'properties': {},
					'geometry': {
						'type': 'LineString',
						'coordinates': route_astar
					}
				}
			});
			map.addLayer({
				'id': 'route_astar',
				'type': 'line',
				'source': 'route_astar',
				'layout': {
					'line-join': 'round',
					'line-cap': 'round'
				},
				'paint': {
					'line-color': '#fcbe03',
					'line-width': 4
				}
			});
		});
	% endif

	// Add zoom and rotation controls to the map.
	map.addControl(new mapboxgl.NavigationControl());

	// create a HTML element for each feature
	var el_start = document.createElement('div');
	el_start.className = 'marker_start';

	// create a HTML element for each feature
	var el_end = document.createElement('div');
	el_end.className = 'marker_end';

	// make a marker for each feature and add to the map
	

	% if 'route_shortest' in data:
		var sp = ${data['route_shortest'][0]};
		var start_marker = new mapboxgl.Marker(el_start)
		  .setLngLat(sp)
		  .addTo(map)
		  .setDraggable(true);

		$("#startPoint").val(sp[1].toFixed(4)+", "+sp[0].toFixed(4));

		// make a marker for each feature and add to the map
		var ep = ${data['route_shortest'][-1]};
		var finish_marker = new mapboxgl.Marker(el_end)
		  .setLngLat(ep)
		  .addTo(map)
		  .setDraggable(true);
		$("#destinationPoint").val(ep[1].toFixed(4)+", "+ep[0].toFixed(4));

	% elif 'route_yens' in data:
		var sp = ${data['route_yens'][0]};
		var start_marker = new mapboxgl.Marker(el_start)
		  .setLngLat(sp)
		  .addTo(map)
		  .setDraggable(true);

		$("#startPoint").val(sp[1].toFixed(4)+", "+sp[0].toFixed(4));

		// make a marker for each feature and add to the map
		var ep = ${data['route_yens'][-1]};
		var finish_marker = new mapboxgl.Marker(el_end)
		  .setLngLat(ep)
		  .addTo(map)
		  .setDraggable(true);
		$("#destinationPoint").val(ep[1].toFixed(4)+", "+ep[0].toFixed(4));

	% elif 'route_astar' in data:
		var sp = ${data['route_astar'][0]};
		var start_marker = new mapboxgl.Marker(el_start)
		  .setLngLat(sp)
		  .addTo(map)
		  .setDraggable(true);

		$("#startPoint").val(sp[1].toFixed(4)+", "+sp[0].toFixed(4));

		// make a marker for each feature and add to the map
		var ep = ${data['route_astar'][-1]};
		var finish_marker = new mapboxgl.Marker(el_end)
		  .setLngLat(ep)
		  .addTo(map)
		  .setDraggable(true);
		$("#destinationPoint").val(ep[1].toFixed(4)+", "+ep[0].toFixed(4));


	% else:
		var start_marker = new mapboxgl.Marker(el_start)
		  .setLngLat([-72.597, 42.394])
		  .addTo(map)
		  .setDraggable(true);	

		// make a marker for each feature and add to the map
		var finish_marker = new mapboxgl.Marker(el_end)
		  .setLngLat([-72.47, 42.394])
		  .addTo(map)
		  .setDraggable(true);

	% endif

	/*map.on('click', function(e) {
		alert(JSON.stringify(e.lngLat.wrap()));
	});*/
	function startOnDragEnd() {
		var lngLat = start_marker.getLngLat();
		var point = $('#startPoint');
		point.val(lngLat.lat.toFixed(4)+", "+lngLat.lng.toFixed(4));
	}
	function finishOnDragEnd() {
		var lngLat = finish_marker.getLngLat();
		var point = $('#destinationPoint');
		point.val(lngLat.lat.toFixed(4)+", "+lngLat.lng.toFixed(4));
	}
	 
	start_marker.on('dragend', startOnDragEnd);
	finish_marker.on('dragend', finishOnDragEnd);


</script>

</html>
