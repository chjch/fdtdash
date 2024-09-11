/*global vendors*/
// noinspection JSCheckFunctionSignatures

JTSplashPage.hideSplashScreen();

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
    container: "deckgl-container", // Reference to the scene div created in step 5
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
    var query = sceneLayer.createQuery();
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

function sendSelectionToDash(buildings) {
    fetch('/jtdash/selection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                buildings: buildings
            }),
        }).then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


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
    var query = sceneLayer.createQuery();
    query.returnGeometry = true;
    query.outFields = ["*"];


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