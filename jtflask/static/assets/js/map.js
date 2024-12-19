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


        let arcgisToolInstance = null

        function initializeArcGISTool() {
            // move sketch or reload sketch
            // console.log('initializeSketchTool statement')
            const sketch = JTSketchWidget.createSketch(graphicsLayer, viewInstance, "arcgis-sketch-container");
            JTSketchWidget.setupSketchEventListeners(sketch, tileLayer);
            sketch.on("create", function (event) {
                if (event.state === "complete") {
                    const geometry = event.graphic.geometry;
                    queryBuildings(geometry);
                }
            });

            const event = new CustomEvent('arcgis-tool-initialized');
            document.dispatchEvent(event);
        }

        arcgisToolInstance = initializeArcGISTool()

        // We render the basemap gallery into the container we created for it
        const baseMapGalleryContainer = document.querySelector(
            "#basemap-gallery-card-content"
        );
        const basemapGallery = new vendors.BasemapGallery({
            view: JTMap.getSceneView(),
            container: baseMapGalleryContainer,
        });


        // Move the container into the basemap card
        document.querySelector("#basemap-gallery-card").appendChild(baseMapGalleryContainer);

        // Floating card test for building selection stats
        JTFloatingCard.init(
            document.getElementById('building-selection-stats-card'),
            document.getElementById('building-selection-stats-card'),  // Assuming same element for drag handle
            document.getElementById('undock-button'),
            document.getElementById('dock-icon'),
            document.getElementById('digital-twin-container')
        );

        // noinspection JSIgnoredPromiseFromCall
        viewInstance.when(() => {
            viewInstance.map.basemap.referenceLayers.forEach(layer => {
                if (layer.title === "Buildings") {
                    layer.visible = false
                }
            });
            let query = sceneLayer.createQuery();
            query.returnGeometry = true;
            query.outFields = ["*"];


            JTUtils.setElementId(
                document.querySelector(
                    ".esri-locate.esri-widget.esri-component"
                ),
                "customLocateButton"
            );
            JTUtils.setElementId(
                document.querySelector(
                    ".esri-component.esri-zoom.esri-widget"
                ),
                "customZoomButton"
            );
            JTUtils.setElementId(
                document.querySelector(
                    ".esri-component.esri-navigation-toggle.esri-widget"
                ),
                "customNavigationToggle"
            );
            JTUtils.setElementId(
                document.querySelector(
                    ".esri-component.hide-interface.esri-widget"
                ),
                "customHideInterface"
            );
            JTUtils.setElementId(
                document.querySelector(
                    ".esri-component.esri-fullscreen.esri-widget"
                ),
                "customFullscreen"
            );
            // esri-component esri-fullscreen esri-widget
            // noinspection CssInvalidHtmlTagReference
            document.getElementById("customNavigationToggle")
                .querySelector("calcite-button")
                .shadowRoot.querySelector('button')
                .style.setProperty('border-bottom-color', '#5932EA')
            JTUtils.setElementId(
                document.querySelector(
                    ".esri-ui-bottom-right.esri-ui-corner"
                ),
                "uiCornerBottomRight"
            );
        });

        viewInstance.whenLayerView(sceneLayer).then((layerView) => {

            JTSelectionSketch.selectAllBuildings(layerView);


            const colorVariableButtons = {
                "doruc-button": JTUtils.dorucFieldStops,
                "effyrblt-button": JTUtils.effyrbltFieldStops,
                "totlvgarea-button": JTUtils.totlvgareaFieldStops,
                "justvalue-button": JTUtils.jvFieldStops,
                "reset-color-button": JTUtils.defaultFieldStops
            };

            Object.keys(colorVariableButtons).forEach(buttonId => {
                document.getElementById(buttonId).addEventListener("click", () => {
                    // noinspection JSValidateTypes
                    sceneLayer.renderer = JTBuilding.colorByValueRanges(colorVariableButtons[buttonId]);
                });
            });

            JTUtils.dorucLandUseMapping().then(mapping => {
                const buttons = [
                    {id: 'highlight-residential', category: 'RESIDENTIAL'},
                    {id: 'highlight-retail', category: 'RETAIL/OFFICE'},
                    {id: 'highlight-vacant', category: 'VACANT NONRESIDENTIAL'},
                    {id: 'highlight-industrial', category: 'INDUSTRIAL'},
                    {id: 'highlight-agricultural', category: 'AGRICULTURAL'}
                ];
                buttons.forEach(button => {
                    document.getElementById(button.id).addEventListener('click', () => {
                        JTBuilding.highlightByLandUseCategory(layerView, mapping, button.category);
                    });
                });
            });
        });


        return {map: mapInstance, view: viewInstance, sceneLayer: sceneLayer};
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

    const switchSceneLayer = (newLayerUrl, zoomToFullExtent = false) => {
        // Remove the existing layer from the map if any
        if (currentLayer) {
            mapInstance.remove(currentLayer);
        }

        // Create a new SceneLayer with the provided URL
        currentLayer = new vendors.SceneLayer({
            url: newLayerUrl,
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
        currentLayerUrl = newLayerUrl;

        // Wait for the layer to load and get its fullExtent
        currentLayer.when(() => {
            if (zoomToFullExtent && currentLayer.fullExtent) {
                viewInstance.goTo(currentLayer.fullExtent).catch((error) => {
                    console.error("Error zooming to layer extent:", error);
                });
            } else if (!currentLayer.fullExtent) {
                console.warn("Full extent not available for the selected layer.");
            }

            // Initialize JTSelectionSketch for the new SceneLayer
            viewInstance.whenLayerView(currentLayer).then((sceneLayerView) => {
                // Call unloadWidget to ensure previous instances are cleared
                // JTSelectionSketch.unloadWidget(viewInstance);

                // Initialize the sketch tool for the new SceneLayerView
                JTSelectionSketch.initWidget(sceneLayerView, "selection-widget-container");
                JTSelectionSketch.selectAllBuildings(sceneLayerView);


            }).catch((error) => {
                console.error("Error initializing JTSelectionSketch:", error);
            });



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
    const getLayerById = (layerId) => {
        const layer = mapInstance.findLayerById(layerId);
        if (!layer) {
            console.warn(`Layer with ID ${layerId} not found.`);
        }
        return layer;
    };

    // Get the current SceneView instance
    const getSceneView = () => {
        if (!viewInstance) {
            console.warn("SceneView has not been initialized.");
        }
        return viewInstance;
    };

    // Get the current Map instance
    const getMap = () => {
        if (!mapInstance) {
            console.warn("Map has not been initialized.");
        }
        return mapInstance;
    };

    // Get the LayerView for a specific layer
    const getLayerView = (layer) => {
        if (!viewInstance) {
            console.warn("View instance not initialized.");
            return null;
        }

        return viewInstance.whenLayerView(layer)
            .then((layerView) => layerView)
            .catch((error) => {
                console.error("Error retrieving LayerView:", error);
                return null;
            });
    };

    // Zoom to a specific layer's full extent
    const zoomToLayer = (layer) => {
        if (layer && layer.fullExtent) {
            viewInstance.goTo(layer.fullExtent).catch((error) => {
                console.error("Error zooming to layer:", error);
            });
        } else {
            console.warn("Layer or layer extent not available.");
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
                spatialReference: {wkid: 4326}
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
        zoomToExtent: zoomToExtent,
        getSceneView: getSceneView,
        getMap: getMap,
        getLayerView: getLayerView,
        switchSceneLayer: switchSceneLayer,
    };
})();
