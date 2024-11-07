// Dash related JavaScript code

const JTDash = (() => {
    "use strict";

    const mapToDash = (storeId, mapData) => {
        dash_clientside.set_props(storeId, { data: mapData });
        return dash_clientside.no_update;
    };

    const handleNavbarButtonClick = (...inputs) => {
        //On Initial Render
        if (inputs.every((input) => input === undefined)) {
            handleInitialState();
            return;
        }
        const collapseButtonId = "collapse-button";
        const clickedButtonId = dash_clientside.callback_context.triggered_id;

        if (navbarButtonIds.includes(clickedButtonId)) {
            handleNavbarButtonClassUpdate(clickedButtonId);
            handleNavbarDrawerClassUpdate(clickedButtonId);
        }
        if (clickedButtonId === collapseButtonId) {
            handleCollapseButtonClick(collapseButtonId);
        }
    };

    const loadSvg = (svgFilePath, svgId) => {
        // Fetch the SVG file and insert it into the DOM
        fetch(svgFilePath)
            .then(response => response.text())
            .then(svgContent => {
                document.getElementById(svgId).innerHTML = svgContent;
            }
        );
    };

    // Register functions with dash_clientside object under clientside namespace
    // allow `mapToDash`, `handleNavbarButtonClick` to be called from Dash
    window.dash_clientside = Object.assign({}, window.dash_clientside, {
        clientside: {
            mapToDash: mapToDash,
            handleNavbarButtonClick: handleNavbarButtonClick,
            loadSvg: loadSvg
        },
    });

    return {
        mapToDash: mapToDash,
        loadSvg: loadSvg
    };
})();  // IIFE
