	var map = null;
    var boxpolys = null;
    var directions = null;
    var routeBoxer = null;
    var distance = null; // km
    
    initialize = function () {
      // Default the map view to the continental U.S.
      var mapOptions = {
        center: new google.maps.LatLng(37.09024, -95.712891),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        zoom: 4
      };
      
      map = new google.maps.Map(document.getElementById("map"), mapOptions);
      routeBoxer = new RouteBoxer();
      
      directionService = new google.maps.DirectionsService();
      directionsRenderer = new google.maps.DirectionsRenderer({ map: map });      
    }
    
    function route() {
      // Clear any previous route boxes from the map
      clearBoxes();
      
      // Convert the distance to box around the route from miles to km
      distance = parseFloat(document.getElementById("distance").value) * 1.609344;
      
      var request = {
        origin: document.getElementById("from").value,
        destination: document.getElementById("to").value,
        travelMode: google.maps.DirectionsTravelMode.DRIVING
      }
      
      // Make the directions request
      directionService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsRenderer.setDirections(result);
          
          // Box around the overview path of the first route
          var path = result.routes[0].overview_path;
          var boxes = routeBoxer.box(path, distance);
          drawBoxes(boxes);
        } else {
          alert("Directions query failed: " + status);
        }
      });
    }
    
    // Draw the array of boxes as polylines on the map
    function drawBoxes(boxes) {
      boxpolys = new Array(boxes.length);
      for (var i = 0; i < boxes.length; i++) {
        boxpolys[i] = new google.maps.Rectangle({
          bounds: boxes[i],
          fillOpacity: 0,
          strokeOpacity: 1.0,
          strokeColor: '#000000',
          strokeWeight: 1,
          map: map
        });
      }
    }
    
    // Clear boxes currently on the map
    function clearBoxes() {
      if (boxpolys != null) {
        for (var i = 0; i < boxpolys.length; i++) {
          boxpolys[i].setMap(null);
        }
      }
      boxpolys = null;
    }
$(document).ready(function(){
	$('.checkbox').live('click', function(){
		$(this).removeClass('checkbox').addClass('checked');
	});
	$('.checked').live('click', function(){
		$(this).removeClass('checked').addClass('checkbox');
	});
	initialize();
	
});