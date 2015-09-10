#!/bin/sh
# @Author: Chengzhe Yan
# @Date:   2015-09-10 18:41:20
# @Last Modified by:   Chengzhe Yan
# @Last Modified time: 2015-09-10 21:20:50


ROOT="/usr/local/collie/"
CFGOAT="goat.json"
CFMASTER="master.json"
PGOAT="cgoat.py"
PMASTER="cmaster.py"
TARGET="/etc/init.d/collie"

rm -r $ROOT
rm $TARGET
mkdir $ROOT
cp $CFGOAT $CFMASTER $PMASTER $PGOAT $ROOT
chmod +x $ROOT$PGOAT
chmod +x $ROOT$PMASTER

echo 'ROOT="/usr/local/collie/"' >> $TARGET
if [ "$1" = "master" ]
then
	echo 'APP=$ROOT"cmaster.py"' >> $TARGET
	echo 'CF=$ROOT"master.json"' >> $TARGET
else
	echo 'APP=$ROOT"cgoat.py"' >> $TARGET
	echo 'CF=$ROOT"goat.json"' >> $TARGET
fi
cat collie >> $TARGET
chmod +x $TARGET
