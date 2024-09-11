const BuildingQueryTool = (() => {
    "use strict";

    // Function to initialize the ArcGIS Sketch tool for building queries
    function initializeBuildingQueryTool(graphicsLayer, view, tileLayer, sceneLayer) {
        console.log('Initializing Building Query Tool');

        // Create the sketch widget for drawing on the map
        const sketch = JTSketchWidget.createSketch(graphicsLayer, view, "arcgis-sketch-container");
        JTSketchWidget.setupSketchEventListeners(sketch, tileLayer);

        // Event listener when a new geometry is drawn
        sketch.on("create", function (event) {
            if (event.state === "complete") {
                const geometry = event.graphic.geometry;
                queryBuildingsStats(geometry, sceneLayer);
            }
        });

        // Dispatch custom event when the tool is initialized
        const event = new CustomEvent('building-tool-initialized');
        document.dispatchEvent(event);

        return sketch;  // Return the sketch instance
    }

    // Function to query building statistics by geometry
    function queryBuildingsStats(geometry, sceneLayer) {
        var query = sceneLayer.createQuery();
        query.geometry = geometry;
        query.spatialRelationship = "intersects";
        query.outStatistics = [
            { onStatisticField: "DORUC", outStatisticFieldName: "DORUC", statisticType: "count" },
            { onStatisticField: "EFFYRBLT", outStatisticFieldName: "EFFYRBLT", statisticType: "avg" },
            { onStatisticField: "TOTLVGAREA", outStatisticFieldName: "TOTLVGAREA", statisticType: "avg" },
            { onStatisticField: "JV", outStatisticFieldName: "JV", statisticType: "avg" }
        ];

        sceneLayer.queryFeatures(query).then(function (results) {
            // Extract building statistics from the result
            const stats = results.features[0].attributes;
            updateBuildingStatsCharts(stats);
        }).catch(function (error) {
            console.error("Error querying building statistics: ", error);
        });
    }

    // Function to update the DMC charts with new building statistics
    function updateBuildingStatsCharts(stats) {
        // Prepare chart data for DORUC, EFFYRBLT, TOTLVGAREA, JV
        const chartData = {
            DORUC: stats.DORUC,
            EFFYRBLT: stats.EFFYRBLT,
            TOTLVGAREA: stats.TOTLVGAREA,
            JV: stats.JV
        };

        // Call the backend to update the charts
        fetch('/jtdash/update-building-stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(chartData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Update DMC charts here using the new data
            // You can use your existing logic to refresh or update the charts dynamically
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // Return the public API for the tool
    return {
        initialize: initializeBuildingQueryTool
    };
})();