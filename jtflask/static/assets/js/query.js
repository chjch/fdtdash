/*global vendors*/

const queryObjectIds = (layer, geometry, spatialRelationship) => {
    if (!geometry) {
        return;
    }
    const query = layer.createQuery();
    query.geometry = geometry;
    query.spatialRelationship = spatialRelationship;

    return layer.queryObjectIds(query).then((objectIds) => {
        if (objectIds.length > 0) {
            return objectIds;
        }
        return [];  // Return an empty array if no object IDs are found
    });
};

const JTSpatialQuery = (() => {
    const runQuery = (layer, geometry, spatialRelationship) => {
        // Debounce the query to prevent multiple requests from being sent
        const debouncedQuery = vendors.promiseUtils.debounce(queryObjectIds);
        return debouncedQuery(layer, geometry, spatialRelationship);
    }
    return {
        runQuery: runQuery
    };
})(); // IIFE