
from m5.objects import *

# Define system
system = System()
system.clk_domain = SrcClockDomain(clock='1GHz', voltage_domain=VoltageDomain())
system.mem_mode = 'timing'  # Required for shared memory
system.mem_ranges = [AddrRange('512MB')]

# Create CPUs
system.cpu = [MinorCPU() for i in range(4)]  # Adjust the number of cores

# Configure thread-level parallelism
for cpu in system.cpu:
    cpu.workload = SEWorkload.init_compatible('daxpy')  # Path to your daxpy binary
    cpu.createThreads()

# Define memory
system.membus = SystemXBar()
system.mem_ctrl = DDR3_1600_8x8(range=system.mem_ranges[0], port=system.membus.master)
system.system_port = system.membus.slave

# Define cache
system.l1_cache = [L1ICache(size='32kB') for _ in range(4)]
system.l2_cache = L2Cache(size='256kB')
for i in range(4):
    system.cpu[i].icache_port = system.l1_cache[i].cpu_side
    system.cpu[i].dcache_port = system.l1_cache[i].cpu_side

system.l2bus = SystemXBar()
for i in range(4):
    system.l1_cache[i].mem_side = system.l2bus.slave
system.l2_cache.cpu_side = system.l2bus.master
system.l2_cache.mem_side = system.membus.slave

# Simulation configuration
root = Root(full_system=False, system=system)
m5.instantiate()
print("Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
