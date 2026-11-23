# VBoy Color for Steam Frame

Virtual Boy games in color and in real 3D, running natively on the Steam Frame.
This is a fork of [yuk27/VBoyColor](https://github.com/yuk27/VBoyColor), with Frame support and fixes added.

![Wario Land in VBoy Color: the original red on the left, colored on the right](images/wario-land.png)

## Features

- Runs on the Frame itself, with no PC streaming
- Real 3D: each eye gets its own picture
- Controls laid out for the Frame's controllers
- Adds itself to your Steam library, with artwork
- Less GPU work per frame than before
- Wario Land's level-exit room no longer shows black boxes
- Everything else from VBoy Color: color packs, save states, RetroAchievements

## How it works

- The emulator runs on the Frame. It draws a separate picture for each eye through SteamVR.
- Built-in color packs and color modes paint the games.
- You supply the games. Nothing is streamed from a PC.

## Requirements

- A Steam Frame.
- Your own Virtual Boy games as `.vb` files. Unzip any `.zip` downloads first.
- A computer with Git and Docker to build it. On an Intel or AMD PC, Docker also needs ARM64 emulation.

No games are included. Use only ROMs you made from cartridges you own.

## Install

1. Build the Frame package on your computer:

   ```sh
   git clone --recurse-submodules -b frame https://github.com/simplysanatori/VBoyColor.git
   cd VBoyColor
   DOCKER_DEFAULT_PLATFORM=linux/arm64 ./tools/steam_frame/build-linux-arm64.sh
   ```

2. Copy the folder `build-frame/VBoyColorVR-linux-arm64/` to the Frame as `~/Games/VBoyColor`.
3. Put your `.vb` files in its `roms` folder.
4. On the Frame, add it to Steam. Steam closes for a moment and starts again.

   ```sh
   cd ~/Games/VBoyColor
   ./install-to-steam.py
   ```

Full build notes are in [docs/STEAM_FRAME.md](docs/STEAM_FRAME.md#building-it-yourself).

## First run

1. Start **VBoy Color** from your Steam library.
2. Point at a game and pull the trigger.
3. Hold Menu for half a second to open the menu. **Settings → Color mode** changes the colors.

## Controls

| Virtual Boy | Steam Frame |
|---|---|
| Left D-pad | left stick or D-pad |
| Right D-pad | right stick |
| A / B | A / B |
| L / R | triggers or bumpers |
| Start | tap Menu (or Y) |
| Select | View (or X) |
| VBoy Color's menu | hold Menu for half a second |
| Pick in the menu | point and pull the trigger |

Remap anything in **Settings → Button mapping**. Every control is in the [user guide](docs/USER_GUIDE.md#controls).

## Update

Pull and rebuild, then copy the new folder over the old one. Your games and saves stay.

```sh
cd VBoyColor
git pull --recurse-submodules
DOCKER_DEFAULT_PLATFORM=linux/arm64 ./tools/steam_frame/build-linux-arm64.sh
```

## Uninstall

On the Frame, take it out of Steam, then delete the folder:

```sh
cd ~/Games/VBoyColor
./install-to-steam.py --uninstall
```

## Troubleshooting

- **No games in the library:** put unzipped `.vb` files in the `roms` folder.
- **Controllers do nothing:** start it from the Steam library, not a terminal.
- **Scrolling stutters:** set VBoy Color to 100 Hz in SteamVR's per-app settings.
- **The menu won't open:** hold Menu for half a second, or hold the left stick click for a second.
- **A `GLIBC` error on the Frame:** rebuild with the Docker script above.

More fixes are in [docs/STEAM_FRAME.md](docs/STEAM_FRAME.md#checks-and-common-problems).

## More

- [User guide](docs/USER_GUIDE.md): every feature, all platforms, RetroArch and the full controls
- [Steam Frame details](docs/STEAM_FRAME.md)
- [Color packs](docs/COLOR_PACKS.md)
- [Building](docs/BUILDING.md)
- [AGENTS.md](AGENTS.md): for developers and AI agents

## Support

Support VBoy Color's author: https://ko-fi.com/yuk27 or https://github.com/sponsors/yuk27

Support this Frame fork: https://ko-fi.com/sana748653

## Credits

- [VBoy Color](https://github.com/yuk27/VBoyColor) by yuk27: the emulator, color modes and color packs.
- astromaddie: the Steam Frame port ([#15](https://github.com/yuk27/VBoyColor/pull/15), [#16](https://github.com/yuk27/VBoyColor/pull/16)).
- [VirtualBoyGo](https://github.com/CidVonHighwind/VirtualBoyGo) by CidVonHighwind: the VR app VBoy Color started from.
- [Beetle VB](https://github.com/libretro/beetle-vb-libretro): the emulator core.

The full list is in [AGENTS.md](AGENTS.md#credits) and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

VBoy Color is an independent fan project, not affiliated with Nintendo or Meta. "Virtual Boy" is a trademark of Nintendo.

## Licence

GNU General Public License v3.0 ([LICENSE](LICENSE)).

## How this was made

I started this project and used AI (Claude) to speed up development. I write, review and fix code by hand all the way through, keep the AI's work checked and reined in, and aim to keep the port as lightweight as possible. I test it on my own Steam Frame. This fork builds on yuk27's VBoy Color and astromaddie's Frame port.
