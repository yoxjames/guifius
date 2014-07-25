/* Draw default explore nodes */
var wiz_phase = 0;
  
/* Bottom Panel show/hide */
$(".toggle-bpanel").click(function()
{
  $(".bpanel").toggle();
});

/* 
 * Use hidden togglespace 
 */
$("#toggle-bpanel-off").click(function()
{
  $("#toggle-bpanel-off").hide();
  $("#toggle-bpanel-on").show();
});

/* 
 * Use showing togglespace 
 */
$("#toggle-bpanel-on").click(function()
{
  $("#toggle-bpanel-off").show();
  $("#toggle-bpanel-on").hide();
});

/* 
 * New Network Popup, should use jQuery UI dialogs.
 */
$("#new-network-button").click(function(event)
{
  $("#new-network-one").dialog("open");
  event.preventDefault();
  wiz_phase=1;
});

/*
 * New node button pushed.
 * Calls addNodeMode() which sets the map to node dropping mode
 * also hides the bpanel
 */
$("#new-node-button").click(function()
{
  addNodeMode();
  $("#node-name").val("");
  node_insert = 1;
  //$("new-node-popup").show();
  //$(".bpanel").hide();
  //$(".toggle-bpanel").hide();
});

var curNet = [];

  var type_selected = "UNKNOWN";
  var current_polarization = "UNKNOWN";
  var connection_mode = 0;
  var a_device;

/*
 * jQuery UI setup
 */
$("#new-network-button").button();

