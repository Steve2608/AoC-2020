AOC="AoC-2020"
rm "$AOC.zip"

zip "$AOC.zip" */* all.py LICENSE.md all.txt -x all.sh *.class
