import time
import numpy as np
from typing import List, Optional

import threading
import pandas as pd
import requests
import plotly.express as px

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
    this function finds the next largest prime number and then    The input is data in the form of a list and the output is a function"""
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
    the input is data in the form of a list and the output is a funciton."""
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?
    """
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://127.0.0.1:5000' # TODO: Change this to the IP address of your server

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        data1 = None
        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            response=requests.post(f"{offload_url}/process1", json=data)
            data1 = response.json()
        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        # TODO: Implement this case
        data2=None
        def offload_process2(data):
            nonlocal data2
            r_2=requests.post("http://offload_url/process2", json=data)
            data2=response.json()
        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1=process1(data)
        thread.join()
        

    elif offload == 'both':
        # TODO: Implement this case
        data1 = None
        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            r=requests.post("http://offload_url/process1", json=data)
            data1 = response.json()
        data2=None
        def offload_process2(data):
            nonlocal data2
            r_2=requests.post("http://offload_url/process2", json=data)
            data2=response.json()
        thread1=threading.Thread(target=offload_process1, args=(data,))
        thread2=threading.Thread(target=offload_process2, args=(data,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        

    ans = final_process(data1, data2)
    return ans 

def main():
    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference
    
    rows=[]
    samples=5
    modes=[None, 'process1','process2','both']

    for mode in modes:
        times=[]
        for i in range(samples):
            start=time.time()
            run(mode)
            end =time.time()
            times.append(end - start)
            print(f"Offloading {mode} - sample {i+1}: {times[-1]:.2f}")
        rows.append([str(mode), np.mean(times), np.std(times)])
    df3=pd.DataFrame(rows, columns=['times', 'mean', 'std'])



    # TODO: Plot makespans (total execution time) as a bar chart with error bars
    # Make sure to include a title and x and y labels
    
    plt.bar(modes,df3)   
    plt.title('lab 10 plot')
    plt.xlabel('modes')
    plt.ylabel('times')

    # TODO: save plot to "makespan.png"
    plt.savefig('makespan.png"')


    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()