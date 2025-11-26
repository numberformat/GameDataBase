"""(c) 2025 Neeraj Verma — MIT License. https://noami.us"""

import subprocess

FILES = [
    "arcade_capcom.csv",
    "arcade_irem.csv",
    "arcade_sega.csv",
    "arcade_snk.csv",
    "arcade_taito.csv",

    "console_nec_cdrom2.csv",
    "console_nec_pcengine_turbografx_supergrafx.csv",
    "console_nec_pcfx.csv",

    "console_nintendo_64dd.csv",
    "console_nintendo_bandai_sufamiturbo.csv",
    "console_nintendo_famicom_nes.csv",
    "console_nintendo_famicomdisksystem.csv",
    "console_nintendo_gameboy.csv",
    "console_nintendo_nintendo64.csv",
    "console_nintendo_satellaview.csv",
    "console_nintendo_superfamicom_snes.csv",
    "console_nintendo_virtualboy.csv",

    "console_pioneer_laseractive.csv",

    "console_sega_gamegear.csv",
    "console_sega_markIII_mastersystem.csv",
    "console_sega_megacd_segacd.csv",
    "console_sega_megadrive_genesis.csv",
    "console_sega_saturn.csv",
    "console_sega_sg1000_sc3000_othellomultivision.csv",
    "console_sega_super32x.csv",

    "console_snk_neogeopocket_neogeopocketcolor.csv",
]

for f in FILES:
    try:
        subprocess.run(
            ["python", "scripts/normalize_to_3nf.py", "--file", f],
            check=True
        )
    except Exception as e:
        print(f"⚠️ Skipped {f} due to error: {e}")
