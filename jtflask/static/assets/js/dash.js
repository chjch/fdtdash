// Dash related JavaScript code

const JTDash = (() => {
    "use strict";

    const sendToDash = (storeId, mapData) => {
        dash_clientside.set_props(storeId, {data: mapData});
        return dash_clientside.no_update;
    };

    let currentLayer = null;
    let currentLayerUrl = null;

    const dashToMap = (data) => {

        const updateLayerTexture = (mode) => {
            let color = "blue";
            let colorMixMode = "replace";

            switch (mode) {
                case "original":
                    sceneLayer.renderer = null;
                    return;
                case "select":
                    color = "violet";
                    colorMixMode = null; //  original texture
                    break;
                case "emphasize":
                    color = "teal";
                    colorMixMode = "tint"; // Highlight
                    break;
                case "desaturate":
                    color = "yellow";
                    colorMixMode = "tint"; // Desaturate
                    break;
                case "replace":
                    color = "gray";
                    colorMixMode = "replace"; // Remove texture
                    break;
                default:
                    console.warn("Unknown texture mode:", mode);
                    return;
            }
            // Apply the new renderer to the scene layer
            sceneLayer.renderer = {
                type: "simple",
                symbol: {
                    type: "mesh-3d",
                    symbolLayers: [
                        {
                            type: "fill",
                            material: {
                                color: color,
                                colorMixMode: colorMixMode
                            }
                        }
                    ]
                }
            };
        };

        const setSceneLayer = (layerUrl) => {
            if (currentLayer) {
                JTMap.map.remove(currentLayer);
            }

            currentLayer = new vendors.SceneLayer({
                url: layerUrl,
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
                }
            });

            JTMap.map.add(currentLayer);
            currentLayerUrl = layerUrl;
    };

        // Define zoomToExtent function
        const zoomToExtent = (extent) => {
            if (extent) {
                view.goTo({
                    extent: new vendors.Extent({
                        xmin: extent.xmin,
                        ymin: extent.ymin,
                        xmax: extent.xmax,
                        ymax: extent.ymax,
                        spatialReference: { wkid: 4326 }
                    })
                });
            } else {
                console.warn("Extent data is missing for zoom operation.");
            }
        };

        if (data) {
            console.log("Data received from Dash:", data);

            // Handle map actions based on the action type
            if (data.action === "setRenderer") {
                const {mode, layerId} = data.payload;
                const layer = JTMap.getLayerById(layerId);
                JTBuilding.setRenderer(layer, mode);

            } else if (data.action === "zoomToExtent") {
                const {extent_payload} = data.payload;
                JTMap.zoomToExtent(extent_payload);
                // zoomToExtent(extent_payload);

            } else if (data.action === "updateLayerTexture") {
                const {mode} = data.payload;
                updateLayerTexture(mode);

            } else if (data && data.action === "updateSceneLayer") {
                const {layerUrl} = data.payload;
                setSceneLayer(layerUrl);

            } else if (data && data.action === "initMap") {
                const {mapContainerId,layerUrl,zoomToFullExtent} = data.payload;
                JTMap.initMap(mapContainerId,layerUrl,zoomToFullExtent);

            } else {
                console.warn("Unknown action received from Dash:", data.action);
            }
        } else {
            console.warn("No data received from Dash.");
        }
    };


    const clearOutDash = (storeId) => {
        dash_clientside.set_props(storeId, {data: []});
        return dash_clientside.no_update;
    };

    // Register the function with dash_clientside object under clientside namespace
    window.dash_clientside = Object.assign({}, window.dash_clientside, {
        clientside: {
            sendToDash: sendToDash,
            dashToMap: dashToMap,
            // clearOutDash: clearOutDash

        }
    });

    const svgOnHover = (svgPath, svgId, svgContainerId, colorOnFocus, colorOutFocus) => {
        // Fetch the SVG file and insert it into the DOM
        fetch(svgPath)
            .then(response => response.text())
            .then(svgContent => {
                document.getElementById(svgId).innerHTML = svgContent;

                // Now the SVG is in the DOM, and you can manipulate it
                const svgPaths = document.querySelectorAll(`#${svgId} path`);

                document.getElementById(svgContainerId)
                    .addEventListener('mouseover', () => {
                        svgPaths.forEach((path) => {
                            ['fill', 'stroke'].forEach(attr => {
                                if (path.getAttribute(attr)) {
                                    path.setAttribute(attr, colorOnFocus);  // Change both fill and stroke to white if they exist
                                }
                            });
                        });
                    });
                document.getElementById(svgContainerId)
                    .addEventListener('mouseout', () => {
                        svgPaths.forEach((path) => {
                            ['fill', 'stroke'].forEach(attr => {
                                if (path.getAttribute(attr)) {
                                    path.setAttribute(attr, colorOutFocus);  // Change both fill and stroke to white if they exist
                                }
                            });
                        });
                    });
            });
    };

    return {
        sendToDash: sendToDash,
        svgOnHover: svgOnHover,
        dashToMap: dashToMap,

        // setSceneLayer: setSceneLayer,
        // getCurrentLayer: () => currentLayer
        // clearOutDash: clearOutDash
    };
})();  // IIFE
