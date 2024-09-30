const JTUtils = (() => {
    "use strict";

    const setElementId = (element, id) => {
        if (element) {
            element.id = id;
        }
    };

    const dorucLandUseMapping = () => {
        return fetch('/jtdash/assets/data/land_use_categories.json')
            .then(response => response.json())
            .then(jsonData => {
                const mapping = {};
                jsonData.forEach(item => {
                    // noinspection JSUnresolvedVariable
                    const doruc = item.doruc;
                    const landUseCategory = item["land use category"];
                    // Store the mapping of doruc to land use category
                    if (doruc && landUseCategory) {
                        mapping[doruc.trim()] = landUseCategory.trim();
                    }
                });
                return mapping;
            })
            .catch(error => {
                console.error('Error loading LUGEN Mapping JSON:', error);
                return {};
            });
    };

    const dorucFieldStops = {
        field: "DORUC",
        stops: [
            { value: 0, color: [255, 255, 255, 0.4] },
            { value: 1, color: [255, 204, 51, 0.7] },  // Yellow for residential
            { value: 2, color: [255, 87, 51, 0.7] },  // Red for commercial
            { value: 3, color: [153, 102, 204, 0.7] } // Purple for industrial
        ]
    };
    const effyrbltFieldStops = {
        field: "EFFYRBLT",
        stops: [
            { value: 1950, color: [153, 204, 255, 0.7] }, // Light blue
            { value: 1975, color: [51, 153, 255, 0.7] },  // Blue
            { value: 2000, color: [0, 102, 255, 0.7] }    // Dark blue
        ]
    };
    const totlvgareaFieldStops = {
        field: "TOTLVGAREA",
        stops: [
            { value: 1000, color: [204, 255, 204, 0.7] }, // Light green
            { value: 2000, color: [102, 255, 102, 0.7] }, // Green
            { value: 3000, color: [0, 153, 0, 0.7] }      // Dark green
        ]
    };
    const jvFieldStops = {
        field: "JV",
        stops: [
            { value: 100000, color: [255, 255, 153, 0.7] }, // Light yellow
            { value: 500000, color: [255, 204, 0, 0.7] },  // Orange
            { value: 1000000, color: [255, 153, 0, 0.7] }  // Dark orange
        ]
    };
    const defaultFieldStops = {
        field: null,  // No specific field needed for default white color
        stops: [
            { value: 0, color: [255, 255, 255, 1] }  // White for resetting
        ]
    };

    return {
        setElementId: setElementId,
        dorucLandUseMapping: dorucLandUseMapping,
        dorucFieldStops: dorucFieldStops,
        effyrbltFieldStops: effyrbltFieldStops,
        totlvgareaFieldStops: totlvgareaFieldStops,
        jvFieldStops: jvFieldStops,
        defaultFieldStops: defaultFieldStops,
    };
})();  // IIFE