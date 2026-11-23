"""Leave a tile uncolored where one room's map shows it - without the pack's paintings.

A pack colors a tile the same everywhere (unless a painting gave a map cell, palette or layer its
own colors). Some games use one tile for two things: Virtual Boy Wario Land's plain solid tile is
dark in most rooms, so the pack paints it black, but one room's side walls are made of it - and
they came out as black boxes (issue 14). This plays a movie up to a stretch of frames where that
room shows, finds the map cells that show the given tiles there (on the given layers), and gives
each one a cell variant that leaves the tile uncolored ("keep", like a painting's magenta): there,
it takes the Multicolor palette's colors like the room's other unpainted tiles. Everything else in
the pack stays as it was.

    python3 keepcells.py ROM.vb MOVIE.bk2 PACK.vbcp OUT.vbcp FIRST-LAST[,FIRST-LAST...] --tiles d58f91f5,014c9985 [--worlds 28,29]

(Every visit to the room is worth listing: a room scrolled differently shows other cells.)

Map cells are the VIP's BG map positions, so another room that loads the same tile at the same
cell in the same palette gets it too - check with a whole-run comparison (both packs) before using
the result.
"""
import argparse
import ctypes as C
import os
import sys

os.environ.setdefault("VBP_OPTS", "vb_opposite_directions=enabled,vb_cpu_emulation=accurate")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402

from vbp import VB, lib, capture  # noqa: E402
from tas import movie_frames  # noqa: E402

lib.vbp_pack_set_cell.argtypes = [C.c_int, C.c_int, C.c_uint32, C.c_uint64, C.c_uint64, C.c_void_p]
U = np.uint64


def main():
    p = argparse.ArgumentParser()
    p.add_argument("rom")
    p.add_argument("movie")
    p.add_argument("pack")
    p.add_argument("out")
    p.add_argument("frames", help="the room's frames: FIRST-LAST, comma-separated stretches")
    p.add_argument("--tiles", required=True, help="tile hashes (hex), comma-separated")
    p.add_argument("--worlds", default="", help="only these layers (comma-separated); default all")
    a = p.parse_args()
    tiles = [int(h, 16) for h in a.tiles.split(",")]
    worlds = [int(w) for w in a.worlds.split(",")] if a.worlds else list(range(32))
    stretches = [tuple(int(x) for x in r.split("-")) for r in a.frames.split(",")]
    last = max(b for _, b in stretches)

    vb = VB(a.rom, pack=a.pack)
    cells = set()
    for i, m in enumerate(movie_frames(a.movie), 1):
        lib.vbp_run(m, 1)
        if i > last:
            break
        if not any(f <= i <= l for f, l in stretches):
            continue
        vb.render(True)  # (captures read the frame the renderer just painted)
        for eye in (0, 1):
            t, c, _ = capture(eye)
            h = (t & U(0xFFFFFFFF)).astype(np.int64)
            sel = (np.isin(h, tiles) & np.isin(((t >> U(43)) & U(31)).astype(int), worlds) & (((c >> 31) & 1) == 1) &
                   (((t >> U(40)) & U(1)) == 0))
            cells |= set(zip((c[sel] & 0xFFFF).tolist(), ((t[sel] >> U(38)) & U(3)).tolist(), h[sel].tolist()))

    rgb = np.zeros(64 * 3, np.uint8)
    for cell, palette, h in sorted(cells):
        lib.vbp_pack_set_cell(cell, palette, h, 0, 0xFFFFFFFFFFFFFFFF, rgb.ctypes.data)
    size = lib.vbp_paint_bytes(None)
    buf = (C.c_uint8 * size)()
    lib.vbp_paint_bytes(buf)
    original = open(a.pack, "rb").read()
    data = bytes(buf)
    # (the ROM footer - "VBGOROM1", CRC, size - when Serialize didn't write one)
    if original[-16:-8] == b"VBGOROM1" and data[-16:-8] != b"VBGOROM1":
        data += original[-16:]
    open(a.out, "wb").write(data)
    print(f"{len(cells)} cells left uncolored ({', '.join(sorted({f'{h:08x}' for _, _, h in cells}))}); "
          f"{len(original)} -> {len(data)} bytes, {a.out}")


if __name__ == "__main__":
    main()
