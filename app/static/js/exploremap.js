window.onload=init();
//console.log("init runs");
var map, Street, Terrain, Satellite, renderer, nodeLayer, addpolyLayer, polygonLayer, from, to, formats, select, connectionStyle, connectionLayer;

function init() 
{
  map = new OpenLayers.Map('map-container', 
  {
    controls: 
    [
      new OpenLayers.Control.Navigation(),
      new OpenLayers.Control.PanZoomBar(),
    ],
    numZoomLevels: 20,
    projection: "EPSG:900913"
  });

  map.displayProjection = new OpenLayers.Projection("EPSG:4326");
  from = new OpenLayers.Projection("EPSG:4326");
  to = new OpenLayers.Projection("EPSG:900913");

  var nodest = 
  {
    'pointRadius': 2,
    'fillColor': '#00000'
  };

  connectionStyle = {
	  strokeColor: '#0000ff',
	  strokeOpacity: 0.5,
	  strokeWidth: 5
  };


  var nodesty = OpenLayers.Util.applyDefaults(nodest,
                OpenLayers.Feature.Vector.style["defaults"]);

  var nodestyle = new OpenLayers.StyleMap({'default': nodest});

  map.addLayer(Street = new OpenLayers.Layer.XYZ("Street",
  [
    "http://otile4.mqcdn.com/tiles/1.0.0/map/${z}/${x}/${y}.png",
    "http://otile4.mqcdn.com/tiles/1.0.0/map/${z}/${x}/${y}.png",
    "http://otile4.mqcdn.com/tiles/1.0.0/map/${z}/${x}/${y}.png",
    "http://otile4.mqcdn.com/tiles/1.0.0/map/${z}/${x}/${y}.png"
  ],
  {
    attribution: "CC BY SA OSM Contributors",
                 transitionEffect: "resize"
  }));



  map.addLayer(Terrain = new OpenLayers.Layer.XYZ("terrain",
  [
    "http://a.tile.stamen.com/terrain/${z}/${x}/${y}.jpg",
    "http://b.tile.stamen.com/terrain/${z}/${x}/${y}.jpg",
    "http://c.tile.stamen.com/terrain/${z}/${x}/${y}.jpg",
    "http://d.tile.stamen.com/terrain/${z}/${x}/${y}.jpg"
  ],
  {
    attribution: "CC BY SA Stamen/OSM",
    transitionEffect: "resize"
  }));
  Terrain.setName('Terrain');

 
  map.addLayer(Satellite = new OpenLayers.Layer.XYZ("Imagery",
  [
    "http://otile1.mqcdn.com/tiles/1.0.0/sat/${z}/${x}/${y}.png",
    "http://otile2.mqcdn.com/tiles/1.0.0/sat/${z}/${x}/${y}.png",
    "http://otile3.mqcdn.com/tiles/1.0.0/sat/${z}/${x}/${y}.png",
    "http://otile4.mqcdn.com/tiles/1.0.0/sat/${z}/${x}/${y}.png"
  ],
  {
    attribution: "CC BY SA OSM Contributors",
    transitionEffect: "resize"
  }));

  map.addLayer(nodeLayer= new OpenLayers.Layer.Vector("Nodes",
  {
    //style: OpenLayers.Feature.Vector.style["default"]
    style: nodest
  }, 
  {
    renderers: renderer
  }));

  map.addLayer(addNodeLayer= new OpenLayers.Layer.Vector("AddNodes",
  {
    style: OpenLayers.Feature.Vector.style["default"]
  }, 
  {
    renderers: renderer
  }));


  map.addLayer(polygonLayer = new OpenLayers.Layer.Vector("Polygon"));

  map.addLayer(addpolyLayer = new OpenLayers.Layer.Vector("AddPolygon"));

  map.addLayer(connectionLayer = new OpenLayers.Layer.Vector("Connections"));

  center = new OpenLayers.LonLat(-93,43);
  center.transform(from,to);
      2
  map.setCenter(center, 4);

  var geolocate = new OpenLayers.Control.Geolocate(
  {
    bind: false,
    geolocationOptions: 
    {
      enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 7000
    }
  }); 
  var baseLayerOptions = 
  {
    displayInLayerSwitcher: false
  };

  controls = 
  {
    /* This was commented out so that the layer switcher in map does not
     * render. This allows me to implement it as a div outside the map
     * which had the styling changed to blend in.
     */
    //switcher: new OpenLayers.Control.LayerSwitcher({'ascending':true}),
    locator: geolocate,
    polygon: new OpenLayers.Control.DrawFeature(addpolyLayer, OpenLayers.Handler.Polygon),
    node: new OpenLayers.Control.DrawFeature(addNodeLayer, OpenLayers.Handler.Point)
  }
      
  for(var key in controls) 
  {
    map.addControl(controls[key]);
  }
            
  var firstGeolocation = true;
  map.addControl(new OpenLayers.Control.LayerSwitcher(
  {
    'div':OpenLayers.Util.getElement('layerswitcher')
  }));

  var options = 
  {
    hover: true,
    onSelect: serialize
  };

  select = new OpenLayers.Control.SelectFeature(addpolyLayer, options);
  map.addControl(select);
  select.activate();


  var in_options = 
  {
    'internalProjection': map.baseLayer.projection,
    'externalProjection': new OpenLayers.Projection("ESPG:4326")
  };

  var out_options = 
  {
    'internalProjection': map.baseLayer.projection,
    'externalProjection': new OpenLayers.Projection("ESPG:4326")
  };

  formats = 
  {
    'in': 
    {
      geojson: new OpenLayers.Format.GeoJSON(in_options)
    },
    'out': 
    {
      geojson: new OpenLayers.Format.GeoJSON(out_options)
    }
  };

  addNodeLayer.events.register("featureadded", addNodeLayer, function(f) 
  {
    var coords = 
    {
      x: f.feature.geometry.x,
      y: f.feature.geometry.y
    };
    document.getElementById('node-lat').value = coords['x'];
    document.getElementById('node-lon').value = coords['y'];

    viewMode();

  });
  
  geolocate.events.register("locationupdated",geolocate, function(e) 
  {
    //console.log("x:" + e.point.x);
    //console.log("y:" + e.point.y);
    center = new OpenLayers.LonLat(e.point.x, e.point.y);
    map.setCenter(center, 10);
  });
  
  map.addControl(new OpenLayers.Control.MousePosition());

  add_overlays();
}


