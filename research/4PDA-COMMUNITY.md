# 4PDA KM6 / KM6 Deluxe evidence register (Nov 2026)

Main thread: https://4pda.to/forum/index.php?showtopic=1007166

**Method:** selected historical posts and recent October–November 2026 pages reviewed. Not a line-by-line read of ~20,000 posts. Users' reports are not independently reproduced on this project's board.

| Issue | Community evidence | Relevance |
|---|---|---|
| V01 original remote voice on slimBOX | On Nov 11, Rev1 owner using slimBOX 11.47 reported voice fails with V01 but V03 works; copying older remote files unsuccessful. https://4pda.to/forum/index.php?showtopic=1007166&view=findpost&p=145956348 | P0 restore V01 mic, investigate BT audio path |
| Ethernet/Wi-Fi varies by revision | Some installs lose LAN; same Nov11 Rev1 report had 1Gbps negotiated LAN and >100Mbps 2.4GHz Wi-Fi. Official slimBOX warns about newer-revision Ethernet. https://slimboxtv.ru/mecool-km6/ | P0 identify exact board/PHY and firmware |
| Remote repeats/misses keys | Oct22 owner reported five remotes with spurious double/missing inputs over years. https://4pda.to/forum/index.php?showtopic=1007166&view=findpost&p=145631504 | Event diagnostics / wake / BT stability |
| Remote wake/disconnect | Jan-Jul reports of failure to wake after idle and spontaneous wake with UR02 remote. https://4pda.to/forum/index.php?showtopic=1007166&st=19940 | P1 power-state correctness |
| Audio ports / 5.1 | Stock-vs-port discussions mention SPDIF and analog loss; Sep26 reports fail to obtain AC3 surround on optical receiver. https://4pda.to/forum/index.php?showtopic=1007166&st=19980 | PCM, passthrough and audio HAL |
| HDR/AFR / blank display | Oct26 HDR stuck on for some TVs; other posts report AFR black-screen switching. https://4pda.to/forum/index.php?showtopic=1007166&st=20000 | HDMI EDID/HDR/AFR |
| Video freezes | Apr26 VLC pause/resume freeze/losing audio; some content-specific faults. https://4pda.to/forum/index.php?showtopic=1007166&st=19860 | Codec/player stress tests |
| Intermittent HDMI blank + audio screech | Apr26 Rev1 owner reported issue improved after slimBOX, not proven universal. https://4pda.to/forum/index.php?showtopic=1007166&st=19860 | Audio/video/thermal/PSU diagnosis |
| Power adapter / eMMC failures | Oct25–27 owner reported 'dead' unit under load due to PSU voltage sag; other posters warn flash failure can be eMMC. https://4pda.to/forum/index.php?showtopic=1007166&st=20020 | Basic power/storage diagnostics before firmware changes |
| User complaints after 2025 stock updates | Oct9 report of new remote disconnections after installing 2025 stock package. https://4pda.to/forum/index.php?showtopic=1007166&st=20000 | Regression testing |
| XCPE discussion | Nov3–11 users share package findings and debate ADB removal; model-specific infection on this unit NOT independently proved. https://4pda.to/forum/index.php?showtopic=1007166&st=20060 | P0 secure provenance |

Other useful threads: slimBOX https://4pda.to/forum/index.php?showtopic=993324; relevant Apr 2026 Rev1 V01 mic report https://4pda.to/forum/index.php?showtopic=993324&st=21620.

**Do not** present certification, Widevine L1, Dolby Vision or paid streaming compatibility as a guaranteed software feature.