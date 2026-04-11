from redis import Redis
from rq import Queue
import os
from dotenv import load_dotenv

load_dotenv()

redis_conn = Redis.from_url(os.environ["REDIS_URL"])

queue = Queue(connection=redis_conn)


"""
Note: We are intentionally using rq version 1.15.1 reason being with the latest version of rq because triggers 
multiprocessing (fork) internally and windows doesn’t support fork hence at the intial only when we do
from rq import Queue our app crasses there for We are using specific version which doesn't forks.
In the linux or docker envirnoment latest version works efficently.


FLOW: We first create a queue connection, redis provides a queue to us now we use rq that takes
task from the queue and then run it using multiprocessing and workers 

To run rq workers simply run the command rq worker but since I am using an online redis here there fore 
i need to run using this complete command provding the url of queue(redis):
rq worker --url rediss://default:gQAAAAAAAURhAAIncDEzODMzZTU3MDIyOTM0ZDY5YjYxMDk2ODYxYjRkODE5NHAxODMwNDE@golden-woodcock-83041.upstash.io:6379 --worker-class rq.worker.SimpleWorker

If you are on docker or local runing then simple rq worker will work since it looks for default
localhost connection of redis i.e redis runing in the docker


currently this code is not woring properly rq is not able to close the task since it is not
well supported for windwos env.
"""