$(document).ready(function(){
  // ---INITALIZE MAP---
  var map; //make map global variable
  function init_map(){
    //create map on center of US
    var minZoomLevel =4
    var var_location = new google.maps.LatLng(39, -95)
    var mapOptions = {
      center: var_location,
      zoom: minZoomLevel
    };

    map = new google.maps.Map(document.getElementById("map-container"), mapOptions);    
  }

  google.maps.event.addDomListener(window, 'load', init_map);
  //---START SOCKETIO---
  namespace = '/tweets';
  var socket = io.connect('//' + document.domain + ':' + location.port + namespace);
  socket.on('connect', function(){
      console.log('user connected on client side');
  })

  //---RECEIVE & HANDLE TWEET---
  socket.on('tweet', function(msg) {

    //--DATE--
    var date = msg.created_at;
    var ndate = new Date(date);
    date = ndate.toString().substring(0,date.length-9);

    //--TWEET--
    var text;
    if (msg.hasOwnProperty('extended_tweet')){ //if tweet gets cut off get specific text 
      text = msg.extended_tweet.full_text;} 
      else if (msg.hasOwnProperty('retweeted_status')){ //if it is a retweet
      try{
        text='RT @' + msg.retweeted_status.user.screen_name + ': ' + msg.retweeted_status.extended_tweet.full_text;}
      catch(err){
        text='RT @' + msg.retweeted_status.user.screen_name + ': ' + msg.retweeted_status.text; }  } 
      else {
        text = msg.text;  }
    
   //--LOCATION COORDINATES--
    var coordinates = [];
    var location;
    if (msg.place != null){
      location = msg.place.full_name
      // console.log(location)
      var tmp = msg.place.bounding_box.coordinates[0][0]
      coordinates = tmp.reverse()   //if place exists
      }
      else if (msg.quoted_status != undefined) {
        if (msg.quoted_status.place != null){
          location = msg.quoted_status.place.full_name
          var tmp = msg.quoted_status.place.bounding_box.coordinates[0][0]
          coordinates = tmp.reverse()
        } //if quoted status place exists
      }
      else if (msg.retweeted_status != undefined) {
        if (msg.retweeted_status.place != null){
          location = msg.retweeted_status.place.full_name
          var tmp = msg.retweeted_status.place.bounding_box.coordinates[0][0]
          coordinates = tmp.reverse()
        } //if quoted status place exists
      }
    var glocation = new google.maps.LatLng(coordinates[0], coordinates[1])   
    // put a marker in the location
    // console.log(coordinates)
    var marker = new google.maps.Marker({position: glocation, map: map,title:location });
    marker.setMap(map);
    
    //--TWEET HTML FORMAT
    var tweetformat = '<div id="iWindow"><a href="https://twitter.com/' + msg.user.screen_name + '" target="_blank"><img id="profimg" src="' + msg.user.profile_image_url_https + '"</a><div>' + msg.user.name + '<a href="https://twitter.com/' + msg.user.screen_name + '" target="_blank"> @' + msg.user.screen_name + '</a></div><div id="text"> ' + text + '</div><br><div id="date">' + date + '</div></div>'
    $('#iWindow').linkify({
      target: "_blank"    
    });

    //-- ADD TWEET TO INFO WINDOW
    var infoWindowOptions = {
      content: tweetformat,
      maxWidth: 250
    }         
    var infoWindow = new google.maps.InfoWindow(infoWindowOptions);
    google.maps.event.addListener(marker, 'click', function(e){
      infoWindow.open(map,marker);
    })    

    //--ADD TWEET TO FEED
    $(tweetformat).hide().prependTo('#tweetArea').fadeIn('slow');    
    $('#tweetArea').linkify({
      target: "_blank"    
    });
 });

}); //end of on document start
 
