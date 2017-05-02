'''map'''
function init_map() {
  var minZoomLevel = 4
  var var_location = new google.maps.LatLng(37.09024, -95.712891);
  var mapOptions = {
    center: var_location,
    zoom: minZoomLevel
  };

  // put a marker in the location
  var marker = new google.maps.Marker({
    position: var_location,
    map: map,
    title:"USA"
  });

  var map = new google.maps.Map(document.getElementById("map-container"), mapOptions);
  marker.setMap(map); 
  }
google.maps.event.addDomListener(window, 'load', init_map);

'''SocketIO'''
// start up the SocketIO connection the server
  namespace = '/tweets';
  var socket = io.connect('//' + document.domain + ':' + location.port + namespace);
  socket.on('connect', function(){
      console.log('user connected on map client side');
  })
  // socket.on('tweet', function(msg) {
  //   console.log(msg)
  // }
