// import { Map } from "./vendors.min.js";
// import {SceneView} from "./vendors.min.js";
// import SceneView from "@arcgis/core/views/SceneView";
// require('../../../jtdash/assets/js/vendors.min.js');

// const Map = require("./vendors.min.js").Map;

const BLKGRP = 'https://taurus.at.geoplan.ufl.edu/arcgis/rest/services/fgdl/USCB/Mapserver/10/' +
    'query?where=COUNTY=31&outFields=TOTALPOP,GEOID20&f=geojson';

// const BLDG_JAX_DT = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/ArcGIS/rest/services/" +
//     "PLW_Jacksonville_BLD_2018/SceneServer/layers/0";

const BLDG_JAX_DT = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/PLW_Jacksonville_BLD_Merge_Join_for_web/SceneServer/layers/0";

//
// const layer = new vendors.DeckLayer({
//     'deck.layers': [
//         new vendors.GeoJsonLayer({
//             id: "block-group-layer",
//             data: BLKGRP,
//             opacity: 0.2,
//             stroked: true,
//             filled: true,
//             extruded: true,
//             wireframe: false,
//             fp64: true,
//             getElevation: f => Math.sqrt(f.properties.TOTALPOP) * 100,
//             getFillColor: f => [255, 255, 255, 255], // colorScale(f.properties.TOTALPOP),
//             getLineColor: f => [0, 0, 0],
//             getLineWidth: 2,
//             pickable: true,
//             // onDataLoad: () => {
//             //     deckgl.setProps({
//             //         viewState: newViewState
//             //     });
//             // }
//             onClick: ({layer, object}) => {
//                 const {viewport} = layer.context;
//                 const [xmin, ymin, xmax, ymax] = turf.bbox(object);
//                 const {longitude, latitude, zoom} = viewport.fitBounds(
//                     [[xmin, ymin], [xmax, ymax]],
//                     {
//                         width: 400,
//                         height: 400
//                     }
//                 );
//                 deckgl.setProps({
//                     viewState: {
//                         longitude,
//                         latitude,
//                         zoom: zoom-1,
//                         pitch: 45,
//                         transitionInterpolator: new deck.FlyToInterpolator(),
//                         transitionDuration: "auto"
//                     }
//                 });
//                 // console.log('Clicked:', object);
//                 // document.getElementById("GEOID20").attributes[1].value = object.properties.GEOID20;
//                 // console.log(document.getElementById("deckgl-container"));
//                 document.getElementById("deckgl-container").setAttribute("data-geoid20", object.properties.GEOID20);
//                 // document.getElementById("means-to-work-title").innerHTML = object.properties.GEOID20;
//                 // console.log(document.getElementById("GEOID20").attributes[4].value);
//             }
//         })
//     ]
// });

// const AIR_PORTS =
//     'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_airports.geojson';
//
// const layer = new vendors.DeckLayer({
//     effect: 'bloom(1.5, 0.5px, 0.1)',
//     'deck.getTooltip': info => info.object && info.object.properties.name,
//     'deck.layers': [
//         new vendors.GeoJsonLayer({
//             id: 'airports',
//             data: AIR_PORTS,
//             // Styles
//             filled: true,
//             pointRadiusMinPixels: 2,
//             pointRadiusScale: 2000,
//             getPointRadius: f => 11 - f.properties.scalerank,
//             getFillColor: [200, 0, 80, 180],
//             // Interactive props
//             pickable: true,
//             autoHighlight: true,
//             onClick: info =>
//                 info.object &&
//                 // eslint-disable-next-line
//                 alert(`${info.object.properties.name} (${info.object.properties.abbrev})`)
//         }),
//         new vendors.ArcLayer({
//             id: 'arcs',
//             data: AIR_PORTS,
//             dataTransform: d => d.features.filter(f => f.properties.scalerank < 4),
//             // Styles
//             getSourcePosition: f => [-0.4531566, 51.4709959], // London
//             getTargetPosition: f => f.geometry.coordinates,
//             getSourceColor: [0, 128, 200],
//             getTargetColor: [200, 0, 80],
//             getWidth: 1
//         })
//     ]
// });

// vendors.loadArcGISModules(['esri/Map', 'esri/views/MapView'], {version: '4.21'})
//     .then(({DeckLayer, modules}) => {
//         const [Map, MapView] = modules;
//
//         const layer = new DeckLayer({
//             'deck.layers': [
//                 new vendors.ScatterplotLayer({
//                     data: [
//                         {position: [0.119, 52.205]}
//                     ],
//                     getPosition: d => d.position,
//                     getColor: [255, 0, 0],
//                     radiusMinPixels: 20
//                 })
//             ]
//         });
//
//         const view = new MapView({
//             container: "deckgl-container",
//             map: new Map({
//                 basemap: "dark-gray-vector",
//                 layers: [layer]
//             }),
//             center: [0.119, 52.205],
//             zoom: 5
//         });
//     });

function getSymbol(color) {
    return {
        type: "polygon-3d", // autocasts as new PolygonSymbol3D()
        symbolLayers: [
            {
                type: "extrude", // autocasts as new ExtrudeSymbol3DLayer()
                material: {
                    color: color
                },
                edges: {
                    type: "solid",
                    color: "#999",
                    size: 0.5
                }
            }
        ]
    };
}

