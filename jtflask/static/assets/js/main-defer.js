/*global vendors*/
// noinspection JSCheckFunctionSignatures

JTSplashPage.hideSplash();

// const BLDG_JAX_DT = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/" +
//     "PLW_Jacksonville_BLD_Merge_Join_for_web/SceneServer";

const BLDG_JAX_DT = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/" +
    "PLW__JTAoi_Jax__WebLayer_AGOL/SceneServer"

const demImageServer = "https://tiledimageservices.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/" +
    "USGS_1M_DEM_50M_Resample/ImageServer";

const map = new vendors.Map({
    basemap: "navigation-dark-3d",
    ground: "world-elevation"
});

const view = new vendors.SceneView({
    container: "digital-twin-container", // main div element for digital twin
    map: map, // Reference to the map object created before the scene
    camera: {
        position: [-81.66916428, 30.29352027, 2569],
        heading: 13.89,
        tilt: 51
    }
});

let sceneLayer = new vendors.SceneLayer({
    url: BLDG_JAX_DT,
    renderer: {
        type: "simple",
        symbol: {
            type: "mesh-3d",
            symbolLayers: [{
                type: "fill",
                material: {
                    color: [255, 255, 255, 0.7],
                    colorMixMode: "replace"
                },
                edges: null
            }]
        }
    },
});

const tileLayer = new vendors.ImageryTileLayer({
    url: demImageServer
});
const graphicsLayer = new vendors.GraphicsLayer({
    elevationInfo: {
        mode: "relative-to-ground"
    }
});

// Create the Locate widget
const locateWidget = new vendors.Locate({
    view: view,
    graphic: new vendors.Graphic({
        symbol: {
            outline: {
                color: "white",
                width: 1 // points
            },
            color: "blue",
            size: "12px", // pixel
            style: "circle",
            type: "simple-marker",
        }
    }),
});

function queryBuildings(geometry) {
    let query = sceneLayer.createQuery();
    query.geometry = geometry;
    query.spatialRelationship = "intersects";
    query.returnGeometry = true;
    query.outFields = ["*"];

    sceneLayer.queryFeatures(query).then(function(results) {
        const buildings = results.features.map(feature => feature.attributes);
        sendSelectionToDash(buildings);
    });
}
let arcgisToolInstance = null

function initializeArcGISTool() {
    // move sketch or reload sketch
    console.log('initializeSketchTool statement')
    const sketch = JTSketchWidget.createSketch(graphicsLayer, view, "arcgis-sketch-container");
    JTSketchWidget.setupSketchEventListeners(sketch, tileLayer);
    sketch.on("create", function(event) {
        if (event.state === "complete") {
            const geometry = event.graphic.geometry;
            queryBuildings(geometry);
        }
    });

    const event = new CustomEvent('arcgis-tool-initialized');
    document.dispatchEvent(event);
}

arcgisToolInstance = initializeArcGISTool()

// ORIGINAL SENDSELECTIONTODASH FUNCTION
// function sendSelectionToDash(buildings) {
//     fetch('/jtdash/selection', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 buildings: buildings
//             }),
//         }).then(response => response.json())
//         .then(data => {
//             console.log('Success:', data);
//         })
//         .catch((error) => {
//             console.error('Error:', error);
//         });
// }

// test: function to populate the dcc.Store with data from localStorage location @_@
function populateStore() {
    // Retrieve data from localStorage
    const eff_yr_blt_chart = localStorage.getItem('eff-yr-blt-chart');
    const tot_lvg_area_chart = localStorage.getItem('tot-lvg-area-chart');
    const just_value_chart = localStorage.getItem('just-value-chart');
    const doruc_chart = localStorage.getItem('doruc-chart');

    // Update the dcc.Store component
    const storeElement = document.querySelector('#chart-data-store');
    const data = {
        eff_yr_blt_chart: eff_yr_blt_chart ? JSON.parse(eff_yr_blt_chart) : [],
        tot_lvg_area_chart: tot_lvg_area_chart ? JSON.parse(tot_lvg_area_chart) : [],
        just_value_chart: just_value_chart ? JSON.parse(just_value_chart) : [],
        doruc_chart: doruc_chart ? JSON.parse(doruc_chart) : []
    };

    // Trigger an event or store the data
    if (storeElement) {
        const event = new CustomEvent('updateChartData', { detail: data });
        storeElement.dispatchEvent(event);
    }
}


function sendSelectionToDash(buildings) {
    // Prepare data for the POST request
    const payload = {
        buildings: buildings
    };

    // Send a POST request to the Flask backend
    fetch('/jtdash/selection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),  // Convert the JavaScript object to JSON
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        console.log("Received response from Flask:", data);

        const event = new CustomEvent("update-charts", {
            detail: { chartData: data.selection }
        });
        document.getElementById('event-listener-container').dispatchEvent(event);
        // window.dispatchEvent(event);  // Dispatch the event to trigger Dash callback
    })
    .catch(error => {
        console.error("Error sending selection to Dash:", error);
    });
}

// test: dummy update-charts event
// window.addEventListener('update-charts', (e) => {
//     console.log('Event received:', e);
// });
//

// const event = new CustomEvent('update-charts', {
//     detail: {
//         chartData: {
//             effyrblt_chart: [{ label: "Year Built", value: 2000 }],
//             totlvgarea_chart: [{ label: "Living Area", value: 1500 }],
//             jv_chart: [{ label: "Just Value", value: 300000 }],
//             doruc_chart: [{ label: "DORUC", value: 100 }]
//         }
//     }
// });
// document.getElementById('event-listener-container').dispatchEvent(event);




