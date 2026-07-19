from collections import deque

# Function to Print Gantt Chart
def print_gantt(gantt):
    compressed = []

    # Merge consecutive same processes
    for p in gantt:
        if not compressed or compressed[-1][0] != p:
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
            if p[i][1] <= t and rt[i] > 0 and rt[i] < mn:
                mn = rt[i]
                idx = i

        if idx == -1:
            future = [p[i][1] for i in range(n) if rt[i] > 0 and p[i][1] > t]

            if future:
                next_time = min(future)
                gantt.extend(["Idle"] * (next_time - t))
                t = next_time
            continue

        gantt.append(p[idx][0])
        rt[idx] -= 1
        t += 1

        if rt[idx] == 0:
            ct[idx] = t
            done += 1

    tat = [ct[i] - p[i][1] for i in range(n)]
    wt = [tat[i] - p[i][2] for i in range(n)]

    print("\n----- SRTF -----")
    print_gantt(gantt)
    print("Process\tCT\tTAT\tWT")
    for i in range(n):
        print(f"{p[i][0]}\t{ct[i]}\t{tat[i]}\t{wt[i]}")
    print("Average WT =", round(sum(wt) / n, 2))
    print("Average TAT =", round(sum(tat) / n, 2))
    return (
        sum(wt) / n,
        sum(tat) / n
    )


def rr(p, q):
    n = len(p)
    rem = [x[2] for x in p]
    ct = [0] * n
    t = 0
    gantt = []
    ready = deque()
    visited = [False] * n
    done = 0

    while done < n:
        for i in range(n):
            if p[i][1] <= t and not visited[i]:
                ready.append(i)
                visited[i] = True

        if not ready:
            future = [p[i][1] for i in range(n) if not visited[i]]

            if future:
                next_time = min(future)
                gantt.extend(["Idle"] * (next_time - t))
                t = next_time
            continue

        i = ready.popleft()
        run = min(q, rem[i])

        for _ in range(run):
            gantt.append(p[i][0])
        t += run
        rem[i] -= run

        for j in range(n):
            if p[j][1] <= t and not visited[j]:
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
    print("Process\tCT\tTAT\tWT")
    for i in range(n):
        print(f"{p[i][0]}\t{ct[i]}\t{tat[i]}\t{wt[i]}")
    print("Average WT =", round(sum(wt) / n, 2))
    print("Average TAT =", round(sum(tat) / n, 2))
    return (
        sum(wt) / n,
        sum(tat) / n
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

    p.append((f"P{i+1}", at, bt))

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
srtf_wt, srtf_tat = srtf(p)
rr_wt, rr_tat = rr(p, q)

# ---------------- COMPARISON ----------------

print("\n----- COMPARISON -----")

if srtf_wt < rr_wt and srtf_tat < rr_tat:
    print("RESULT: SRTF performs better")
    print("SRTF always runs the process with the least work left, so jobs finish sooner and wait less.")

elif rr_wt < srtf_wt and rr_tat < srtf_tat:
    print("RESULT: Round Robin performs better")
    print("Round Robin gives every process a fair turn, so no single process waits too long.")

else:
    print("RESULT: Mixed performance")
    print("One algorithm has lower waiting time, the other has lower turnaround time, so neither wins overall.")