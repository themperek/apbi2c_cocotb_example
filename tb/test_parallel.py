import os
from mp_tests import MpTest, mp_run
from cocotb_test.run import run as run_cocotb

dut_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apbi2c", "rtl")
sim_args = {
    "verilog_sources": [os.path.join(dut_dir, "apb.v"), os.path.join(dut_dir, "fifo.v"), os.path.join(dut_dir, "i2c.v"), os.path.join(dut_dir, "module_i2c.v")],
    "toplevel": "i2c",
    "module": "test_i2c",
}


if __name__ == "__main__":

    # Run once so all is compiled once (TO be fixed in cocotb-test) ONLY NEEDED 1st time
    try:
        run_cocotb(**sim_args)  # will fail but will compile
    except:
        pass


    t1 = MpTest(sim_args, testcase="test_tree", seed=1, checkpoint=None, pram1=1, param2=3)
    t2 = MpTest(sim_args, testcase="test_tree", seed=2, checkpoint=None, pram1=1, param2=3)
    t3 = MpTest(sim_args, testcase="test_tree", seed=3, checkpoint=None, pram1=1, param2=3)
    t4 = MpTest(sim_args, testcase="test_tree", seed=4, checkpoint=None, pram1=1, param2=3)

    mp_run([t1, t2, t3, t4])

    print(t1.coverage_result_file, t1.result_file)
    # print(t1.checkpoint)
    # print(t1.results)
    
    print(t1.ret1)  
    # or 
    print(t1.results["ret1"])

    if t1.ret1 == 5:
        tests = []
        for i in range(10):
            tests.append(MpTest(sim_args, testcase="test_tree", seed=i, checkpoint=t2.checkpoint))

        mp_run(tests)

        print(tests[0].ret1)
