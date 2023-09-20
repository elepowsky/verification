roomNum=$1
cd ..

cp AltData/Room${roomNum}/img_reduced_bins* BadBins/Room${roomNum}/
cp AltData/Room${roomNum}/badIdx_bins* BadBins/Room${roomNum}/

cd scripts