$("#network-buttonset").buttonset();
$("#node-buttonset").buttonset();
$("#commit-node").button();

  $("#redrop-node-button").attr("disabled","disabled");
  $("#connect-node-button").attr("disabled","disabled");

  $("#redrop-node-button").click(function()
  {
    addNodeMode();
  });

  $("#connect-node-button").click(function()
  {
    connection_mode = 1; // Somebody smack me for this... 
    a_device = current_device;
  });
  
  code_cache = {{ code_cache |safe }}; 
  console.log(JSON.stringify(code_cache));
  console.log({{ current_network | safe}});

  cnt = {{ networks|safe }}
  for (n in cnt)
  {
    name=(cnt[n]['name']);
    id=(cnt[n]['id']);
    $("#network-select").append("<option id='"+n+"'>"+name+"</option>");
  }

  $("#network-type").on('click','option', function()
  {
    type_selected = $(this).attr('code-val');
  });

  $("#network-phase-type").on('click','option', function()
  {
    phase_type_val = $(this).attr('code-val');
  });

  $("#polarization-type").on('click','option', function()
  {
    current_polarization = $(this).attr('code-val');
  });


  $("#commit-network").click(function()
  {  
    var req =
    {
      network_id: curNet['id'],
      name: $("#network-name").val(),
      type_val: type_selected,
      phase_type_val: phase_type_val
    };

    req=JSON.stringify(req);

    $.ajax(
    {
      type: 'POST',
      contentType: "application/json; charset=utf-8",
      url: '/ajax/commit_network',
      data: req,
      success: function(data)
      {
        alert("Network Updated"); // CHANGE THIS
      },
      dataType: "json"
    });
  });



  $("#network-select").on('click','option', function()
  {
    $("#network-type").empty(); // Prevent Duplicates
    $("#network-phase-type").empty(); // Prevent Duplicates
    curNet = cnt[parseInt($(this).attr('id'))];

    console.log(curNet);
    $("#network-name").val(curNet['name']);

    $("#network-type").append(
	    "<option id='network-current-type'>"
	    +code_cache['NET_TYPE'][curNet['type_val']]
	    +"</option>");
    $.each(code_cache['NET_TYPE'], function(value,desc)
    {
      //console.log(value);
      if (desc!= $("#network-current-type").val())
        $("#network-type").append(
		"<option code-val='"+value+"'>"+desc+"</option>");
    });


    $("#network-phase-type").append(
	    "<option id='cur-net-phase-type'>"
	    +code_cache['NET_PHASE_TYPE'][curNet['phase_type_val']]
	    +"</option>");

    cur_net_phase_type = $("#cur-net-phase-type").val();
    phase_type_val = cur_net_phase_type;

    $.each(code_cache['NET_PHASE_TYPE'], function(value,desc)
    {
      //console.log(value);
      if (desc != $("#cur-net-phase-type").val())
        $("#network-phase-type").append(
		"<option code-val='"+value+"'>"+desc+"</option>");
    });




    var req =
    {
      network_id: curNet['id']
    };

    req = JSON.stringify(req);

    $("#node-select").empty();
    $("#node-select").append("<option>Select Node</option>");


    $.ajax(
    {
      type: 'POST',
      contentType: "application/json; charset=utf-8",
      url: '/ajax/get_devices_for_network',
      data: req,
      success: function(data)
      {
        $.each(data, function(index, value)
        {
          $("#node-select").append("<option id='"+value['id']+"'>"+value['name']+"</option>");
        });
      },
      dataType: "json"
    });
  });

  $("#commit-node").click(function()
  {
    newnode = "FALSE";
    if (node_insert)
      newnode = "TRUE";

    var req = 
    {
      "new": newnode, 
      lat: $("#node-lat").val(),
      lon: $("#node-lon").val(),
      name: $("#node-name").val(),
      type_val: type_selected, // Fix
      polarization_type_val: current_polarization,
      azimuth: $("#azimuth-input").val(),
      elevation: $("#elevation-input").val(),
      status_type_val: "ONLINE", //FIX
      network_id: curNet['id'],
      device_id: current_device
    };

    req = JSON.stringify(req);

    $.ajax(
    {
      type: 'POST',
      contentType: "application/json; charset=utf-8",
      url: '/ajax/add_device',
      data: req,
      success: function(data)
      {
        alert("COMMITTED");
      },
      dataType: "json"
    });

    node_insert = 0;
  });

  $("#node-select").on('click', 'option', function()
  {
    current_device = parseInt($(this).attr('id'));

    my_node_types = code_cache['NODE_TYPE']
    
    $("#node-type").empty();
    $("#node-type").append(
	    "<option id='node-current-type'>Node Type</option>");

    $("#polarization-type").empty();
    $("#polarization-type").append(
		    "<option id='current-polarization-type'>Polarization Type</option>");

    




    $("#redrop-node-button").removeAttr("disabled");
    $("#connect-node-button").removeAttr("disabled");
    
    req = 
    {
      device_id: parseInt($(this).attr('id'))
    };

    req=JSON.stringify(req);
    
    $.ajax(
    {
      type: 'POST',
      contentType: "application/json; charset=utf-8",
      url: '/ajax/get_device_info',
      data: req,
      success: function(data)
      {
        $("#node-lat").val(data['lat']);
	$("#node-lon").val(data['lon']);
	$("#node-name").val(data['name']);
	$("#node-current-type").text(code_cache['NODE_TYPE'][data['type_val']]);
	$("#node-current-type").val(data['type_val']);
	$("#current-polarization-type").text(code_cache['POLARIZATION_TYPE'][data['polarization_type_val']]);
	$("#current-polarization-type").val(data['polarization_type_val']);
        current_polarization = data['polarization_type_val'];
	$("#azimuth-input").val(data['azimuth']);
	$("#elevation-input").val(data['elevation']);

        $.each(my_node_types, function(value,desc)
        {
          if (value != $("#node-current-type").val())
          $("#node-type").append(
		"<option code-val="+value+">"+desc+"</option>");
        });

        $.each(code_cache['POLARIZATION_TYPE'], function(value,desc)
        {
          if (value != $("#current-polarization-type").val())
          $("#polarization-type").append(
		"<option code-val="+value+">"+desc+"</option>");
        });


      },
      dataType: "json"
    });

    if (connection_mode)
    {
      req =
      {
        device_a_id: a_device,
	device_b_id: current_device,
	type_val: "UNKNOWN",
	active: 1,
	bandwidth: 0
      };

      req = JSON.stringify(req);

      $.ajax(
      {
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        url: '/ajax/connect_devices',
        data: req,
        success: function(data) 
	  {
            alert("success");
	    connection_mode = 0;
	    a_device = 0;
	  },
        dataType: "json"
      });

    } 
  });

