docker cp in.csv olx://usr/src/app/in.csv
docker exec -ti olx sh -c "pgrep chrome | xargs kill -9"
docker exec -ti olx python3 main.py
docker cp olx://usr/src/app/out.csv out.csv 
