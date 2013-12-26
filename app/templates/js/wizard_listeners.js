/*
 * Wizard Phase One
 * This is where we set up the dialog
 * involved in gathering the name of the
 * new network.
 */
$( "#new-network-one" ).dialog(
{
  autoOpen: false,
  width: 400,
  buttons:
  [{
    text: "Cancel",
    click: function() 
    {
      $(this).dialog("close");
    }
   },
   {
     text: "Next",
     click: function() 
     {
       /*
        * Enter Phase Two:
        */
        addPolyMode();
        var data = 
        {   
          "name": $("#network-name-input").val(), 
          "type_val": "UNKNOWN", 
          "phase_type_val": "FUN" 
        };

        data=JSON.stringify(data);
      
        /* send add_network ajax to add network name */
	ajax_req(
	  '/ajax/add_network',
	  data,
          function(data)
          {
	    network_id = data; // Cringeworthy I know x_x....
	    $("#new-network-one").dialog("close");
	    $("#new-network-two").dialog("open");
          });
      }
    
    }],
});

$("#new-network-two").dialog(
{
  autoOpen: false,
  width: 400,
  buttons:
  [{
    text: "Cancel",
    click: function()
    {
      $(this).dialog("close");
    }
   },
   {
     text: "Clear",
     click: function()
     {
       clearAddPoly();
     }
   },
   {
     text: "Next",
     click: function()
     {
       
       var data = 
       {
         "data": $("#polygon-json-output").val(),
         "network_id": network_id.toString()
       };
       
       data = JSON.stringify(data);

       ajax_req(
         '/ajax/add_polygon',
	 data,
         function(data)
         {
	   console.log("add_polygon: " + data);
	   $("#new-network-two").dialog("close");
           window.location.replace("/build");
         });
     }
    }]
});
