const JTBuilding = (() => {
    "use strict";

    const colorByValueRanges = (fieldStops) => {
        return {
            type: "simple",  // autocasts as new SimpleRenderer()
            symbol: {
                type: "mesh-3d",  // autocasts as new MeshSymbol3D()
                symbolLayers: [{
                    type: "fill",  // autocasts as new FillSymbol3DLayer()
                    material: {
                        color: [255, 255, 255, 0.7],
                        colorMixMode: "replace"
                    },
                    edges: null
                }]
            },
            visualVariables: [{
                type: "color",
                field: fieldStops.field,
                stops: fieldStops.stops
            }]
        };
    };

    const highlightByLandUseCategory = (layerView, mapping, category) => {
        JTAttributeQuery.byField(JTMap.getCurrentLayer(), 'DORUC', undefined,["OBJECTID", "DORUC"])
            .then(attributes => {
                const filteredAttributes = attributes.filter(attr => {
                    const landUseCategory = mapping[attr.DORUC];
                    return landUseCategory === category;
                });
                // noinspection JSUnresolvedVariable
                const objectIds = filteredAttributes.map(attr => attr.OBJECTID);
                JTHighlight.highlightBuildings(objectIds, layerView);
            })
            .catch(error => {
                console.error(`Error fetching attributes for category ${category}:`, error);
            });
    }

        // New function to set the renderer based on the selected type
    const setRenderer = (layer, type) => {
        if (type === "original") {
            // Reset to original by removing any renderer
            layer.renderer = null;
        } else if (type === "select") {
            // Keep the texture unmodified, no color mix
            layer.renderer = getUniqueValueRenderer("purple", null);
        } else if (type === "emphasize") {
            // Apply color tint, but keep the texture
            layer.renderer = getUniqueValueRenderer("red", "tint");
        } else {
            // Apply a white color with either 'tint' or 'replace' based on the type
            const colorMixMode = type === "desaturate" ? "tint" : "replace";

            // Create a SimpleRenderer and apply it to the layer
            const locationRenderer = {
                type: "simple",  // SimpleRenderer
                symbol: {
                    type: "mesh-3d",  // MeshSymbol3D
                    symbolLayers: [{
                        type: "fill",  // FillSymbol3DLayer
                        material: {
                            color: "blue",  // Apply white color
                            colorMixMode: colorMixMode  // Apply mix mode based on the type
                        }
                    }]
                }
            };
            layer.renderer = locationRenderer;
        }
    };

    // Function to create unique value renderer with optional color and colorMixMode
    const getUniqueValueRenderer = (color, colorMixMode) => {
        return {
            type: "unique-value",
            field: "OBJECTID",  // The field to base unique values on
            uniqueValueInfos: [{
                value: null,
                symbol: {
                    type: "mesh-3d",  // MeshSymbol3D
                    symbolLayers: [{
                        type: "fill",  // FillSymbol3DLayer
                        material: {
                            color: color || null,  // Use provided color or keep texture unmodified
                            colorMixMode: colorMixMode || null  // Use provided color mix mode
                        }
                    }]
                }
            }]
        };
    };

    // Return the public API
    return {
        colorByValueRanges: colorByValueRanges,
        highlightByLandUseCategory: highlightByLandUseCategory
    };
})();  // IIFE
