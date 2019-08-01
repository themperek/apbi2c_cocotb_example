

from cocotb_test.run import run
import os


from multiprocessing import Pool


def sim_mp(sim_args, seed, test_name):
    os.environ["RANDOM_SEED"]  = str(seed)
    os.environ["TESTCASE"]  = test_name
    
    coverege_results_file_name = os.path.abspath(os.path.join("sim_build", sim_args['module'] + "_"+ test_name + "_" + str(seed) + ".xml"))
    os.environ["COCOTB_COVEREGE_RESULTS_FILE_NAME"] = coverege_results_file_name
    test_results = run(**sim_args)
    
    return coverege_results_file_name, test_results

pool = Pool()

dut_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apbi2c","rtl")
sim_args = {
    "verilog_sources": [
     os.path.join(dut_dir, "apb.v"),
     os.path.join(dut_dir, "fifo.v"),
     os.path.join(dut_dir, "i2c.v"),
     os.path.join(dut_dir, "module_i2c.v"),
     ],
    "toplevel": "i2c",
    "module": "test_i2c",
    
}


if __name__ == "__main__":
    
    #Run once so all it is compiled once (TO be fixed in cocotb-test)   ONLY NEEDED 1st time
    try:
        sim_mp(sim_args, 1, "test_tree_non_existing") 
    except:
        pass
    
    #define arguments (seeds/tests) to run for multiple runs 
    agrs = []
    for seed in range(10):
        agrs.append((sim_args, seed,"test_tree"))
    
    #run in paraller
    results = pool.starmap(sim_mp, agrs)
    
    #Can parse xml files (YAML would be easier)
    print(results)
    