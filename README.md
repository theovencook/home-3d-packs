# Home 3D packs

Furniture packs for [Home 3D](https://github.com/theovencook/home-3d), a floor plan and 3D room planner for
Home Assistant. One folder per pack. All packs are MIT licensed (see `LICENSE`).

Home 3D already ships with these packs and works offline. The copies here let you update a pack without
waiting for a new Home 3D version: Home 3D checks each pack's own `release` number and offers a newer one.

## Packs

### Home 3D core

- Pack id: `theovencook.core`
- 847 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.core

Everyday furniture for every room, made for Home 3D. Ships with the app and works offline.

### IKEA UK range

- Pack id: `theovencook.ikea-uk`
- 408 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.ikea-uk

IKEA UK bestsellers in their sizes, modelled for Home 3D from simple shapes. Search by the readable name or the IKEA name. Not made or endorsed by IKEA.

## Install a pack

In Home 3D open **Extensions**, choose **Install from GitHub**, paste a pack's install URL and confirm. Home
Assistant downloads and checks the pack; nothing else is fetched. Pasting the repository URL
(`https://github.com/theovencook/home-3d-packs`) lists the packs and asks for one folder URL.

## Update a pack

The update check compares each installed pack's `release` in its `pack.json` with the one here, so a new
release of one pack does not show as an update for the others.

## Contributing and format

The pack format is described in the Home 3D repository (`docs/packs.md`). These folders are generated from
the packs in Home 3D with `tools/publish_packs.py`; send changes to Home 3D rather than editing them here.

## Trademarks

IKEA is a trademark of Inter IKEA Systems B.V. The IKEA UK pack (theovencook.ikea-uk/) names IKEA products only so they can be found; its models are our own work, built from simple shapes. Home 3D is not affiliated with, sponsored by or endorsed by IKEA or Inter IKEA Systems B.V.
