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

    const svgOnHover = (svgPath, svgId, svgContainerId, colorOnFocus, colorOutFocus) => {
        // Fetch the SVG file and insert it into the DOM
        fetch(svgPath)
            .then(response => response.text())
            .then(svgContent => {
                document.getElementById(svgId).innerHTML = svgContent;

                // Now the SVG is in the DOM, and you can manipulate it
                const svgPaths = document.querySelectorAll(`#${svgId} path`);

                document.getElementById(svgContainerId)
                    .addEventListener('mouseover', () => {
                        svgPaths.forEach((path) => {
                            ['fill', 'stroke'].forEach(attr => {
                                if (path.getAttribute(attr)) {
                                    path.setAttribute(attr, colorOnFocus);  // Change both fill and stroke to white if they exist
                                }
                            });
                        });
                    });
                document.getElementById(svgContainerId)
                    .addEventListener('mouseout', () => {
                        svgPaths.forEach((path) => {
                            ['fill', 'stroke'].forEach(attr => {
                                if (path.getAttribute(attr)) {
                                    path.setAttribute(attr, colorOutFocus);  // Change both fill and stroke to white if they exist
                                }
                            });
                        });
                    });
            });
    };

    return {
        sendToDash: sendToDash,
        svgOnHover: svgOnHover
    };
})();  // IIFE
