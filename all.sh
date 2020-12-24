AOC="AoC-2020"

rm "$AOC.zip" all.txt

python3.9 all.py > all.txt

zip "$AOC.zip" */* all.py LICENSE.md all.txt -x all.sh *.class