function toggleControl(toggle_key) 
{
  for(key in controls) 
  {
    var control = controls[key];
    if(toggle_key == key) 
    {
      control.activate();
    } 
    else 
    {
      control.deactivate();
    }
  }
}

function serialize(feature)
{
  var str = formats['out']['geojson'].write(feature, false);
  //alert(str);
  document.getElementById('polygon-json-output').value = str;
}

function clearAddPoly()
{
  addpolyLayer.removeAllFeatures();
}

function addPolyMode()
{
  select.activate();
  toggleControl("polygon");
}

function addNodeMode()
{
  toggleControl("node");
}

function viewMode()
{
  select.deactivate();
  toggleControl("geolocate");
}

function addPolygon(source_json)
{
  polygonLayer.addFeatures(formats['in']['geojson'].read(source_json));
}

function addPoint(lat, lon)
{
  //console.log("adding point");
  //console.log(lat);
  //console.log(lon);
  var point = new OpenLayers.Geometry.Point(lat,lon);
  var pointFeature = new OpenLayers.Feature.Vector(point);
  nodeLayer.addFeatures([pointFeature]);
}

function addConnection(dev_a, dev_b)
{
  var points = new Array(
    new OpenLayers.Geometry.Point(dev_a[0], dev_a[1]),
    new OpenLayers.Geometry.Point(dev_b[0], dev_b[1]));

  var line = new OpenLayers.Geometry.LineString(points);
  var feature = new OpenLayers.Feature.Vector(line, null,connectionStyle);

  connectionLayer.addFeatures([feature]);
}
