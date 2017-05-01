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

// $(document).ready(function(){     
    // namespace = '/tweets';
    // var socket = io.connect('//' + document.domain + ':' + location.port + namespace);
    // socket.on('connect', function(){
    //     console.log('user connected on client side');
    // })

    // //on receiving tweet 
    // socket.on('tweet', function(msg) {
    //     var date = msg.created_at;
    //     var text = msg.text;
    //     console.log(msg)
    //     console.log(msg.retweeted_status.place.full_name)
    //     console.log(msg.retweeted_status.place.bounding_box.coordinates)
    //     }
        
    //     //prepend tweet to tweetArea
    //     $('<div><a href="https://twitter.com/' + msg.user.screen_name + '" target="_blank"><img id="profimg" src="' + msg.user.profile_image_url_https + '"</a><div>' + msg.user.name + '<a href="https://twitter.com/' + msg.user.screen_name + '" target="_blank"> @' + msg.user.screen_name + '</a></div><div id="text"> ' + text + '</div><br><div id="date">' + date.substring(0,date.length-14) + '</div></div>').hide().prependTo('#tweetArea').fadeIn('slow');    
    //     $('#tweetArea').linkify({
    //       target: "_blank"    
    //     });
// });
