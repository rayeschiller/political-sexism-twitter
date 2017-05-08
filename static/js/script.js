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

    // put a marker in the location
    // var marker = new google.maps.Marker({
    //   position: var_location,
    //   map: map,
    //   title:"USA"
    // });
    // marker.setMap(map);
    
  }

  google.maps.event.addDomListener(window, 'load', init_map);
  //---START SOCKETIO---
    // start up the SocketIO connection the server
    namespace = '/tweets';
    var socket = io.connect('//' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function(){
        // socket.send('user has connected!');
        console.log('user connected on client side');
    })

  //---RECEIVE TWEET---
    socket.on('tweet', function(msg) {
      //Get Location coordinates
      var coordinates = []
      try{
        var location = msg.place.full_name
        console.log(location)
        var tmp = msg.place.bounding_box.coordinates[0][0]
        coordinates = tmp.reverse()  
        
      }
      catch(err){//do nothing
      }
      var date = msg.created_at;
      var ndate = new Date(date);
      date = ndate.toString().substring(0,date.length-9);
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
      
      var glocation = new google.maps.LatLng(coordinates[0], coordinates[1])   
      // put a marker in the location
      console.log(coordinates)
      var marker = new google.maps.Marker({position: glocation, map: map,title:"tweet"  });
      marker.setMap(map);
      
      var tweetformat = '<div id="iWindow"><a href="https://twitter.com/' + msg.user.screen_name + '" target="_blank"><img id="profimg" src="' + msg.user.profile_image_url_https + '"</a><div>' + msg.user.name + '<a href="https://twitter.com/' + msg.user.screen_name + '" target="_blank"> @' + msg.user.screen_name + '</a></div><div id="text"> ' + text + '</div><br><div id="date">' + date + '</div></div>'
      $('#iWindow').linkify({
        target: "_blank"    
      });
      //add tweet to map infoWindow
      var infoWindowOptions = {
        content: tweetformat,
        maxWidth: 250
      }         
      var infoWindow = new google.maps.InfoWindow(infoWindowOptions);
      google.maps.event.addListener(marker, 'click', function(e){
        infoWindow.open(map,marker);
      })    

      //prepend tweet to tweetArea
      $(tweetformat).hide().prependTo('#tweetArea').fadeIn('slow');    
      
      $('#tweetArea').linkify({
        target: "_blank"    
      });
 });

}); //end of on document start
 
