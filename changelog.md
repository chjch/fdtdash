# Change made in the main branch

## 2024-09-27

### Rename

1. `jtflask/jtdash/callbacks.py`
    - `process_store_data` -> `update_data_store`: following Dash's naming
      convention on callbacks.
    - `toggle_drawer_and_size` -> `toggle_sidebar_drawer`
2. `jtflask/static/assets/js/query.js`
    - `JTNonSpatialQuery` -> `JTAttributeQuery`

### Move

1. `jtflask/static/assets/js/main-defer.js`
    - `recolorBuildings` -> `jtflask/static/assets/js/cityscape.js` as
      `JTBuilding.colorByValueRange()`
    - `filterAndHighlightByCategory` -> `jtflask/static/assets/js/cityscape.js` as
      `JTBuilding.highlightByLandUseCategory()`
2. `Parcels_To_LUGEN_Descripts_2024.csv` -> `land_use_categories.json`

### Change

1. `jtflask/static/assets/js/query.js`: merged `JTAttributeQuery.byFieldName`
   and `JTAttributeQuery.byFieldValue` into `JTAttributeQuery.byField`

### Add

1. `jtflask/static/assets/js/utils.js`
    - migrate `setElementId` from `main-defer.js`
    - migrate `addRecolorListener` from `main-defer.js`
    - migrate `loadLUGENMapping` from `main-defer.js` and rename as
      `JTUtils.dorucLandUseMapping()`
2. `jtflask/static/assets/js/cityscape.js`:
    - new file for 3d city models, e.g., building, road, tree, etc.
    - add `JTBuilding` to handle building-related operations, e.g., recoloring
      and highlighting
