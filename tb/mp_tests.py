import pickle as p
import tempfile
import os
from cocotb_test.run import run as run_cocotb
from multiprocessing import Pool


def pickle(filename, **kwargs):
    with open(filename, "wb") as handle:
        p.dump(kwargs, handle)


def unpickle(filename):
    with open(filename, "rb") as handle:
        b = p.load(handle)
    return b


class MpTest(object):
    def __init__(self, sim_args, testcase, seed=1, **kwargs):
        self.sim_args = sim_args
        self.testcase = testcase
        self.seed = seed
        self.kwargs = kwargs


def _run_test(sim_args, seed, testcase, kwargs):
    os.environ["RANDOM_SEED"] = str(seed)
    os.environ["TESTCASE"] = testcase

    fo = tempfile.NamedTemporaryFile()
    in_filename = fo.name
    fo.close()

    fo = tempfile.NamedTemporaryFile()
    out_filename = fo.name
    fo.close()

    fo = tempfile.NamedTemporaryFile(suffix="_coverege.xml")
    coverege_results_file_name = fo.name
    fo.close()

    os.environ["COCOTB_KWARGS_FILENAME"] = in_filename
    os.environ["COCOTB_RESULTS_FILENAME"] = out_filename
    os.environ["COCOTB_COVEREGE_RESULTS_FILE_NAME"] = coverege_results_file_name

    pickle(filename=in_filename, **kwargs)

    test_results = run_cocotb(**sim_args)

    res = unpickle(out_filename)

    return coverege_results_file_name, test_results, res


def mp_run(tests):
    pool = Pool()

    agrs = []
    for t in tests:
        agrs.append((t.sim_args, t.seed, t.testcase, t.kwargs))

    ret = pool.starmap(_run_test, agrs)

    for i, t in enumerate(tests):
        t.coverage_result_file = ret[i][0]
        t.result_file = ret[i][1]

        for arg in ret[i][2]:
            setattr(t, arg, ret[i][2][arg])

        t.results = ret[i][2]

    return ret
