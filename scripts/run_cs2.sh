#!/bin/bash

set -eux

function ensure_steamcmd_is_configured {
    # make sure steamcmd is updated
    /usr/games/steamcmd +quit
    ln ~/.local/share/Steam/steamcmd/linux64/steamclient.so ~/.steam/sdk64/ 
}

function ensure_cs_is_updated {
    /usr/games/steamcmd +force_install_dir ~/cs2 +login "${STEAM_USERNAME}" "${STEAM_PASSWORD}" +app_update 730 validate +quit
}

function run {
    screen -S server ./cs2/game/bin/linuxsteamrt64/cs2 -dedicated +map de_dust2 -usercon -console
}

ensure_cs_is_updated
run

