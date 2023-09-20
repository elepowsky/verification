# Run all scripts in order to move pbm and create all necessary things
# Current directory:
# ~/Documents/Github/Verification/WheeledRobotSimulations/

# echo $1
# echo "$1"

roomNumber="$1"
roomStr="Room$1"
# echo "Room$1"
# echo ${roomStr}


echo "Copying files to blender folder"
cp pybullet/Rooms/${roomStr}.pbm assets/blender/ 

echo "..."
echo "Running blender"
cd assets/blender 
blender --background --python pbm_to_obj.py

# move from blender to blender_done
echo "..."
echo "Moving things from blender to blender_done"
sleep 5
cd ..
mv blender/Room* blender_done/

echo "..."
echo "Making directory in Rooms/todo folder"
mkdir Rooms/todo/${roomStr}

echo "..."
echo "Moving obj and mtl files into todo/"
cp blender_done/${roomStr}.obj Rooms/todo/${roomStr}
cp blender_done/${roomStr}.mtl Rooms/todo/${roomStr}

echo "Building urdfs"
cd Rooms/
python3 build_room_urdfs.py

echo "Moving to done/ folder"
sleep 5
mv todo/Room* done/

cd ../../pybullet/

cp configuration/scenarios/Room6.yml configuration/scenarios/${roomStr}.yml
mkdir models/scenes/${roomStr}
cp ../assets/Rooms/done/${roomStr}.urdf models/scenes/${roomStr}/
cp ../assets/blender_done/${roomStr}.pbm models/scenes/${roomStr}/

mkdir models/scenes/${roomStr}/${roomStr}
cp ../assets/Rooms/done/${roomStr}/Room*.obj models/scenes/${roomStr}/${roomStr}/

echo "Rearranging .obj files in models/scenes/${roomStr}/${roomStr}"
cp models/scenes/${roomStr}/${roomStr}/${roomStr}_vhacd.obj models/scenes/${roomStr}/${roomStr}/${roomStr}_old.obj
cp models/scenes/${roomStr}/${roomStr}/${roomStr}.obj models/scenes/${roomStr}/${roomStr}/${roomStr}_vhacd.obj

echo "Moving back to WheeledRobotSimulations directory"
cd ..

echo "Finished messy stuff"

echo "Need to update the yaml file at pybullet/configurations/scenarios/${roomStr}.yml"

