# usage: sh commands.sh -n ${NUMBER}

while getopts n: flag
do
    case "${flag}" in
        n) envnum=${OPTARG};;
    esac
done


cp ../../../assets/Rooms/done/Room${envnum}/Room${envnum}.obj Room${envnum}/Room${envnum}/
cp ../../../assets/Rooms/done/Room${envnum}/Room${envnum}_vhacd.obj Room${envnum}/Room${envnum}/
