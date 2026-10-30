# Home 3D packs

Furniture packs for [Home 3D](https://github.com/theovencook/home-3d), a floor plan and 3D room planner for
Home Assistant. One folder per pack. All packs are MIT licensed (see `LICENSE`).

Home 3D already ships with these packs and works offline. The copies here let you update a pack without
waiting for a new Home 3D version: Home 3D checks each pack's own `release` number and offers a newer one.

## Packs

### Bedroom & kids

- Pack id: `theovencook.bedroom`
- 77 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.bedroom

Beds, kids' furniture and storage for bedrooms and nurseries, modelled for Home 3D from simple shapes. Ships with the app and works offline.

### Decor & plants

- Pack id: `theovencook.decor`
- 130 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.decor

Decoration, frames, candles, vases, trays, cushions, throws and plants, modelled for Home 3D from simple shapes. Ships with the app and works offline.

### Smart-home devices

- Pack id: `theovencook.devices`
- 75 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.devices

Smart-home devices for Home 3D: sensors, switches, thermostats, doorbells, boilers, meters, alarms, smart speakers and radiators, modelled from simple shapes so they can be linked to their Home Assistant entities. Ships with the app and works offline.

### Household & building

- Pack id: `theovencook.household`
- 89 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.household

Household items, architecture (stairs, fireplaces and other building features) and pet gear, modelled for Home 3D from simple shapes. Ships with the app and works offline.

### IKEA UK range

- Pack id: `theovencook.ikea-uk`
- 547 items, release 2, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.ikea-uk

IKEA UK bestsellers in their sizes, modelled for Home 3D from simple shapes. Search by the readable name or the IKEA name. Not made or endorsed by IKEA.

### IT & network

- Pack id: `theovencook.it`
- 22 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.it

Racks, switches, routers, NAS boxes, access points and UPSs for the cupboard under the stairs or the server room, modelled for Home 3D from simple shapes. Ships with the app and works offline.

### Kitchen & bath

- Pack id: `theovencook.kitchen-bath`
- 146 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.kitchen-bath

Kitchen units, appliances and bathroom fittings, modelled for Home 3D from simple shapes. Appliances can be linked to a switch and a power sensor. Ships with the app and works offline.

### Living

- Pack id: `theovencook.living`
- 142 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.living

Sofas, seating, tables, lamps and media furniture for the living room, modelled for Home 3D from simple shapes. Ships with the app and works offline.

### Makers

- Pack id: `theovencook.makers`
- 38 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.makers

3D printers (FDM and resin), wash and cure stations and workshop kit for makers, modelled for Home 3D from simple shapes. Printers show their progress, chamber light and camera when linked to a printer entity. Ships with the app and works offline.

### Office & tech

- Pack id: `theovencook.office`
- 66 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.office

Desks, office furniture, computers, cameras and other tech, modelled for Home 3D from simple shapes. Ships with the app and works offline.

### Garden & outdoor

- Pack id: `theovencook.outdoor`
- 116 items, release 1, licence MIT
- Install URL: https://github.com/theovencook/home-3d-packs/tree/main/theovencook.outdoor

Garden furniture, outdoor items, sport kit and vehicles, modelled for Home 3D from simple shapes. Ships with the app and works offline.

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
