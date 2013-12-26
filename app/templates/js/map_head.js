<script src="{{ url_for('static', filename='js/exploremap.js')}}" defer="defer"></script>
<script src="{{ url_for('static', filename='js/CustomLayers-2.12/OpenLayers.js') }}"></script>


<!-- Non jQuery javascript. Used for behinds the scenes non visual
stuff
-->
<script type="text/javascript">
/* locate
 * Takes a string as input (hopefully an address)
 * and attemps to send that information to google
 * to recieve a json object in return that contains
 * location information. This function returns an array
 * of two elements [lat,lon] for latitude and longitude.
 */
function locate(addr)
{
  var trans_input;
  var loc_info;
  var lat,lon
  trans_input = addr.replace(/ /g,"+");
  loc_info = httpGet("http://maps.googleapis.com/maps/api/geocode/json?address=" + trans_input + "&sensor=true");
       
  eval("json_rep = "+loc_info);
  lat = json_rep.results[0].geometry.location.lat;
  lon = json_rep.results[0].geometry.location.lng;
  return [lon,lat];
}

/* httpGet
 * Helper function that sends out a GET request to a desired
 * URL. The responsetext from google is actually json despite
 * the xmlHttp stuff.
 */
function httpGet(theUrl)
{
    var xmlHttp = null;

    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function add_overlays()
{
  global_json = {{ map_data |safe }};

  $.each(global_json['online_networks'], function(index,network)
  {
    addPolygon(network['data']); // Draw Polygon layer
    $.each(network['devices'], function(index,device)
    {
      addPoint(device['device']['lat'], device['device']['lon']);
      $.each(device['connections'], function(index,connection)
      {
        addConnection(
	  [device['device']['lat'],device['device']['lon']],
	  [connection['lat'],connection['lon']]);
      });
    });
  });
}

</script>

