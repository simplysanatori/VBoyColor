# AGENTS.md

This file holds the technical detail moved out of the README, for developers and AI agents.

## This fork

This is a Steam Frame fork of [yuk27/VBoyColor](https://github.com/yuk27/VBoyColor).
The `frame` branch brings in astromaddie's Steam Frame support
([#15](https://github.com/yuk27/VBoyColor/pull/15)) and menu fix
([#16](https://github.com/yuk27/VBoyColor/pull/16)): native Linux ARM64
packaging, Frame controller bindings, a SteamVR projection-layer path so each
eye gets its own Virtual Boy picture, and a Steam library installer with
artwork. No streaming PC or Android compatibility layer is needed on the Frame.

Start with [the Frame guide](docs/STEAM_FRAME.md) for installation, controls and a
fresh build. [BUILDING.md](docs/BUILDING.md) covers the other targets. The upstream
project's features and downloads are in [docs/USER_GUIDE.md](docs/USER_GUIDE.md); links to
`yuk27/VBoyColor/releases` are upstream releases, not releases made by this fork.

The `frame` branch is upstream `main` plus astromaddie's two pull requests (merged
with their authorship kept) and these changes:

- **Updater** (`core/io/Updater.cpp`): picks the release package for the machine's
  CPU, `-linux-arm64` on ARM64 and `-linux-x64` elsewhere. Before, any `-linux-`
  tarball matched, so an ARM64 machine could get the x64 one.
- **Black eye buffers** (`OpenXrApp::CreateSwapchains`, `RenderFrame`): the
  projection layer under the screen and menu is one 16x16 swapchain
  (`XR_SWAPCHAIN_CREATE_STATIC_IMAGE_BIT` where the runtime has it, else an
  ordinary one), cleared once and shown to both eyes. Upstream cleared two
  full-size eye swapchains every refresh, each followed by `vkQueueWaitIdle`.
- **Screen layer switch**: `VBC_SCREEN_AS_PROJECTION=0/1` picks per-eye quads or
  PR 15's projection layer. The default stays the projection layer on SteamVR.
  The per-eye quads are worth an A/B on the Frame: Azahar for Frame's per-eye
  quads do show 3D there.
- **Timing log**: `VBC_FRAME_TIMING=1` logs, every 5 s, the refresh rate, the
  app's work per refresh (average and worst) and the time in `xrWaitFrame`.
  See [docs/STEAM_FRAME.md](docs/STEAM_FRAME.md#testing-switches).
- **Command line**: `--rom <file>` for both apps (`OpenXrApp::PlayRom` in VR),
  `--fullscreen` and `--windowed` for the window app, and `--help`.
- **Frame Menu button** (`XrInput::Sync`, `OpenXrApp::RenderFrame`): with the
  Frame's interaction profile active, Menu is reported on its own. A tap sends
  the gamepad's Start (`EmuButton_Enter`, the default Start binding) for six
  refreshes. Holding it for 500 ms opens the menu, and a tap closes an open menu.
  Quest Touch controllers are unchanged.
- **Wario Land, issue 14**: the level-exit room's side walls use a solid tile
  (and two others) that the pack paints black or purple elsewhere. The room's
  258 map cells that show them (its whole map: BG segments 2 and 3, 129 cells
  each) are cell variants with every pixel "keep" (uncolored). The tool is
  `tools/harness/keepcells.py`, using `TileColorPack::SetCellTile` and the
  harness's `vbp_pack_set_cell`. It was checked over TASVideos 4560M: the room's
  10 visits are fixed in both eyes, and no other frame changes.

Building on a current rolling distro can fail on the pinned dependencies (the
Vulkan-Headers C++ module, old FreeType CMake minimums). An Ubuntu 22.04
container, as in `tools/steam_frame/`, works. Build `VBoyColorVR` and
`VBoyColor` one after the other: both copy `colorpacks/` after linking, and in
one parallel build the two copies can collide.

## Building

See [docs/BUILDING.md](docs/BUILDING.md) - the Windows and Linux apps, PC VR,
the Android app (Quest, phones and TVs) and the RetroArch core, all from one
CMake project. GitHub Actions builds app changes on pushes and pull requests;
docs-only changes are skipped. The workflow can also be run manually.

## Steam Frame notes

[docs/STEAM_FRAME.md](docs/STEAM_FRAME.md) covers the Frame build, the
packaging, the projection layer, the controller profile and the testing switches.

## Credits

- **[VirtualBoyGo](https://github.com/CidVonHighwind/VirtualBoyGo)** by
  CidVonHighwind - VBoy Color started as a fork of its OpenXR + Vulkan
  rework. The VR app, renderer, menu, save states and button mapping come
  from there. Thank you for building it and sharing it.
- **[Beetle VB](https://github.com/libretro/beetle-vb-libretro)** - libretro's
  fork of Mednafen's Virtual Boy emulation, the emulator core. It is compiled
  untouched, apart from a generated hook in its video code that reports which
  tile drew each pixel (`cmake/PatchBeetleVip.cmake`).
- **[Red Viper](https://github.com/skyfloogle/red-viper)** - the Virtual Boy
  emulator for the 3DS, for the idea of coloring the four shades (its
  multicolour mode). No Red Viper code is used.
- **[RetroAchievements](https://retroachievements.org)** and its
  [rcheevos](https://github.com/RetroAchievements/rcheevos) library (MIT) -
  the achievements, made by its community for every Virtual Boy game it covers.
- **[Super Bit Shader](https://github.com/AshleyPikachu/Super-Bit-Shader)** by
  Ashley the Pikachu - RetroArch shaders that color the Virtual Boy, the Game
  Boy and the other monochrome handhelds, with side-by-side 3D for the
  Virtual Boy in VR. Thank you for keeping the colored Virtual Boy scene
  going with your great work. Super Bit Shader implementation is WIP.
- The libraries and fonts listed in
  [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

## How this was made

I started this project and used AI (Claude) to speed up development. I write, review and fix code by hand all the way through, keep the AI's work checked and reined in, and aim to keep the port as lightweight as possible. I test it on my own Steam Frame. This fork builds on yuk27's VBoy Color and astromaddie's Frame port.
