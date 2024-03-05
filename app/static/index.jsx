// import {Tile3DLayer, FlyToInterpolator, COORDINATE_SYSTEM } from "deck.gl";
// import {MapboxOverlay as DeckOverlay} from '@deck.gl/mapbox';
import {I3SLoader} from "@loaders.gl/i3s";
// import DeckGL from "@deck.gl/react";
// import {Tile3DLayer} from '@deck.gl/geo-layers';
import {FlyToInterpolator} from '@deck.gl/core';
import {COORDINATE_SYSTEM} from '@deck.gl/core';

// window.DeckOverlay = DeckOverlay;
// window.DeckGL = DeckGL;
// window.Tile3DLayer = Tile3DLayer;
window.FlyToInterpolator = FlyToInterpolator;
window.COORDINATE_SYSTEM = COORDINATE_SYSTEM;
window.I3SLoader = I3SLoader;
