
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


       // // Extract multidimensionalInfo safely, with a default empty object
       //  let multidimensionalInfo = results.multidimensionalInfo || {
       //      dimensions: []  // Default empty dimensions array if multidimensionalInfo is null or undefined
       //  };
       //
       //  console.log("multidimensionalInfo:", multidimensionalInfo);
       //
       //  // Store multidimensionalInfo in the graphic's attributes
       //  graphic.attributes = {
       //      ...graphic.attributes,
       //      multidimensionalInfo: multidimensionalInfo.dimensions.length > 0 ? multidimensionalInfo : {
       //          dimensions: [
       //              { time: "2024-08-07T16:00:00Z", depth: 100, value: 45 },
       //              { time: "2024-08-07T17:00:00Z", depth: 150, value: 50 }
       //          ]
       //      }
       //  };


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
``
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