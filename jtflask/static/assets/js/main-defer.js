/*global vendors*/
// noinspection JSCheckFunctionSignatures

/*
 * main-defer.js
 * ---------------------
 * Purpose: This script defines and manipulates DOM elements created with
 *          ArcGIS Maps SDK for JavaScript.
 * Scope: Define layers, maps, and widgets used in the sceneView.
 *        Handles event listeners, dynamic updates to the DOM.
 *        Avoid defining specific behaviors and rules. e.g., how a query works.
 */

JTSplashPage.hideSplash();

JTDash.loadSvg(
    '/jtdash/assets/svg/legend_icon.svg',
    'legend-svg'
);
JTDash.loadSvg(
    '/jtdash/assets/svg/basemap_icon.svg',
    'basemap-svg'
);

const bldgSceneServer = "https://services.arcgis.com" +
    "/LBbVDC0hKPAnLRpO/arcgis/rest/services/" +
    "PLW__JTAoi_Jax__WebLayer_AGOL/SceneServer"

const Downtown_Saint_Jones_River_SceneServer = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/" +
    "arcgis/rest/services/PLW_Jacksonville_BLD_Downtown_Saint_Jones_River/SceneServer"

const Ribault_2_SceneServer = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/" +
    "arcgis/rest/services/PLW_Jacksonville_BLD_Ribault_2/SceneServer"

const Ribault_Scenic_Drive_Park_SceneServer = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/" +
    "arcgis/rest/services/PLW_Jacksonville_BLD_Ribault_Scenic_Drive_Park/SceneServer"

const Hogen_Creek_Neighborhood_SceneServer = "https://services.arcgis.com/LBbVDC0hKPAnLRpO/" +
    "arcgis/rest/services/PLW_Jacksonville_BLD_Hogen_Creek_Neighborhood/SceneServer"

const demImageServer = "https://tiledimageservices.arcgis.com/" +
    "LBbVDC0hKPAnLRpO/arcgis/rest/services/" +
    "USGS_1M_DEM_50M_Resample/ImageServer";

const tileLayer = new vendors.ImageryTileLayer({
    url: demImageServer
});
const graphicsLayer = new vendors.GraphicsLayer({
    elevationInfo: {
        mode: "relative-to-ground"
    }
});
const initializeMap = JTMap.initMap("digital-twin-container", bldgSceneServer);

//Move zoom, navigation, and compass to the bottom right
initializeMap.view.ui.move(["compass", "zoom", "navigation-toggle"], "bottom-right");

// Create the Locate widget
const locateWidget = new vendors.Locate({
    view: initializeMap.view,
    graphic: new vendors.Graphic({
        symbol: {
            outline: {
                color: "whit    e",
                width: 1, // points
            },
            color: "blue",
            size: "12px", // pixel
            style: "circle",
            type: "simple-marker",
        },
    }),
});
initializeMap.view.ui.add(locateWidget, "bottom-right");


//Add Fullscreen widget
const fullscreenWidget = new vendors.Fullscreen({
    view: initializeMap.view
});

initializeMap.view.ui.add(fullscreenWidget, "bottom-right");

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

initializeMap.view.whenLayerView(initializeMap.sceneLayer).then((layerView) => {

    const selectionSketch = JTSelectionSketch.initWidget(
        layerView,
        "selection-widget-container"
    );

    // Call selectAllBuilds after widget loads
    JTSelectionSketch.selectAllBuildings(layerView);
});
