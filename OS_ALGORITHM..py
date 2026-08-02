from collections import deque# required for implementing the ready queue in Round Robin scheduling

# Function to Print Gantt Chart
def print_gantt(gantt):
    compressed = []

    # Merge consecutive same processes
    for p in gantt:
        if not compressed or compressed[-1][0] != p:#checkes if the last process in the compressed list is different from the current process
            compressed.append([p, 1])
        else:
            compressed[-1][1] += 1

    print("\nGantt Chart:")

    # Top Border
    for _ in compressed:
        print("+-------", end="")
    print("+")

    # Process Names
    for p, _ in compressed:
        print(f"|{p:^7}", end="")
    print("|")

    # Bottom Border
    for _ in compressed:
        print("+-------", end="")
    print("+")

    # Timeline
    time = 0
    print(f"{time:<8}", end="")
    for _, duration in compressed:
        time += duration
        print(f"{time:<8}", end="")
    print("\n")


# Counts how many times the process running on the CPU changes
# (used only for the tie-break decision, does not affect scheduling logic)
def count_switches(gantt):
    switches = 0
    for i in range(1, len(gantt)): 
        if gantt[i] != gantt[i - 1]:
            switches += 1
    return switches


#-------------------------- SRTF (Shortest Remaining Time First) --------------------------
def srtf(p):
    n = len(p)
    rt = [x[2] for x in p]
    ct = [0] * n
    t = done = 0
    gantt = []

    while done < n:
        idx = -1    
        mn = 10 ** 9
        for i in range(n):
            if p[i][1] <= t and rt[i] > 0 and rt[i] < mn:# it checks if the process has arrived, has remaining time, and has the least remaining time among all processes
                mn = rt[i]
                idx = i

        if idx == -1: #
            future = [p[i][1] for i in range(n) if rt[i] > 0 and p[i][1] > t]

            if future:
                next_time = min(future)
                gantt.extend(["Idle"] * (next_time - t))#curr = 5 , arr = 8 , diff = 3
                t = next_time #jumps directly
            continue    

        gantt.append(p[idx][0])#IF SELECTED PROCESS IS P2 IT WILL APPEND P2 IN GANTT CHART 
        rt[idx] -= 1 #reduces the remaining time of the selected process by 1
        t += 1

        if rt[idx] == 0:
            ct[idx] = t #stores ct
            done += 1 #increases ct by 1

    tat = [ct[i] - p[i][1] for i in range(n)] #calc tat for each p
    wt = [tat[i] - p[i][2] for i in range(n)]#calc wt for each p

    print("\n----- SRTF -----")
    print_gantt(gantt)
    print("Process\tCT\tTAT\tWT\tRT")
    for i in range(n):
        print(f"{p[i][0]}\t{ct[i]}\t{tat[i]}\t{wt[i]}\t{rt[i]}")
        # prints ct, tat, wt, rt for each process
    print("Average WT =", round(sum(wt) / n, 2))
    print("Average TAT =", round(sum(tat) / n, 2))
    return (
        sum(wt) / n,
        sum(tat) / n,
        gantt
    )

#---------------------------------------- ROUND ROBIN ----------------------------------------
def rr(p, q):
    n = len(p) 
    rem = [x[2] for x in p]
    ct = [0] * n 
    t = 0#current CPU time
    gantt = [] 
    ready = deque()#processes that are ready to execute
    visited = [False] * n #KEEPS TRACK OF PROCESSES THAT HAVE BEEN ADDED TO THE READY QUEUE
    done = 0 

    while done < n:
        for i in range(n):
            if p[i][1] <= t and not visited[i]:
                ready.append(i)
                visited[i] = True

        if not ready:
            future = [p[i][1] for i in range(n) if not visited[i]]#future arrival times of processes that have not yet been visited

            if future:
                next_time = min(future)
                gantt.extend(["Idle"] * (next_time - t))
                t = next_time
            continue

        i = ready.popleft()#pops the first process from the ready queue
        run = min(q, rem[i])
        #suppose TIME SLICE = 4
        #rt = 2
        #cpu should execute 2 and not 4 
        #min() chooses smaller value.

        for _ in range(run):
            gantt.append(p[i][0])
        t += run#it increases cpu time, amt of time process runs
        rem[i] -= run# it decreses cpu time, amt of time process runs

        for j in range(n):
            if p[j][1] <= t and not visited[j]:#Adds all newly arrived processes to the ready queue.
                ready.append(j)
                visited[j] = True

        if rem[i] > 0:
            ready.append(i)
        else:
            ct[i] = t
            done += 1

    tat = [ct[i] - p[i][1] for i in range(n)]
    wt = [tat[i] - p[i][2] for i in range(n)]

    print("\n----- ROUND ROBIN -----")
    print_gantt(gantt)
    print("Process\tCT\tTAT\tWT\tRT")
    for i in range(n):
        print(f"{p[i][0]}\t{ct[i]}\t{tat[i]}\t{wt[i]}\t{rem[i]}")
    print("Average WT =", round(sum(wt) / n, 2))
    print("Average TAT =", round(sum(tat) / n, 2))

    return (
        sum(wt) / n,
        sum(tat) / n,
        gantt
    )


