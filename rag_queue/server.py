from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query
from .queues.worker import process_querry
from .client.rq_client import queue

app=FastAPI()

@app.get('/')
def root():
    return {"status": 'Server is up and running'}

@app.post('/chat')
def chat(query: str= Query(..., description="The chat query of user")):
    job=queue.enqueue(process_querry,query)
    return {"status":"queued", "job_id":job.id}


@app.get('/job-status')
def get_result(job_id: str=Query(...,description="JOB ID")):
    job=queue.fetch_job(job_id=job_id)
    result=job.return_value()

    return {"result":result}