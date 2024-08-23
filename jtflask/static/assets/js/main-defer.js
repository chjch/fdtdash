/*global vendors*/
// noinspection JSCheckFunctionSignatures

const { utils } = vendors;

// const BLDG_JAX_DT = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/" +
//     "PLW_Jacksonville_BLD_Merge_Join_for_web/SceneServer";

const BLDG_JAX_DT =
  "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/" +
  "PLW__JTAoi_Jax__WebLayer_AGOL/SceneServer";

const demImageServer =
  "https://tiledimageservices.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/" +
  "USGS_1M_DEM_50M_Resample/ImageServer";

const map = new vendors.Map({
  basemap: "navigation-dark-3d",
  ground: "world-elevation",
});

const view = new vendors.SceneView({
  container: "deckgl-container", // Reference to the scene div created in step 5
  map: map, // Reference to the map object created before the scene
  camera: {
    position: [-81.66916428, 30.29352027, 2569],
    heading: 13.89,
    tilt: 51,
  },
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
            color: [255, 255, 255, 0.7],
            colorMixMode: "replace",
          },
          edges: null,
        },
      ],
    },
  },
});
const tileLayer = new vendors.ImageryTileLayer({ url: demImageServer });
const graphicsLayer = new vendors.GraphicsLayer({
  elevationInfo: { mode: "relative-to-ground" },
});

// Create the Locate widget
const locateWidget = new vendors.Locate({
  view: view,
  graphic: new vendors.Graphic({
    symbol: {
      outline: {
        color: "white",
        width: 1, // points
      },
      color: "blue",
      size: "12px", // pixel
      style: "circle",
      type: "simple-marker",
    },
  }),
});

const sketch = JTSketchWidget.createSketch(graphicsLayer, view, "sketchWidget");
JTSketchWidget.setupSketchEventListeners(sketch, tileLayer);

let basemapToggle = new vendors.BasemapToggle({
  view: view, // The view that provides access to the map's "streets-vector" basemap
  nextBasemap: "hybrid", // Allows for toggling to the "hybrid" basemap
});

view.ui.move(["zoom", "compass", "navigation-toggle"], "top-right");
view.ui.add(sketch, "bottom-right");
view.ui.add(basemapToggle, "bottom-right");
view.ui.add(locateWidget, "top-right");

map.add(sceneLayer);
// map.add(tileLayer);
map.add(graphicsLayer);

const setElementId = (element, id) => {
  if (element) {
    element.id = id;
  }
};

view.when(() => {
  utils.hideSplashScreen();
  
  view.map.basemap.referenceLayers.forEach((layer) => {
    if (layer.title === "Buildings") {
      layer.visible = false;
    }
  });
  var query = sceneLayer.createQuery();
  query.returnGeometry = true;
  query.outFields = ["*"];

  // sceneLayer.queryFeatures(query).then(function(results) {
  //     let colorData = {};
  //     let identifyPromises = [];
  //
  //     results.features.forEach(feature => {
  //         let centroid = feature.geometry.centroid;
  //         let objectId = feature.attributes.OBJECTID_1;
  //         let identifyPromise = tileLayer.identify(centroid).then(function(results) {
  //             // feature.attributes.NPARNO = results.value[0];
  //             // let edits = {
  //             //     updateFeatures: [feature]
  //             // };
  //             colorData[objectId] = results.value[0];
  //             // console.log(feature.attributes.NPARNO);
  //             // console.log(feature.attributes.OBJECTID_1);
  //             // featureLayer.applyEdits(edits);
  //         });
  //         identifyPromises.push(identifyPromise);
  //     });
  //
  //     // Wait for all identify promises to complete
  //     Promise.all(identifyPromises).then(() => {
  //         let colorDataJson = JSON.stringify(colorData);
  //
  //         let arcadeExpression = `
  //             var colorData = Dictionary(${colorDataJson});
  //             // var colorData2 = Dictionary(extraInfo);
  //             return colorData[Text($feature.OBJECTID_1)];
  //             // if(HasValue(colorData2, ["251"])){
  //             //     // if() evaluates to true, thus executing the return
  //             //     return colorData2["1"];
  //             // }
  //         `;
  //
  //         // console.log(arcadeExpression);
  //
  //         sceneLayer.renderer = new vendors.SimpleRenderer({
  //             symbol: {
  //                 type: "mesh-3d", // autocasts as new MeshSymbol3D()
  //                 symbolLayers: [{
  //                     type: "fill", // autocasts as new FillSymbol3DLayer()
  //                     material: {
  //                         color: [255, 255, 0, 0.8],
  //                         colorMixMode: "replace"
  //                     },
  //                     edges: null
  //                 }]
  //             },
  //             visualVariables: [{
  //                 type: "color",
  //                 valueExpression: arcadeExpression,
  //                 stops: [
  //                     { value: -10, color: [0, 255, 0, 0.4] },
  //                     { value: 1, color: [0, 255, 0, 0.4] },
  //                     { value: 2, color: [255, 255, 0, 0.4] },
  //                     { value: 3, color: [255, 165, 0, 0.4] },
  //                     { value: 4, color: [255, 69, 0, 0.4] },
  //                     { value: 5, color: [255, 0, 0, 0.4] },
  //                     { value: 100, color: [255, 0, 0, 0.4] }
  //                 ]
  //             }]
  //         }); // Set the renderer on the layer
  //     });
  // });

  setElementId(
    document.querySelector(".esri-locate.esri-widget.esri-component"),
    "customLocateButton"
  );
  setElementId(
    document.querySelector(".esri-component.esri-zoom.esri-widget"),
    "customZoomButton"
  );
  setElementId(
    document.querySelector(".esri-ui-bottom-right.esri-ui-corner"),
    "uiCornerBottomRight"
  );
});