# ---------------- MAIN ----------------

# Number of Processes
while True:
    try:
        n = int(input("Enter number of processes (1-20): ")) 
        if n <= 0:
            print("Error: Number of processes must be greater than 0.\n")
        elif n > 20:
            print("Error: Number of processes cannot exceed 20.\n")
        else:
            break
    except ValueError:
        print("Error: Please enter a valid integer.\n")

p = []

# Arrival Time and Burst Time
for i in range(n):

    while True:
        try:
            at = int(input(f"Arrival Time of P{i+1} (0-60): "))
            if at < 0:
                print(f"Error: Arrival Time of P{i+1} cannot be negative.\n")
            elif at > 60:
                print(f"Error: Arrival Time of P{i+1} cannot exceed 60.\n")
            else:
                break
        except ValueError:
            print(f"Error: Arrival Time of P{i+1} must be an integer.\n")

    while True:
        try:
            bt = int(input(f"Burst Time of P{i+1} (1-30): "))
            if bt <= 0:
                print(f"Error: Burst Time of P{i+1} must be greater than 0.\n")
            elif bt > 30:
                print(f"Error: Burst Time of P{i+1} cannot exceed 30.\n")
            else:
                break
        except ValueError:
            print(f"Error: Burst Time of P{i+1} must be an integer.\n")

    p.append((f"P{i+1}", at, bt))# # Store process as (Process Name, Arrival Time, Burst Time)

# Time Quantum
while True:
    try:
        q = int(input("Enter Time Quantum (1-10): "))
        if q <= 0:
            print("Error: Time Quantum must be greater than 0.\n")
        elif q > 10:
            print("Error: Time Quantum cannot exceed 10.\n")
        else:
            break
    except ValueError:
        print("Error: Time Quantum must be an integer.\n")

# Execute Algorithms
srtf_wt, srtf_tat, srtf_gantt = srtf(p)
rr_wt, rr_tat, rr_gantt = rr(p, q)

# ---------------- COMPARISON ----------------

print("\n----- COMPARISON -----")
srtf_score = srtf_wt + srtf_tat
rr_score = rr_wt + rr_tat

if srtf_score < rr_score:
    print("RESULT: SRTF performs better")
elif rr_score < srtf_score:
    print("RESULT: Round Robin performs better")
else:
    # Scores are tied on WT + TAT, so decide the winner using the Gantt chart
    # itself: fewer context switches means less CPU switching overhead.
    srtf_switches = count_switches(srtf_gantt)
    rr_switches = count_switches(rr_gantt)

    print(f"Scores are tied (WT+TAT = {srtf_score:.2f}). Deciding winner using Gantt chart context switches.")
    print(f"SRTF Context Switches = {srtf_switches}")
    print(f"Round Robin Context Switches = {rr_switches}")

    if srtf_switches < rr_switches:
        print("RESULT: SRTF performs better (fewer context switches on Gantt chart)")
    elif rr_switches < srtf_switches:
        print("RESULT: Round Robin performs better (fewer context switches on Gantt chart)")
    else:
        print("RESULT: Both perform equally (even Gantt chart context switches are same)")
