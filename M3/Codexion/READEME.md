*This project has been created as part of the 42 curriculum by mafonso.*

## Description

**Codexion** is a concurrent programming simulation that models a group of coders sharing limited resources in a circular co-working hub. Each coder needs two USB dongles (left and right) to compile quantum code. The simulation demonstrates classic concurrency challenges: deadlock prevention, starvation avoidance, resource cooldown, and fair scheduling.

The program uses POSIX threads (`pthread`) to represent coders as independent threads. Each coder cycles through three states: **compiling** (requires 2 dongles), **debugging**, and **refactoring**. The simulation stops when either all coders have completed the required number of compiles or a coder burns out from missing their compilation deadline.

## Instructions

### Compilation

```bash
make
```

### Execution

```bash
./codexion <number_of_coders> <time_to_burnout> <time_to_compile> <time_to_debug> <time_to_refactor> <number_of_compiles_required> <dongle_cooldown> <scheduler>
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `number_of_coders` | Number of coders (and dongles) |
| `time_to_burnout` | Milliseconds before burnout if no compile starts |
| `time_to_compile` | Milliseconds spent compiling (holding 2 dongles) |
| `time_to_debug` | Milliseconds spent debugging |
| `time_to_refactor` | Milliseconds spent refactoring |
| `number_of_compiles_required` | Number of compiles needed to stop successfully |
| `dongle_cooldown` | Milliseconds a dongle is unavailable after release |
| `scheduler` | `fifo` (First In, First Out) or `edf` (Earliest Deadline First) |

### Example

```bash
./codexion 5 1000 200 300 400 3 100 fifo
```

## Resources

### Documentation & References
- [pthreads documentation](https://man7.org/linux/man-pages/man7/pthreads.7.html)
- [Dining Philosophers Problem](https://en.wikipedia.org/wiki/Dining_philosophers_problem)
- [Deadlock - Coffman's Conditions](https://en.wikipedia.org/wiki/Deadlock#Necessary_conditions)
- [Earliest Deadline First Scheduling](https://en.wikipedia.org/wiki/Earliest_deadline_first_scheduling)

### AI Usage
AI was used for:
- **Initial problem structure**: Structure of flow, mutexes positions, and condition variables
- **Debugging assistance**: Identifying race conditions and deadlock scenarios
- **Documentation**: Structuring this README and code comments
- All AI-generated code was reviewed, tested, and fully understood before integration.

## Blocking Cases Handled

### Deadlock Prevention (Coffman's Conditions)
The solution breaks the 4 Coffman conditions:
1. **Mutual Exclusion**: Dongles are protected by mutexes
2. **Hold and Wait**: Coders acquire dongles in a fixed order (left then right, by ID)
3. **No Preemption**: Resources are never forcibly taken
4. **Circular Wait**: Fixed acquisition order prevents circular dependency

### Starvation Prevention
- **FIFO**: Fair queue ordering prevents starvation
- **EDF**: Earliest deadlines served first, ensuring no coder misses their deadline if parameters are feasible
- **Tie-breaking**: Deterministic coder_id tie-breaker ensures consistent behavior

### Cooldown Handling
Each dongle tracks its `available_at` timestamp. Coders cannot acquire a dongle until `current_time >= available_at`, preventing resource contention during cooldown periods.

### Precise Burnout Detection
A dedicated monitor thread checks coders at regular intervals (500µs). Burnout is detected within 10ms of the actual deadline, meeting the subject's precision requirements.

### Log Serialization
All log messages are protected by a global output mutex, preventing interleaving of messages from different threads.

## Thread Synchronization Mechanisms

### pthread_mutex_t
- **Dongle mutexes**: Each dongle has a mutex to protect its state (available_at, queue)
- **Log mutex**: Serializes output to prevent message interleaving
- **State mutex**: Protects shared simulation state (`sim_stop`, `sim_running`)

### pthread_cond_t
- **Condition variables**: Used for efficient waiting when dongles are unavailable
- **`pthread_cond_timedwait`**: Allows coders to wait with a timeout for resources

### Priority Queue (Custom Implementation)
- **Heap-based priority queue**: O(log n) push/pop operations
- **FIFO mode**: Sorted by request timestamp
- **EDF mode**: Sorted by deadline (`last_compile_start + time_to_burnout`)
- **Tie-breaker**: `coder_id` ensures deterministic ordering in edge cases

### Race Condition Prevention
- All shared state is accessed only while holding appropriate mutexes
- Atomic operations for `compiles_done` and `last_compile_start` (protected by state mutex)
- Dongle acquisition uses a two-phase locking protocol with fixed ordering

### Thread-Safe Communication
- Monitor thread coordinates with coders via shared state protected by mutexes
- Coders signal the monitor through state changes (e.g., incrementing compiles_done)
- Log messages are atomic (single write per message)

## Technical Decisions

### Fixed Acquisition Order
All coders acquire dongles in ascending ID order (`min(dongle_left, dongle_right)` first). This prevents circular wait and is the classic solution to the dining philosophers problem.

### Monitor Thread Design
A separate thread periodically checks all coders instead of using condition variables for each coder. This simplifies coordination and ensures precise burnout detection without adding complexity to the coder threads.

### Real-time vs CPU Time
Using `gettimeofday()` for real-time measurements, as recommended by the subject for simplicity and compatibility.
```