#!/bin/sh
#####
# get_pitches.sh
#  This loads pitch by pitch data from mlb.com
#####
readonly GAMEDAY_HOST=http://www.mlb.com
readonly GAMEDAY_ROOT=/gdcross/components/game/mlb/year_2013/
readonly DEST_PATH=../data/pitches

if [ ! -d "$DEST_PATH" ]; then
  mkdir $DEST_PATH
fi

# -e robots=off : 
# -r : recursive download
# -np : don't follow parent links
# -l 5 : five levels of recursion (month, day, game ID, inning, inning_all.xml)
# -R index.html : don't keep index files around
# -A inning_all.xml : keep inning_all.xml only
# -nH : don't create host directory (../data/www.mlb.com/ etc...)
# --cut-dirs=4 : trim four levels from the local folder structure so it starts at year_...
# -w 0.1 : wait 100ms between requests so we don't bog down the server and get ourselves banned
# --no-verbose : inside voices please
wget -e robots=off -r -np -l 5 -R index.html -A inning_all.xml -nH --cut-dirs=4 -w 0.1 \
  -X ${GAMEDAY_ROOT}batters \
  -X ${GAMEDAY_ROOT}media \
  -X ${GAMEDAY_ROOT}mobile \
  -X ${GAMEDAY_ROOT}pitchers \
  -X ${GAMEDAY_ROOT}*/*/batters \
  -X ${GAMEDAY_ROOT}*/*/media \
  -X ${GAMEDAY_ROOT}*/*/pitchers \
  -X ${GAMEDAY_ROOT}*/*/pitching_staff \
  -X ${GAMEDAY_ROOT}*/*/pitching_staff \
  -X ${GAMEDAY_ROOT}*/*/*/batters \
  -X ${GAMEDAY_ROOT}*/*/*/media \
  -X ${GAMEDAY_ROOT}*/*/*/notifications \
  -X ${GAMEDAY_ROOT}*/*/*/onbase \
  -X ${GAMEDAY_ROOT}*/*/*/pitchers \
  -X ${GAMEDAY_ROOT}*/*/*/premium \
  --no-verbose $GAMEDAY_HOST$GAMEDAY_ROOT -P $DEST_PATH