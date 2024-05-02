import multiprocessing
from home import app as app0
from soil_classification import app as app1
from weed_detection import app as app2
from crop_recommendation import app as app3
from about import app as app4
from contact import app as app5
from fertilizer_recommendation import app as app6
from disease_identification import app as app7
from livestock_disease import app as app8


def run_app0():
    app0.run(port=5000)

def run_app1():
    app1.run(port=5001)

def run_app2():
    app2.run(port=5002)

def run_app3():
    app3.run(port=5003)

def run_app4():
    app4.run(port=5004)

def run_app5():
    app5.run(port=5005)

def run_app6():
    app6.run(port=5006)

def run_app7():
    app7.run(port=5007)

def run_app8():
    app8.run(port=5008)

if __name__ == '__main__':
    p0 = multiprocessing.Process(target=run_app0)
    p1 = multiprocessing.Process(target=run_app1)
    p2 = multiprocessing.Process(target=run_app2)
    p3 = multiprocessing.Process(target=run_app3)
    p4 = multiprocessing.Process(target=run_app4)
    p5 = multiprocessing.Process(target=run_app5)
    p6 = multiprocessing.Process(target=run_app6)
    p7 = multiprocessing.Process(target=run_app7)
    p8 = multiprocessing.Process(target=run_app8)

    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()

    p0.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()