
roomStr=$1

cd ..

python3 pairs.py --env Room${roomStr}
python3 binning_stats_pdata.py ${roomStr}
rm pairs_room${roomStr}_large.csv
cd scripts
# python3 Check_Removed_Bins_Copy.py ${roomStr} 5 
# python3 Check_Removed_Bins_Copy.py ${roomStr} 10
# python3 Check_Removed_Bins_Copy.py ${roomStr} 20
