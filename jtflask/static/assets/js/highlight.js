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

    const highlightBuildings = (objectIds, sceneLayerView) => {
        // Remove any previous highlighting
        clearHighlighting();

        if (objectIds.length > 0) {
            highlightHandle = sceneLayerView.highlight(objectIds);
        }
    };

    return {
        clearHighlighting: clearHighlighting,
        highlightBuildings: highlightBuildings
    };
})();  // IIFE