/*****************************************************************
 * Set each unique value directly in the renderer's constructor.
 * At least one field must be used (in this case the "DESCLU" field).
 * The label property of each unique value will be used to indicate
 * the field value and symbol in the legend.
 *
 * The size visual variable sets the height of each building as it
 * exists in the real world according to the "ELEVATION" field.
 *****************************************************************/

var renderer = {
    type: "unique-value", // autocasts as new UniqueValueRenderer()
    defaultSymbol: getSymbol([255, 255, 200, 0.5]),
    defaultLabel: "Other",
    field: "TOTALPOP",
    // uniqueValueInfos: [
    //     {
    //         value: "Residential",
    //         symbol: getSymbol("#A7C636"),
    //         label: "Residential"
    //     },
    //     {
    //         value: "Commercial",
    //         symbol: getSymbol("#FC921F"),
    //         label: "Commercial"
    //     },
    //     {
    //         value: "Hotel/Motel",
    //         symbol: getSymbol("#ED5151"),
    //         label: "Hotel/Motel"
    //     },
    //     {
    //         value: "Apartment Rentals",
    //         symbol: getSymbol("#149ECE"),
    //         label: "Apartment Rentals"
    //     }
    // ],
    visualVariables: [
        {
            type: "size",
            field: "TOTALPOP"
        }
    ]
};

// Set the renderer on the layer
const buildingsLayer = new vendors.GeoJSONLayer({
    url: BLKGRP,
    renderer: renderer,
    elevationInfo: {
        mode: "on-the-ground"
    },
    title: "Extruded building footprints",
    // popupTemplate: {
    //     // autocasts as new PopupTemplate()
    //     title: "{TYPE}",
    //     content: [
    //         {
    //             type: "fields",
    //             fieldInfos: [
    //                 {
    //                     fieldName: "TYPE",
    //                     label: "Type"
    //                 },
    //                 {
    //                     fieldName: "HEIGHT",
    //                     label: "Height"
    //                 }
    //             ]
    //         }
    //     ]
    // },
    outFields: ["GEOID20", "TOTALPOP"]
});

let sceneLayer = new vendors.SceneLayer({
    url: BLDG_JAX_DT,
    renderer: {
        type: "simple",
        symbol: {
            type: "mesh-3d",
            symbolLayers: [
                {
                    type: "fill",
                    material: {
                        color: [255, 255, 255],
                        colorMixMode: "replace"
                    },
                    edges: {
                        type: "solid",
                        color: [0, 0, 0, 1],
                        size: 0.5
                    }
                }
            ]
        }
    }

});

const map = new vendors.Map({
    basemap: "satellite",
    layers: [
        // buildingsLayer,
        sceneLayer
    ],
    ground: "world-elevation"
});

const view = new vendors.SceneView({
    container: "deckgl-container", // Reference to the scene div created in step 5
    map: map, // Reference to the map object created before the scene
    camera: { // Sets the initial camera position
        // position: {
        //     spatialReference: {
        //         latestWkid: 3857,
        //         wkid: 102100
        //     },
        //     x: -11262192.883555487,
        //     y: 2315246.351026253,
        //     z: 18161244.728082635
        // },
        // heading: 0,
        // tilt: 0.49
        position: [-81.66916428, 30.29352027, 2569],
        heading: 13.89,
        tilt: 51
    }
});

// let zoom = new vendors.Zoom({
//   view: view
// });

let basemapToggle = new vendors.BasemapToggle({
  view: view,  // The view that provides access to the map's "streets-vector" basemap
  nextBasemap: "hybrid"  // Allows for toggling to the "hybrid" basemap
});
//
// let compass = new vendors.Compass({
//   view: view
// });

// let navigationToggle = new vendors.NavigationToggle({
//   view: view
// });

let locateWidget = new vendors.Locate({
  view: view,   // Attaches the Locate button to the view
  graphic: new vendors.Graphic({
    symbol: { type: "simple-marker" }  // overwrites the default symbol used for the
    // graphic placed at the location of the user when found
  })
});

// add home button - zoom back to JaxTwin extent
// add full screen button
//     minimize sidebar



view.ui.move([ "zoom", "compass",  "navigation-toggle"  ], "top-right")
view.ui.add([  basemapToggle, "attribution" ], "bottom-right")
view.ui.add(locateWidget, "top-right")


// const renderer = new vendors.DeckRenderer(view, {
//     layers: [
//         new vendors.ScatterplotLayer({
//             data: [
//                 {position: [0.119, 52.205]}
//             ],
//             getPosition: d => d.position,
//             getColor: [255, 0, 0],
//             radiusMinPixels: 20
//         })
//     ]
// });
//
// vendors.externalRenderers.add(view, renderer);

// const view = new vendors.MapView({
//     container: "deckgl-container", // Reference to the scene div created in step 5
//     map: map, // Reference to the map object created before the scene
//     center: [0.119167, 52.205276],
//     zoom: 5,
// });

// var link = document.createElement('link');
// link.rel = 'stylesheet';
// link.href = 'https://js.arcgis.com/4.29/esri/themes/light/main.css';
// document.head.appendChild(link);