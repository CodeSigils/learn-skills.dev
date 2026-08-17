---
name: ag-grid
description: Use when working with AG Grid.
---

# AG Grid

## Every column carries an explicit `colId`

Set `colId` on every column definition, including field-backed columns where AG Grid would otherwise derive the same id from `field`. Column groups carry an explicit `groupId` the same way.

Page objects can address cells by `col-id`, so an explicit id decouples selector stability from field naming. It also survives a later switch to a `valueGetter`, which could otherwise change the derived id and break every selector at once.

Don't strip either as redundant during a review sweep. Duplicating `field` is the point.

## Style cells with `cellStyle`, not Tailwind classes in `cellClass`

The Theming API injects its stylesheet at runtime, after the app's CSS. A Tailwind utility in `cellClass` can therefore lose to the theme.

Use `cellStyle` for anything the theme also controls. Reserve `cellClass` for utilities the theme doesn't touch, where it works fine.

This is specificity-by-load-order, so it won't reproduce in a style debugger that shows the class as present. The class is present. It lost.

## A column's data type comes from the first row

AG Grid infers a column's type from the value in the **first row**, not from the column as a whole.

One solution is to use a `valueGetter` that returns a string. A `valueFormatter` over a boolean `field` runs after the inference has happened, so it does not help.

## Address grids by role and id in tests

Prefer locating cells by their `gridcell` role together with `col-id`, rather than by position or by text alone. That pairs with the explicit-`colId` rule above and keeps a page object stable when columns are reordered.

Class selectors do not work. In v36 a selector like `.ag-center-cols-container` finds nothing. Use `[role="row"]:has([role="gridcell"])` with `row-index` and `col-id`.

Columns virtualize horizontally as well, so a column scrolled out of view has no cell in the DOM to assert against.

## Identify a row by its id, never by matching its text

Supply `getRowId`, which makes the grid render `row-id`, and address rows by that. Comparing an exact set of ids asserts both directions of a split at once: what should be present and what should not.

Substring-matching a row's name against the row text breaks as soon as two rows share a name fragment. The failure then reads as data leaking between groups rather than as a bad selector, which sends the investigation to the wrong place.

## The grid host needs a definite height

Give the wrapper a definite height. A `min-h` alone collapses `ag-root-wrapper` to about two pixels.

Role-based assertions still pass against a collapsed grid, because the rows are in the DOM. This one fails silently in tests and shows up only in a browser.