// test: event listener for the "Populate Charts" button
// const populateChartsButton = document.getElementById('populate-charts');
// if (populateChartsButton) {
//     populateChartsButton.addEventListener('click', function() {
//         const event2 = new CustomEvent('update-charts', {
//             detail: {
//                 chartData: {
//                     effyrblt_chart: [{ label: "Year Built", value: 2000 }],
//                     totlvgarea_chart: [{ label: "Living Area", value: 1500 }],
//                     jv_chart: [{ label: "Just Value", value: 300000 }],
//                     doruc_chart: [{ label: "DORUC", value: 100 }]
//                 }
//             }
//         });
//         document.getElementById('event-listener-container').dispatchEvent(event2);
//     });
// }

// test: try to send data to dcc.Store from sendSelectionToDash function
// function sendSelectionToDash(buildings) {
//     fetch('/jtdash/selection', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 buildings: buildings
//             }),
//         }).then(response => response.json())
//         .then(data => {
//             console.log('Success:', data);
//
//             // Update the dcc.Store with the processed data from the backend
//             const store = document.querySelector('#chart-data-store');
//             store.dispatchEvent(new CustomEvent('store-update', { detail: data.selection }));
//         })
//         .catch((error) => {
//             console.error('Error:', error);
//         });
// }


// document.addEventListener('store-update', function(event) {
//     // Update the dcc.Store with new data
//     let storeElement = document.getElementById("chart-data-store");
//     storeElement.data = event.detail;
// })

let basemapGallery = new vendors.BasemapGallery({
    view: view,
    container: "arcgis-basemap-gallery-container"
});

view.ui.add(locateWidget, "bottom-right");
view.ui.move(["zoom", "navigation-toggle", "compass"], "bottom-right");

map.add(sceneLayer);
map.add(graphicsLayer);


const categories = {
    DORUC: {
        field: "DORUC",
        colorStops: [
            { value: 0, color: [255, 255, 255, 0.4] },
            { value: 1, color: [255, 204, 51, 0.7] }, // Yellow for residential
            { value: 2, color: [255, 87, 51, 0.7] },  // Red for commercial
            { value: 3, color: [153, 102, 204, 0.7] } // Purple for industrial
        ]
    },
    EFFYRBLT: {
        field: "EFFYRBLT",
        colorStops: [
            { value: 1950, color: [153, 204, 255, 0.7] }, // Light blue
            { value: 1975, color: [51, 153, 255, 0.7] },  // Blue
            { value: 2000, color: [0, 102, 255, 0.7] }    // Dark blue
        ]
    },
    TOTLVGAREA: {
        field: "TOTLVGAREA",
        colorStops: [
            { value: 1000, color: [204, 255, 204, 0.7] }, // Light green
            { value: 2000, color: [102, 255, 102, 0.7] }, // Green
            { value: 3000, color: [0, 153, 0, 0.7] }      // Dark green
        ]
    },
    JV: {
        field: "JV",
        colorStops: [
            { value: 100000, color: [255, 255, 153, 0.7] }, // Light yellow
            { value: 500000, color: [255, 204, 0, 0.7] },  // Orange
            { value: 1000000, color: [255, 153, 0, 0.7] }  // Dark orange
        ]
    }
};

// Function to recolor the buildings based on selected category
function recolorBuildings(category) {
    const selectedCategory = categories[category];
    let renderer = {
        type: "simple",
        symbol: {
            type: "mesh-3d",
            symbolLayers: [{
                type: "fill",
                material: { color: [255, 255, 255, 0.7], colorMixMode: "replace" },
                edges: null
            }]
        },
        visualVariables: [{
            type: "color",
            field: selectedCategory.field,
            stops: selectedCategory.colorStops
        }]
    };

    sceneLayer.renderer = renderer; // Apply renderer to the sceneLayer
}

// Create buttons to control recoloring
document.getElementById("doruc-button").addEventListener("click", () => recolorBuildings("DORUC"));
document.getElementById("effyrblt-button").addEventListener("click", () => recolorBuildings("EFFYRBLT"));
document.getElementById("totlvgarea-button").addEventListener("click", () => recolorBuildings("TOTLVGAREA"));
document.getElementById("justvalue-button").addEventListener("click", () => recolorBuildings("JV"));


const setElementId = (element, id) => {
    if (element) {
        element.id = id;
    }
}

view.when(() => {
    view.map.basemap.referenceLayers.forEach(layer => {
        if (layer.title === "Buildings") {
            layer.visible = false
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
        document.querySelector('.esri-locate.esri-widget.esri-component'),
        "customLocateButton"
    );
    setElementId(
        document.querySelector('.esri-component.esri-zoom.esri-widget'),
        "customZoomButton"
    );
    setElementId(
        document.querySelector('.esri-ui-bottom-right.esri-ui-corner'),
        "uiCornerBottomRight"
    );
    setElementId(
        document.querySelector('.esri-component.esri-navigation-toggle.esri-widget'),
        "customNavigationToggle"
    );
});

view.whenLayerView(sceneLayer).then((layerView) => {
    const selectionSketch = JTSelectionSketch.initWidget(layerView, "selection-widget-container");
        selectionSketch.on("create", function(event) {
        if (event.state === "complete") {
            const geometry = event.graphic.geometry;
            queryBuildings(geometry);
        }
    });

    const store = document.querySelector('#chart-data-store');
    if (store) {
        console.log("Store found: ", store);
    } else {
        console.log("Store not found");
    }
    // view.ui.add(selectionSketch)
});
