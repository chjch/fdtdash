// Dash related JavaScript code

const JTDash = (() => {
    "use strict";

    const sendToDash = (storeId, mapData) => {
        dash_clientside.set_props(storeId, { data: mapData });
        return dash_clientside.no_update;
    };
    // Register the function with dash_clientside object under clientside namespace
    window.dash_clientside = Object.assign({}, window.dash_clientside, {
        clientside: {
            sendToDash: sendToDash
        }
    });

    return {
        sendToDash: sendToDash
    };
})();  // IIFE
