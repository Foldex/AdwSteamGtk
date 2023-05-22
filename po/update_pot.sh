#!/bin/bash
PO_DIR=$(dirname "$(realpath "$0")")
OUT_FILE="$PO_DIR/AdwSteamGtk.pot"

cd "$PO_DIR/.." || exit

xgettext \
	-f "$PO_DIR"/POTFILES \
	-o "$OUT_FILE" \
	--add-comments=Translators \
	--from-code=UTF-8 \
	--keyword=C_:1c,2 \
	--keyword=_ \
	--package-name="AdwSteamGtk" \
	--package-version="0.6.0"

