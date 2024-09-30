const JTBuilding = (() => {
    "use strict";

    const colorByValueRanges = (fieldStops) => {
        return {
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
            },
            visualVariables: [{
                type: "color",
                field: fieldStops.field,
                stops: fieldStops.stops
            }]
        };
    };

    const highlightByLandUseCategory = (layerView, mapping, category) => {
        JTAttributeQuery.byField(sceneLayer, 'DORUC', undefined,["OBJECTID", "DORUC"])
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
    // Return the public API
    return {
        colorByValueRanges: colorByValueRanges,
        highlightByLandUseCategory: highlightByLandUseCategory
    };
})();  // IIFE
