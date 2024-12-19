/*global vendors*/
const JTSketchWidget = (() => {
    "use strict";

    const getColor = (value) => {
        if (value < 1) {
            return [0, 255, 0, 0.4]; // Green for low values
        } else if (value < 2) {
            return [255, 255, 0, 0.4]; // Yellow for medium-low values
        } else if (value < 3) {
            return [255, 165, 0, 0.4]; // Orange for medium values
        } else if (value < 4) {
            return [255, 69, 0, 0.4]; // Dark Orange for medium-high values
        } else {
            return [255, 0, 0, 0.4]; // Red for high values
        }
    };
    // Function to create the Sketch and SketchViewModel
    const createSketch = (graphicsLayer, view, sketchWidget) => {
        const sketchSymbol3D = new vendors.PolygonSymbol3D({
            symbolLayers: [
                new vendors.ExtrudeSymbol3DLayer({
                    size: 20, // extrude by 3.5m meters
                    material: {
                        color: [255, 255, 255, 0.8]
                    },
                    edges: new vendors.SolidEdges3D({
                        size: 1,
                        color: [82, 82, 122, 1]
                    })
                })
            ]
        });

        // Create SketchViewModel
        const sketchViewModel = new vendors.SketchViewModel({
            layer: graphicsLayer,
            view: view,
            polygonSymbol: sketchSymbol3D,  // Assuming sketchSymbol3D is defined elsewhere or passed as an argument
            defaultCreateOptions: {
                hasZ: true  // default value
            },
            updateOnGraphicClick: true, // Enable updating existing graphics
            defaultUpdateOptions: {
                enableZ: true,  // default value
                tool: "reshape",
                reshapeOptions: {
                    edgeOperation: "offset"
                }
            }
        });

        // Create and return Sketch
        return new vendors.Sketch({
            layer: graphicsLayer,
            view: view,
            viewModel: sketchViewModel,
            creationMode: "update",
            visibleElements: {
                createTools: {
                    rectangle: false,
                    circle: false,
                    point: false,
                    polyline: false,
                },
            },
            container: sketchWidget
        });
    };

    // Function to handle the completion of the sketch
    const handleSketchComplete = (graphic, tileLayer) => {
        let centroid = graphic.geometry.centroid;
        tileLayer.identify(centroid).then(results => {
            let pixelValue = results.value[0];
            graphic.symbol = new vendors.PolygonSymbol3D({
                symbolLayers: [
                    new vendors.ExtrudeSymbol3DLayer({
                        size: 20, // extrude by 20 meters
                        material: {
                            color: getColor(pixelValue)
                        },
                        edges: new vendors.SolidEdges3D({
                            size: 1,
                            color: [82, 82, 122, 1]
                        })
                    })
                ]
            });
        });
    };

    // Function to set up event listeners for the Sketch widget
    const setupSketchEventListeners = (sketch, tileLayer) => {
        sketch.on("create", event => {
            if (event.state === "complete") {
                handleSketchComplete(event.graphic, tileLayer);
            }
        });

        sketch.on("update", event => {
            if (event.state === "complete" && event.graphics.length > 0) {
                handleSketchComplete(event.graphics[0], tileLayer);
            }
        });
    };

    // Return the public API
    return {
        createSketch: createSketch,
        handleSketchComplete: handleSketchComplete,
        setupSketchEventListeners: setupSketchEventListeners
    };
})();

