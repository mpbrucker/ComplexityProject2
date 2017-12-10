import pickle
import types
import datetime

from multiprocessing import pool

from quake import Earthquake

params = {
    "processes": 8,
    "test_range": (0.05, 0.25),
    "test_def": 20,
    "iters": 1  ,
    "n": 35
}

def run_quake_wrapper(params):
    return run_quake(**params)

def run_quake(iters, **params):
    quake = Earthquake(**params)
    info = {"iters": iters, "a1": quake.a1}
    info.update(params)
    slipped = quake.run(iters)
    return info, slipped

def run_quakes_multithreaded(a_test_range, a_test_res, iters, processes, **params):
    pool = Pool(processes)
    a_vals = np.linspace(*a_test_range, num=a_test_res) # Build a list of elasticity coefficients
    K_val = 1
    KL_vals = K_val/a_vals - 4*K_val  # Calculate KL based on K and alpha

    # params_list = [{"k1": K_val, "kl":kl, **params} for kl in KL_vals]  # build list of params for process distribution
    params_list = []
    for kl in KL_vals:
        ks = {'k1': K_val, "kl":kl}
        ks.update(params)
        params_list.append(kwd)

    infos, slipped = pool.map(run_quake_wrapper, params_list)
    return infos, slipped


if __name__ == "__main__":
    import pickle
    import types

    import datetime
    timestamp = str(datetime.datetime.now())

    infos, slipped = run_quakes_multithreaded(params)

    run = types.SimpleNamespace()
    run.params = params
    run.results = []

    for i in range(len(slipped):
        
