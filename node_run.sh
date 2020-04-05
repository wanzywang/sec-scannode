#!/bin/sh
git pull https://e.coding.net/davytitan/xn-scannode.git
pip install -r ./requirements.txt -i https://pypi.doubanio.com/simple/
touch package.ver
# echo "1.0.0" >> package.ver
# nohup crond >/dev/null 2>&1 &
python -u scan.py
