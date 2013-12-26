/* 
 * Open the rpanel
 */
$(".toggle-rpanel").click(function(){
  $(".rpanel").toggle();
  $(".toggle-rpanel").toggle();
});

/* 
 * "Go button clicked. Try to locate address string 
 */ 
$("#addr-text-btn").click(function(){
  var coords = locate($('#addr-text-input').val());
  center = new OpenLayers.LonLat(coords[0],coords[1]);
  center.transform(from, to);
  map.setCenter(center, 16);
});

/* If a user presses return in the address field then
 * run the same code that would run when the "Go" 
 * button is pushed.
 */
$("#addr-text-input").bind('keypress', function(e){
  if(e.keyCode==13){
    var coords = locate($('#addr-text-input').val());
    center = new OpenLayers.LonLat(coords[0],coords[1]);
    center.transform(from, to);
    map.setCenter(center, 16);
  }
});

/* 
 * If IP Locate is clicked try to locate via IP 
 */
$("#addr-ip-btn").click(function(){
  controls.locator.deactivate();
  controls.locator.activate();
});


/* jQuery UI */
$( "#addr-ip-btn" ).button();
$( "#addr-text-btn" ).button();




