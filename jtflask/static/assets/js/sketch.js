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
    let highlightHandle = null;
    let highlightedObjectIds = [];
    let outFields = ["OBJECTID", "DORUC", "JV", "EFFYRBLT","TOTLVGAREA"];

    const initWidget = (sceneLayerView, container) => {
        const sketchLayer = new vendors.GraphicsLayer({
            title: "Selection Layer",
            elevationInfo: {
                mode: "on-the-ground"
            }
        });
        sceneLayerView.view.map.add(sketchLayer);
        // Create SketchViewModel
        const sketchViewModel = new vendors.SketchViewModel({
            layer: sketchLayer,
            view: sceneLayerView.view,
            polygonSymbol: sketchSymbol,
            defaultCreateOptions: {
                hasZ: false  // default value
            },
            creationMode: "update",
            updateOnGraphicClick: true, // Enable updating existing graphics
            defaultUpdateOptions: {
                enableZ: false,  // default value
                tool: "reshape",
                reshapeOptions: {
                    edgeOperation: "offset"
                }
            }
        });
        const selectionSketchWidget = new vendors.Sketch({
            layer: sketchLayer,
            view: sceneLayerView.view,
            container: container,
            availableCreateTools: ["polygon", "rectangle", "circle"],
            viewModel: sketchViewModel,
        });

        selectionSketchWidget.on("create", event => {
            if (event.state === "start") {
                // Clear all existing graphics when a new creation begins
                sketchLayer.removeAll();
                JTHighlight.clearHighlighting();
            }
            if (event.state === "complete") {
                let sketchGeometry = event.graphic.geometry;

                JTSpatialQuery.attributes(sceneLayerView, sketchGeometry, outFields, spatialRelationship).then((results) => {
                    if (results.length > 0) {
                        // dash_clientside.clientside.sendToDash('chart-data-store', results);
                        JTDash.mapToDash('chart-data-store', results);
                    }
                });
            }
        });
        // Listen to sketch widget's update event to update the filter
        selectionSketchWidget.on("update", event => {
            if (event.state === "start") {
                JTHighlight.clearHighlighting();
            }
            if (event.state === "complete" && event.graphics.length > 0) {
                let sketchGeometry = event.graphics[0].geometry;
                JTSpatialQuery.attributes(sceneLayerView, sketchGeometry, outFields, spatialRelationship).then((results) => {
                    if (results.length > 0) {
                        JTDash.mapToDash('chart-data-store', results);
                    }
                });
            }
        });
        return selectionSketchWidget;
    };

    return {
        initWidget: initWidget
    };
})();  // IIFE