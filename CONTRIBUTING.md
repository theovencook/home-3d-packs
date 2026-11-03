# Contributing

## Get your pack listed

Home 3D's Library has a **Browse packs** tab. It shows the packs listed in `index.json` in this repository: ours,
and community packs added by pull request. Listing a pack means anyone can find it and install it with one click;
Home Assistant then downloads it from your repository, not from here.

### What a listed pack needs

- **A public GitHub repository** with the pack in a folder of its own (or at the repository root): a `pack.json`
  and one JSON file per item, as described in Home 3D's
  [`docs/packs.md`](https://github.com/theovencook/home-3d/blob/main/docs/packs.md).
- **The MIT licence.** `"licence": "MIT"` in `pack.json`, and the MIT licence text in a `LICENSE` file in the pack
  folder or at the top of the repository.
- **Data only.** A pack folder holds `pack.json`, item `.json` files and at most a README, LICENSE or CHANGELOG.
  No scripts, pictures or other files, and no links in any text: Home 3D refuses them on install, and so does the
  check here.
- **A unique id.** The pack id is `publisher.pack`, for example `jane.garden-furniture`. It must not be used by
  another listed pack, and the publisher `theovencook` is ours.
- **It passes the pack check.** Run Home 3D's checker on your folder before you open the pull request:

  ```
  git clone https://github.com/theovencook/home-3d
  pip install voluptuous
  python home-3d/tools/fp3dpack.py validate path/to/your/pack-folder
  ```

### Open the pull request

1. Add your pack to `community.json`: the URL of the pack folder, and optionally the item whose picture should
   stand for the pack.

   ```json
   {
    "packs": [
     {"url": "https://github.com/jane/home-3d-garden/tree/main/jane.garden-furniture", "thumbnail": "bench"}
    ]
   }
   ```

2. Build the index with your pack in it (this fetches the community packs from GitHub and checks them):

   ```
   python tools/build_index.py build . --home3d path/to/home-3d --fetch
   ```

3. Commit `community.json` and `index.json` and open the pull request. CI runs
   `python tools/build_index.py check` on every listed pack; it must pass before we merge.

### After it is listed

- Raise `release` in your `pack.json` whenever you change the pack. Home 3D's update check compares releases, so
  installs pick up the new release from your repository; the index shows the release it last saw (we rebuild it
  now and then, and a pull request that rebuilds it is welcome).
- The weekly CI run checks every listed pack again. A pack that stops passing (for example a file that is not
  data) is taken off the list until it is fixed.
- To be taken off the list, open a pull request that removes your entry, or an issue.

## Our packs

The `theovencook.*` folders are generated from the packs that ship with Home 3D (`tools/publish_packs.py` in the
Home 3D repository, which also rebuilds `index.json`). Send changes to those packs to Home 3D rather than here.
