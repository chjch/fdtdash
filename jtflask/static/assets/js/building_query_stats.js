const BuildingQueryStats = (() => {
    "use strict";

    // Custom event to signal when the tool is initialized
    const dispatchInitializedEvent = () => {
        const event = new CustomEvent('building-tool-initialized');
        document.dispatchEvent(event);
    };

    // Custom event to signal when the tool has finished loading and querying
    const dispatchLoadedEvent = () => {
        const event = new CustomEvent('building-tool-loaded');
        document.dispatchEvent(event);
    };

    // Private function to create a query based on geometry and output stats
    const queryBuildingsByGeometry = (sceneLayerView, sketchGeometry, bufferSize, statDefinitions) => {
        const query = sceneLayerView.createQuery();
        query.geometry = sketchGeometry;
        query.distance = bufferSize;
        query.outStatistics = statDefinitions;

        return sceneLayerView.queryFeatures(query);
    };

    // Function to route data and send it to the server
    const sendSelectionToServer = (statData, route) => {
        fetch(route, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                buildings: statData,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // You can call functions to update the DMC charts with this data here
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    // Function to send data for Effective Year Built chart
    const sendEffectiveYearBuiltData = (stats) => {
        const effYrBltData = [
            stats.EFFYRBLT < 1950 ? 1 : 0,
            stats.EFFYRBLT >= 1950 && stats.EFFYRBLT <= 1975 ? 1 : 0,
            stats.EFFYRBLT > 1975 && stats.EFFYRBLT <= 2000 ? 1 : 0,
            stats.EFFYRBLT > 2000 ? 1 : 0
        ];
        sendSelectionToServer(effYrBltData, '/jtdash/eff-year-built');
    };

    // Function to send data for Total Living Area chart
    const sendTotalLivingAreaData = (stats) => {
        const livingAreaData = [
            stats.TOTLVGAREA < 1000 ? 1 : 0,
            stats.TOTLVGAREA >= 1000 && stats.TOTLVGAREA <= 2000 ? 1 : 0,
            stats.TOTLVGAREA > 2000 && stats.TOTLVGAREA <= 3000 ? 1 : 0,
            stats.TOTLVGAREA > 3000 ? 1 : 0
        ];
        sendSelectionToServer(livingAreaData, '/jtdash/living-area');
    };

    // Function to send data for Just Value chart
    const sendJustValueData = (stats) => {
        const justValueData = [
            stats.JV < 100000 ? 1 : 0,
            stats.JV >= 100000 && stats.JV <= 500000 ? 1 : 0,
            stats.JV > 500000 && stats.JV <= 1000000 ? 1 : 0,
            stats.JV > 1000000 ? 1 : 0
        ];
        sendSelectionToServer(justValueData, '/jtdash/just-value');
    };

    // Function to handle building selection and send data for all charts
    const handleBuildingSelection = (graphic, sceneLayerView, statDefinitions) => {
        return queryBuildingsByGeometry(sceneLayerView, graphic.geometry, 0, statDefinitions).then((result) => {
            const stats = result.features[0].attributes;
            sendEffectiveYearBuiltData(stats);
            sendTotalLivingAreaData(stats);
            sendJustValueData(stats);
            dispatchLoadedEvent();  // Dispatch the loaded event
        });
    };

    // Public function to create and initialize the query tool
    const createBuildingQueryTool = (graphicsLayer, view, sceneLayerView, statDefinitions) => {
        const sketchViewModel = new vendors.SketchViewModel({
            layer: graphicsLayer,
            view: view,
            defaultUpdateOptions: {
                tool: "reshape",
                toggleToolOnClick: false
            },
            defaultCreateOptions: { hasZ: false }
        });

        sketchViewModel.on("create", (event) => {
            if (event.state === "complete") {
                handleBuildingSelection(event.graphic, sceneLayerView, statDefinitions);
            }
        });

        sketchViewModel.on("update", (event) => {
            if (event.state === "complete") {
                handleBuildingSelection(event.graphics[0], sceneLayerView, statDefinitions);
            }
        });

        dispatchInitializedEvent();  // Dispatch the initialized event

        return sketchViewModel;
    };

    return {
        createBuildingQueryTool,
        handleBuildingSelection
    };
})();
