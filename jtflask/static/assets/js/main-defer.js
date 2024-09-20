/*global vendors*/
// noinspection JSCheckFunctionSignatures

JTSplashPage.hideSplash();

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
  container: "digital-twin-container", // main div element for digital twin
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

const tileLayer = new vendors.ImageryTileLayer({
  url: demImageServer,
});
const graphicsLayer = new vendors.GraphicsLayer({
  elevationInfo: {
    mode: "relative-to-ground",
  },
});

function queryBuildings(geometry) {
  let query = sceneLayer.createQuery();
  query.geometry = geometry;
  query.spatialRelationship = "intersects";
  query.returnGeometry = true;
  query.outFields = ["*"];

  sceneLayer.queryFeatures(query).then(function (results) {
    const buildings = results.features.map((feature) => feature.attributes);
    sendSelectionToDash(buildings);
  });
}
let arcgisToolInstance = null;

function initializeArcGISTool() {
  // move sketch or reload sketch
  console.log("initializeSketchTool statement");
  const sketch = JTSketchWidget.createSketch(
    graphicsLayer,
    view,
    "arcgis-sketch-container"
  );
  JTSketchWidget.setupSketchEventListeners(sketch, tileLayer);
  sketch.on("create", function (event) {
    if (event.state === "complete") {
      const geometry = event.graphic.geometry;
      queryBuildings(geometry);
    }
  });

  const event = new CustomEvent("arcgis-tool-initialized");
  document.dispatchEvent(event);
}

arcgisToolInstance = initializeArcGISTool();

function sendSelectionToDash(buildings) {
  fetch("/jtdash/selection", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      buildings: buildings,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

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
view.ui.add(locateWidget, "bottom-right");

//Move zoom, navigation, and compass to the bottom right
view.ui.move(["zoom", "navigation-toggle", "compass"], "bottom-right");

//Add Fullscreen widget
const fullscreenWidget = new vendors.Fullscreen({
  view: view,
});

view.ui.add(fullscreenWidget, "bottom-right");

//Add basemap toggle widget
let basemapToggle = new vendors.BasemapToggle({
  view: view, // The view that provides access to the map's "streets-vector" basemap
  nextBasemap: "hybrid", // Allows for toggling to the "hybrid" basemap
});
view.ui.add(basemapToggle, "bottom-right");

// We render the basemap gallery into the container we created for it
const baseMapGalleryContainer = document.querySelector(
  "#basemap-gallery-card-content"
);
const basemapGallery = new vendors.BasemapGallery({
  view: view,
  container: baseMapGalleryContainer,
});

view.ui.add(basemapGallery);

// Move the container into the basemap card
document
  .querySelector("#basemap-gallery-card")
  .appendChild(baseMapGalleryContainer);


const calciteIcon = document.createElement("calcite-icon");
calciteIcon.setAttribute('icon', 'monitor')
calciteIcon.setAttribute('scale', 's')

const calciteButton = document.createElement("calcite-button");

calciteButton.addEventListener('click', () => {
  const appshell = document.querySelector('.mantine-AppShell-root')
  const currentIcon = calciteIcon.getAttribute('icon')
  if(currentIcon === 'monitor'){
    calciteIcon.setAttribute('icon', 'full-screen-exit')
    appshell.classList.add('hidden')
  }
  else {
    calciteIcon.setAttribute('icon', 'monitor')
    appshell.classList.remove('hidden')
  }
});
calciteButton.appendChild(calciteIcon);

const calciteDiv = document.createElement("div");
calciteDiv.classList.add('esri-component', 'hide-interface', 'esri-widget')
calciteDiv.appendChild(calciteButton)

const bottomRightContainer = document.querySelector(".esri-ui-bottom-right");
bottomRightContainer.prepend(calciteDiv);

map.add(sceneLayer);
// map.add(tileLayer);
map.add(graphicsLayer);

const setElementId = (element, id) => {
  if (element) {
    element.id = id;
  }
};

view.when(() => {
  view.map.basemap.referenceLayers.forEach((layer) => {
    if (layer.title === "Buildings") {
      layer.visible = false;
    }
  });
  let query = sceneLayer.createQuery();
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
  setElementId(
    document.querySelector(
      ".esri-component.esri-navigation-toggle.esri-widget"
    ),
    "customNavigationToggle"
  );
});

view.whenLayerView(sceneLayer).then((layerView) => {
  const selectionSketch = JTSelectionSketch.initWidget(
    layerView,
    "selection-widget-container"
  );
  view.ui.add(selectionSketch, "top-right");
});
