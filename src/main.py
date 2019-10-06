import time
from waqi_pipeline_dag import run_dag

if __name__ == "__main__":
    t0 = time.time()
    run_dag()
    t1 = time.time()
    print(t1 - t0)
