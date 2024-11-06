/*global vendors*/
const JTMap = (() => {
    "use strict";

    let mapInstance = null;
    let viewInstance = null;
    let currentLayer = null;
    let currentLayerUrl = null;

    // Initialize map and scene layer with parameters for map container ID and layer URL
    const initMap = (mapContainerId, layerUrl, zoomToFullExtent = false) => {
        // Initialize map instance if not already created
        mapInstance = mapInstance || new vendors.Map({
            basemap: "navigation-dark-3d",
            ground: "world-elevation"
        });

        // Set up the SceneView
        viewInstance = viewInstance || new vendors.SceneView({
            container: mapContainerId,
            map: mapInstance,
            camera: {
                position: [-81.66916428, 30.29352027, 2569],
                heading: 13.89,
                tilt: 51
            }
        });

        // Initialize scene layer with provided URL and return both view and scene layer
        const sceneLayer = setSceneLayer(layerUrl, zoomToFullExtent);

        return { map: mapInstance, view: viewInstance, sceneLayer: sceneLayer };
    };

    // Set a new scene layer and update the current layer and URL
    const setSceneLayer = (layerUrl, zoomToFullExtent = false) => {
    // Remove the existing layer from the map if any
    if (currentLayer) {
        mapInstance.remove(currentLayer);
    }

    // Create a new SceneLayer with the provided URL
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

    // Add the new layer to the map and update the current URL
    mapInstance.add(currentLayer);
    currentLayerUrl = layerUrl;

     // Wait for the layer to load and get its fullExtent
    currentLayer.when(() => {
        if (zoomToFullExtent && currentLayer.fullExtent) {
            viewInstance.goTo(currentLayer.fullExtent).catch((error) => {
                console.error("Error zooming to layer extent:", error);
            });
        } else if (!currentLayer.fullExtent) {
            console.warn("Full extent not available for the selected layer.");
        }
    }).catch((error) => {
        console.error("Error loading the scene layer:", error);
    });

    // Return the newly created SceneLayer
    return currentLayer;

    };

    // Get the current layer
    const getCurrentLayer = () => currentLayer;

    // Get the URL of the current layer
    const getCurrentLayerUrl = () => currentLayerUrl;

    // Fetch a layer by its ID from the map
    const getLayerById = (layerId) => mapInstance.findLayerById(layerId);

    // Zoom to a specific layer's full extent
    const zoomToLayer = (layer) => {
        if (layer) {
            viewInstance.goTo(layer.fullExtent).catch((error) => {
                console.error("Error zooming to layer:", error);
            });
        }
    };

     // Zoom to a specific extent defined by xmin, ymin, xmax, ymax
    const zoomToExtent = (extentVal) => {
        if (viewInstance) {
            const extent = new vendors.Extent({
                xmin: parseFloat(extentVal.xmin),
                ymin: parseFloat(extentVal.ymin),
                xmax: parseFloat(extentVal.xmax),
                ymax: parseFloat(extentVal.ymax),
                spatialReference: { wkid: 4326 }
            });

            // Calculate the center point from the extent
            const centerPoint = extent.center;

            // Define the target scale or zoom level (optional, adjust as needed)
            const targetScale = 5000;  // Adjust based on required zoom level

            // Set the view to the center with specified scale
            viewInstance.goTo({
                center: [centerPoint.longitude, centerPoint.latitude],
                scale: targetScale
            }).catch((error) => {
                console.error("Error zooming to extent:", error);
            });
        } else {
            console.warn("View instance not initialized.");
        }
    };

    return {
        initMap: initMap,
        setSceneLayer: setSceneLayer,
        getCurrentLayer: getCurrentLayer,
        getCurrentLayerUrl: getCurrentLayerUrl,
        getLayerById: getLayerById,
        zoomToLayer: zoomToLayer,
        zoomToExtent: zoomToExtent
    };
})();
