// Import the necessary ArcGIS API classes
// import Map from "@arcgis/core/Map";
// import SceneView from "@arcgis/core/views/SceneView";
// import { DeckLayer } from "@deck.gl/arcgis";
// import { GeoJsonLayer, ArcLayer } from "@deck.gl/layers";

// Export the classes
export { default as Map } from "@arcgis/core/Map";
export { default as SceneView } from "@arcgis/core/views/SceneView";
export { default as GeoJSONLayer } from "@arcgis/core/layers/GeoJSONLayer";
export { default as FeatureLayer } from "@arcgis/core/layers/FeatureLayer";
export { default as SceneLayer } from "@arcgis/core/layers/SceneLayer";
export { default as Zoom } from "@arcgis/core/widgets/Zoom";
export { default as Locate } from "@arcgis/core/widgets/Locate";
export { default as BasemapToggle } from "@arcgis/core/widgets/BasemapToggle";
export { default as Compass } from "@arcgis/core/widgets/Compass";
export { default as NavigationToggle } from "@arcgis/core/widgets/NavigationToggle";
export { default as Graphic } from "@arcgis/core/Graphic";
// export { default as MapView } from "@arcgis/core/views/MapView";
// export * as externalRenderers from '@arcgis/core/views/3d/externalRenderers';
// export { externalRenderers };

// export { DeckLayer, loadArcGISModules } from "@deck.gl/arcgis";
export { DeckRenderer } from "@deck.gl/arcgis";
export { GeoJsonLayer, ArcLayer, ScatterplotLayer } from "@deck.gl/layers";

// window.SceneView = SceneView;
// Path: jtflask/static/assets/js/vendors.min.js
// Compare this snippet from jtflask/static/assets/js/arcgis-defer.js:
