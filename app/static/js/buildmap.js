          window.onload=init();
          console.log("init runs"); 

	   var map, Street, Terrain, Satellite, renderer, Vector1, from, to;
           function init() {

	      console.log("init ran");
              map = new OpenLayers.Map('map-container', {
                  controls: [
                    new OpenLayers.Control.Navigation(),
                    new OpenLayers.Control.PanZoomBar(),
                  ],
                  numZoomLevels: 19,
                  projection: "EPSG:900913"
                  });

              map.displayProjection = new OpenLayers.Projection("EPSG:4326");
              from = new OpenLayers.Projection("EPSG:4326");
              to = new OpenLayers.Projection("EPSG:900913");

              var fn8 = {
                  'pointRadius': 1,
                  'fillColor': '#ffffff'};
              var fn10 = {
                  'pointRadius': 2,
                  'fillColor': '#ffffff'};

              var fn8sty = OpenLayers.Util.applyDefaults(fn8sty,
                  OpenLayers.Feature.Vector.style["defaults"]);
              var fn10sty = OpenLayers.Util.applyDefaults(fn10sty,
                  OpenLayers.Feature.Vector.style["defaults"]);

              var fn8style = new OpenLayers.StyleMap({'pointRadius': 1,
                  'fillColor': '#ffffff'});
              var fn10style = new OpenLayers.StyleMap({'pointRadius': 2,
                  'fillColor': '#ffffff'});




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

              map.addLayer(Vector1 = new OpenLayers.Layer.Vector("FN-B8",
                    {styleMap: fn8style}, {
                              renderers: renderer
                          }));
              Vector1.displayInLayerSwitcher = false;


              var geofield = " , , , ";
	      //var geofield = document.getElementById("edit-submitted-geofield").value;             
              if (geofield == " , , , "){
                center = new OpenLayers.LonLat(-90,39);
                center.transform(from,to);
                map.setCenter(center, 4);
              }
              else{
                var georeq = OpenLayers.Request.GET({
                  url: "http://nominatim.openstreetmap.org/search/" 
                        + encodeURI(geofield) + "?format=xml&polygon=0&addressdetails=0",
                  callback: geohandler});
              } 

              controls = {
                switcher: new OpenLayers.Control.LayerSwitcher({'ascending':false}),
                addNode: new OpenLayers.Control.DrawFeature(Vector1,
                         OpenLayers.Handler.Point,
                         {'featureAdded': nodeadded})
              }

              erps = {
                FNR10 : 7,
                FNR13 : 8,
                FNR10T : 9,
                FNR13T : 10
              }
 
              for(var key in controls) {
                map.addControl(controls[key]);
              }

              function nodeadded(feature){
                var xval = feature.geometry.x;
                var yval = feature.geometry.y;
                list = document.getElementById("controlList");
                selected = list.options[list.selectedIndex].text;
                var erp = erps[selected];
                var muxer = new OpenLayers.LonLat(xval,yval);
                muxer.transform(to,from);
                var request = OpenLayers.Request.GET({
                    url:
                    encodeURI("/rf.php?x="+muxer.lon.toString()+
                                            "&y="+muxer.lat.toString()+
                                                "&erp="+erp.toString()),
                    callback: rfhandler
                    });
              }

            }


          function overlayer(path){
            var layer = new OpenLayers.Layer.Vector("RF",{
              renderers: location.search.indexOf('Canvas') >= 0 ?
                           ['Canvas', 'SVG', 'VML'] : ['SVG', 'VML', 'Canvas'],
              projection: map.displayProjection,
              strategies: [new OpenLayers.Strategy.Fixed()],
              displayInLayerSwitcher: false,
              styleMap: new OpenLayers.StyleMap({'pointRadius': 0}),
              protocol: new OpenLayers.Protocol.HTTP({
                url: path,
                format: new OpenLayers.Format.KML({
                  maxDepth: 1,
                  baseURL: path,
                  extractStyles: false,
                  extractAttributes: false,
                })
              })
            })
          return layer;
          };

          function rfhandler(request) {
            var path = request.responseXML.firstChild.firstChild.nodeValue;
            var layer = overlayer(path);
            map.addLayer(layer);
            };

          function geohandler(request) {
            var newcenter = new OpenLayers.LonLat(request.responseXML.documentElement.firstElementChild.attributes[4].value, request.responseXML.documentElement.firstElementChild.attributes[3].value);
            newcenter.transform(from, to);
            map.setCenter(newcenter,10);

          }

          function switchControl(){
              list = document.getElementById("controlList");
              selected = list.options[list.selectedIndex].text;
              if(selected == "Navigate"){
                  controls.addNode.deactivate();
                  } else {
                  controls.addNode.activate();
                  }
          }
