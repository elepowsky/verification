roomNum=$1
stepNum=$2
cd ..

python3 pairs_big_altdata.py --env Room${roomNum} --maxstep ${stepNum} --parts 1 --iterations 10000000 
python3 binning_stats_altdata.py ${roomNum} ${stepNum}
rm AltData/Room${roomNum}/maxstep${stepNum}_part1of1.csv

cd scripts