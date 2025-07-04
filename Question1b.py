try:
  # Dask parallel processing
    n_processors = [10, 20]
    n_processors_time = {}

    for processor in n_processors:
        print(f"Starting computation for {processor} processors")
        client = Client(n_workers=processor)

        start = time.time()
        nationalOnly = df2[df2["Level"] == "National"]
      #dropping the uneeccesray columns, just to focus on the three that we need.
        nationalOnly = nationalOnly[["Date", "Number of Trips 10-25", "Number of Trips 50-100"]]


        firstSet = nationalOnly[nationalOnly["Number of Trips 10-25"] > 10000000]
        secondSet = nationalOnly[nationalOnly["Number of Trips 50-100"] > 10000000]
        thirdSet = nationalOnly[(nationalOnly["Number of Trips 50-100"]>10000000) & (nationalOnly["Number of Trips 10-25"] > 10000000)]
        fourthSet = nationalOnly[(nationalOnly["Number of Trips 50-100"]<10000000) & (nationalOnly["Number of Trips 10-25"] > 10000000)]


        set1_pandas = firstSet.compute()
        set2_pandas = secondSet.compute()
        set3_pandas = thirdSet.compute()
        set4_pandas = fourthSet.compute()

        print(len(set1_pandas))
        print(len(set2_pandas))
        print(len(set3_pandas))
        print(len(set4_pandas))

        plt.scatter(set3_pandas["Date"], set3_pandas["Number of Trips 50-100"], color="blue", alpha=0.5)
        #set title
        plt.title("Set 3: Both true")
        plt.xlabel("Date")
        plt.ylabel("Number of Trips 50-100 & Number of Trips 10-25")
        plt.show()

    

        elapsed_time = time.time() - start
        n_processors_time[processor] = elapsed_time
        print(f"Time with {processor} processors: {elapsed_time:.2f} seconds")
        client.close()

    print("Dask timing results:", n_processors_time)

    # Multiprocessing
    times = []
    for numProcessors in [1, 2, 4, 8, 10, 12, 16, 20]:
      print(f"Running multiprocessing with {numProcessors} processors...")
      start_time = time.time()

      pool = multiprocessing.Pool(processes=numProcessors)
      #results = pool.map(process_data, partial_functions)  # Assumes process_data & partial_functions are defined
      pool.close()
      pool.join()

      elapsed = time.time() - start_time
      times.append(elapsed)
      print(f"Total Execution time with {numProcessors} processors: {elapsed:.2f} seconds")
    
    print("Multiprocessing timing results:", times)
    plt.figure(figsize=(10, 6))
    plt.plot(processor_counts, times, marker='o', linestyle='-', color='green')
    plt.title("Multiprocessing Execution Time vs Number of Processors")
    plt.xlabel("Number of Processors")
    plt.ylabel("Execution Time (seconds)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
except Exception as e:
    print("Dam it -", e)