const JTSelectionSketch = (() => {
    "use strict";

    // Define symbol for the filter polygons
    const sketchSymbol = {
        type: "simple-fill", // autocasts as new SimpleFillSymbol()
        color: [255, 140, 0, 0.3],
        style: "solid",
        outline: {
            // autocasts as new SimpleLineSymbol()
            color: [255, 140, 0, 1],
            width: 2
        }
    };

    let spatialRelationship = "intersects";
    let outFields = ["OBJECTID", "DORUC", "JV", "EFFYRBLT", "TOTLVGAREA"];
    let selectionSketchWidget = null;
    let sketchLayer = null;

    /**
     * Removes the initialized Sketch widget, clears graphics, and resets state.
     * @param {SceneView} view - The SceneView instance to clean up.
     */
    const unloadWidget = (view) => {
        const parentContainer = document.getElementById("selection-widget-container");
        if (parentContainer) {
            console.log("Clearing child elements of the container except 'clear-selection-tool-button'...");
            Array.from(parentContainer.children).forEach((child) => {
                if (child.id === "clear-selection-tool-button") {
                    // Skip the "clear-selection-tool-button"
                    return;
                }
                if (typeof child.destroy === "function") {
                    console.log("Destroying custom widget...");
                    child.destroy();
                }
                parentContainer.removeChild(child);
            });
        }

        if (sketchLayer && view) {
            console.log("Removing graphics layer...");
            sketchLayer.removeAll();
            view.map.remove(sketchLayer);
            sketchLayer = null;
        }

        JTHighlight.clearHighlighting();
        console.log("Widget and associated layers cleared.");
    };
    /**
     * Initializes the Sketch widget for a given SceneLayerView.
     * @param {SceneLayerView} sceneLayerView - The SceneLayerView for the active SceneLayer.
     * @param {HTMLElement} container - The container element for the Sketch widget.
     */
    const initWidget = (sceneLayerView, container) => {
        if (!sceneLayerView || !sceneLayerView.view) {
            console.error("SceneLayerView or its view is not defined. Cannot initialize Sketch widget.");
            return;
        }

        // Unload any previous instance of the Sketch widget
        unloadWidget(sceneLayerView.view);

        // Create a new GraphicsLayer for the Sketch widget
        sketchLayer = new vendors.GraphicsLayer({
            title: "Selection Layer",
            elevationInfo: {mode: "on-the-ground"}
        });
        sceneLayerView.view.map.add(sketchLayer);

        // Create the SketchViewModel
        const sketchViewModel = new vendors.SketchViewModel({
            layer: sketchLayer,
            view: sceneLayerView.view,
            polygonSymbol: sketchSymbol,
            defaultCreateOptions: {hasZ: false},
            creationMode: "update",
            updateOnGraphicClick: true,
            defaultUpdateOptions: {
                enableZ: false,
                tool: "reshape",
                reshapeOptions: {edgeOperation: "offset"}
            }
        });

        // Initialize the Sketch widget
        selectionSketchWidget = new vendors.Sketch({
            layer: sketchLayer,
            view: sceneLayerView.view,
            container: container,
            availableCreateTools: ["polygon", "rectangle", "circle"],
            viewModel: sketchViewModel
        });

        // Attach event listeners to the Sketch widget
        selectionSketchWidget.on("create", (event) => {
            if (event.state === "start") {
                sketchLayer.removeAll();
                JTHighlight.clearHighlighting();
            }
            if (event.state === "complete") {
                const sketchGeometry = event.graphic.geometry;
                JTSpatialQuery.attributes(sceneLayerView, sketchGeometry, outFields, spatialRelationship, true)
                    .then((results) => {
                        if (results.length > 0) {
                            JTDash.sendToDash("chart-data-store", results);
                        }
                    });
            }
        });

        selectionSketchWidget.on("update", (event) => {
            if (event.state === "start") {
                JTHighlight.clearHighlighting();
            }
            if (event.state === "complete" && event.graphics.length > 0) {
                const sketchGeometry = event.graphics[0].geometry;
                JTSpatialQuery.attributes(sceneLayerView, sketchGeometry, outFields, spatialRelationship, true)
                    .then((results) => {
                        if (results.length > 0) {
                            JTDash.sendToDash("chart-data-store", results);
                        }
                    });
            }
        });

        // Add event listener for the clear button
        const clearButton = document.getElementById("clear-selection-tool-button");

        if (clearButton) {
            clearButton.addEventListener("click", () => {
                sketchLayer.removeAll();
                JTHighlight.clearHighlighting();
            });
        }

        console.log("Sketch widget initialized for the active SceneLayer.");
        return selectionSketchWidget;
    };

    /**
     * Select all buildings within the current layer's extent.
     * @param {SceneLayerView} sceneLayerView - The SceneLayerView for the active SceneLayer.
     */
    const selectAllBuildings = (sceneLayerView) => {
        if (!sceneLayerView || !sceneLayerView.view) {
            console.error("SceneLayerView or its view is not defined. Cannot select all buildings.");
            return;
        }

        const currentViewExtent = sceneLayerView.view.extent;
        JTSpatialQuery.attributes(sceneLayerView, currentViewExtent, outFields, "contains", false)
            .then((results) => {
                if (results.length > 0) {
                    JTDash.sendToDash("chart-data-store", results);
                }
            })
            .catch((error) => {
                console.error("Error during selectAllBuildings:", error);
            });
    };

    return {
        initWidget: initWidget,
        unloadWidget: unloadWidget,
        selectAllBuildings: selectAllBuildings
    };
})();
