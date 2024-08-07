// import { Map } from "./vendors.min.js";
// import {SceneView} from "./vendors.min.js";
// import SceneView from "@arcgis/core/views/SceneView";
// require('../../../jtdash/assets/js/vendors.min.js');

// const Map = require("./vendors.min.js").Map;

// import {SolidEdges3D} from "../../src";

const BLKGRP = 'https://taurus.at.geoplan.ufl.edu/arcgis/rest/services/fgdl/USCB/Mapserver/10/' +
    'query?where=COUNTY=31&outFields=TOTALPOP,GEOID20&f=geojson';


const BLDG_JAX_DT = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/PLW_Jacksonville_BLD_Merge_Join_for_web/SceneServer/layers/0";

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

// /**********************************************
//  * Graphics layer to sketch on
//  *********************************************/
// // The layer where the graphics are sketched
// const sketchLayer = new vendors.GraphicsLayer({
//   elevationInfo: {
//     mode: "absolute-height"
//   },
//   title: "Sketched geometries"
// });
//
// const map = new vendors.Map({
//     basemap: "satellite",
//     layers: [
//         sketchLayer,
//         sceneLayer
//     ],
//     ground: "world-elevation"
// });
//


const view = new vendors.SceneView({
    container: "deckgl-container", // Reference to the scene div created in step 5
    map: map, // Reference to the map object created before the scene
    camera: { // Sets the initial camera position
        position: [-81.66916428, 30.29352027, 2569],
        heading: 13.89,
        tilt: 51
    }
});

let basemapToggle = new vendors.BasemapToggle({
  view: view,  // The view that provides access to the map's "streets-vector" basemap
  nextBasemap: "hybrid"  // Allows for toggling to the "hybrid" basemap
});

 /**********************************************
 * Symbologies
 *********************************************/
// Polygon symbol used for sketching the extruded building footprints
// const buildingSymbology = new vendors.PolygonSymbol3D({
//   symbolLayers: [
//     new ExtrudeSymbol3DLayer({
//       size: 3.5, // extrude by 3.5m meters
//       material: {
//         color: [255, 255, 255, 0.8]
//       },
//       edges: new SolidEdges3D({
//         size: 1,
//         color: [82, 82, 122, 1]
//       })
//     })
//   ]
// });

 const sketchViewModel = new vendors.SketchViewModel({
          layer: sketchLayer,
          view: view,
              polygonSymbol: {
                type: "simple-fill",
                style: "cross",
                color: "#EFC8B1",
                outline: {
                  width: 3,
                  style: "solid",
                  color: "#514644"
                }
              },
          snappingOptions: {
            enabled: true,
            featureSources: [
              {
                layer: sketchLayer
              }
            ]
          },
          // Show absolute direction value in tooltips
          valueOptions: {
            directionMode: "absolute"
          },
          tooltipOptions: {
            enabled: true
          },
          labelOptions: {
            enabled: true
          },
          defaultUpdateOptions: {
            tool: "reshape",
            reshapeOptions: {
              edgeOperation: "offset"
            }
          }
        });

    const sketch = new vendors.Sketch({
      layer: sketchLayer,
      view: view,
        viewModel: sketchViewModel,
      // graphic will be selected as soon as it is created
      creationMode: "update"
    });

    view.ui.add(sketch, "bottom-right");
        // // Create the Sketch widget and add it to the "sketchWidget" container inside the "sketchPanel" <div>
        // const sketch = new vendors.Sketch({
        //   view,
        //   viewModel: sketchViewModel,
        //   // Remove some buttons from the widget
        //   visibleElements: {
        //     createTools: {
        //       rectangle: false,
        //       circle: false
        //     }
        //   },
        //   container: "sketchWidget"
        // });


let locateWidget = new vendors.Locate({
  view: view,   // Attaches the Locate button to the view
  graphic: new vendors.Graphic({
    symbol: { type: "simple-marker" }  // overwrites the default symbol used for the
    // graphic placed at the location of the user when found
  })
});

 // Add the container for the widget and custom buttons to the view
// view.ui.add("sketchWidget", "top-right");
view.ui.add(locateWidget, "bottom-right")
view.ui.move([ "zoom",  "navigation-toggle", "compass", ], "bottom-right")
view.ui.add([  basemapToggle, "attribution" ], "bottom-right")
