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
	--package-version="0.6.4"

sed -i \
	-e "s/FIRST AUTHOR <EMAIL@ADDRESS>, YEAR./Foldex, $(date +%Y)./" \
	-e "s/Language: /Language: EDIT_LANG_HERE/" \
	-e "s/SOME DESCRIPTIVE TITLE./AdwSteamGtk Pot/" \
	-e "s/YEAR THE PACKAGE'S COPYRIGHT HOLDER/$(date +%Y) Foldex/" \
	-e "s/charset=CHARSET/charset=UTF-8/" \
	-e "s/same license as the AdwSteamGtk package./GNU GPLv3 license./" \
	"$OUT_FILE"
