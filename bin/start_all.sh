echo "Conductor"
PYTHONPATH=`pwd` python crawler/conductor.py --db_uris influx://localhost:8086/crawler --gearman localhost:4730 & echo $! > /tmp/sc
echo "Scheduler"
PYTHONPATH=`pwd` python crawler/scheduler.py --db_uris influx://localhost:8086/crawler --gearman localhost:4730 & echo $! >> /tmp/sc
echo "Worker"
PYTHONPATH=`pwd` python crawler/worker.py --gearman localhost:4730 & echo $! >> /tmp/sc
echo "API"
PYTHONPATH=`pwd` python crawler/api.py 0.0.0.0:8080 --gearman localhost:4730 & echo $! >> /tmp/sc
