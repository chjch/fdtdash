/*global vendors*/

const JTSpatialQuery = (() => {
    const objectIds = (layer, geometry, spatialRelationship) => {
        const queryObjectIds = () => {
            if (!geometry) {
                return;
            }
            const query = layer.createQuery();
            query.geometry = geometry;
            query.spatialRelationship = spatialRelationship;

            return layer.queryObjectIds(query).then((objectIds) => {
                if (objectIds.length > 0) {
                    console.log("Object IDs found:", objectIds);
                    return objectIds;
                }
                return [];  // Return an empty array if no object IDs are found
            });
        };
        // Debounce the query to prevent multiple requests from being sent
        const debouncedQuery = vendors.promiseUtils.debounce(queryObjectIds);
        return debouncedQuery(layer, geometry, spatialRelationship);
    };

    const attributes = (layerView, geometry, outFields, spatialRelationship) => {
        const queryFeatures = () => {
            if (!geometry) {
                return;
            }
            const query = layerView.layer.createQuery();
            query.geometry = geometry;
            query.outFields = outFields;
            query.spatialRelationship = spatialRelationship;
            query.returnGeometry = false;

            return layerView.layer.queryFeatures(query).then((results) => {
                if (results.features.length > 0) {
                    const attributes = results.features.map(feature => feature.attributes);
                    const objectIds = attributes.map(attr => attr.OBJECTID);
                    JTHighlight.highlightBuildings(objectIds, layerView);
                    return attributes;
                }
                return [];  // Return an empty array if no object IDs are found
            });
        };
        // Debounce the query to prevent multiple requests from being sent
        const debouncedQuery = vendors.promiseUtils.debounce(queryFeatures);
        return debouncedQuery(layerView, geometry, outFields, spatialRelationship);
    };

    return {
        objectIds: objectIds,
        attributes: attributes
    };
})(); // IIFE