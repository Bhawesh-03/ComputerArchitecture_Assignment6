# Copyright (c) 2023 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.objects import *
from m5.util import fatal

fatal(
    "The 'configs/example/se.py' script has been deprecated. It can be "
    "found in 'configs/deprecated/example' if required. Its usage should be "
    "avoided as it will be removed in future releases of gem5."
)

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
