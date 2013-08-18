         window.onload=init();
          console.log("init runs");
           var map, Street, Terrain, Satellite, renderer, Vector1, Vector2,
from, to;
           function init() {
              
              
              map = new OpenLayers.Map('map-container', {
                  controls: [
                    new OpenLayers.Control.Navigation(),
                    new OpenLayers.Control.PanZoomBar(),
                  ],
                  numZoomLevels: 20,
                  projection: "EPSG:900913"
                  });

              map.displayProjection = new OpenLayers.Projection("EPSG:4326");
              from = new OpenLayers.Projection("EPSG:4326");
              to = new OpenLayers.Projection("EPSG:900913");

              var nodest = {
                  'pointRadius': 10,
                  'fillColor': '#ffffff'};

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

              map.addLayer(Vector1 = new OpenLayers.Layer.Vector("nodes",
                    {style: OpenLayers.Feature.Vector.style["default"]}, {
                              renderers: renderer
                          }));
              Vector1.displayInLayerSwitcher = false;

              center = new OpenLayers.LonLat(-93,43);
              center.transform(from,to);
         
              map.setCenter(center, 4);

             var geolocate = new OpenLayers.Control.Geolocate({
    		bind: false,
    		geolocationOptions: {
        		enableHighAccuracy: true,
        		maximumAge: 0,
        		timeout: 7000
    		}
             }); 
             var baseLayerOptions = {
               displayInLayerSwitcher: false
             };

              controls = {
                switcher: new OpenLayers.Control.LayerSwitcher({'ascending':true}),
		locator: geolocate,
		area: new OpenLayers.Control.DrawFeature(Vector1, OpenLayers.Handler.Polygon),
		node: new OpenLayers.Control.DrawFeature(Vector1, OpenLayers.Handler.Point)
              }
	      
              for(var key in controls) {
                map.addControl(controls[key]);
              }
              
	    var firstGeolocation = true;
map.addControl(new OpenLayers.Control.LayerSwitcher({'div':OpenLayers.Util.getElement('layerswitcher')}));
geolocate.events.register("locationupdated",geolocate,function(e) {
	console.log("x:" + e.point.x);
	console.log("y:" + e.point.y);
	center = new OpenLayers.LonLat(e.point.x, e.point.y);
	map.setCenter(center, 10);
});
}


function toggleControl(element) {
	for(key in controls) {
		var control = controls[key];
		if(element.value == key && element.checked) {
			control.activate();
		} else {
			control.deactivate();
		}
	}
}
            
