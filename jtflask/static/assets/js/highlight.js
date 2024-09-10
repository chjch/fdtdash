/*global vendors*/
const JTHighlight = (() => {
    "use strict";

    let highlightHandle = null;
    const clearHighlighting = () => {
        if (highlightHandle) {
            highlightHandle.remove();
            highlightHandle = null;
        }
    };

    const highlightBuildings = (sketchGeometry, sceneLayerView) => {
        // Remove any previous highlighting
        clearHighlighting();

        let spatialRelationship = "intersects";

        JTSpatialQuery.runQuery(sceneLayerView, sketchGeometry, spatialRelationship).then((results) => {
            if (results.length > 0) {
                highlightHandle = sceneLayerView.highlight(results);
            }
        });
    };

    return {
        clearHighlighting: clearHighlighting,
        highlightBuildings: highlightBuildings
    };
})();  // IIFE