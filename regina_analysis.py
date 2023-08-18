import numpy as np

def write_warning(run_number, skipped_events):
    with open(f"./TOF-{run_number}.log", "w") as log:
        log.write("These events were skipped:\n")
        for i in range(0, len(skipped_events)):
            log.write(f"{i}\n")

def get_run_number(root_file_path):
    # Split path of files named "root_run_XXXXXX.root" to find XXXXXX
    # @params: _root_file_path_ containing the Linux/Mac path to the root file
    # @return: string with XXXXXX
    split1 = root_file_path.split("-")
    run_number = split1[-1].replace(".npz","")
    return run_number


def load_event_information(event_number, npz_file_path):
    data = np.load(npz_file_path, allow_pickle=True)
    print("Looking for pulse information...")
    entry = np.where(data["event_number"]==event_number)[0][0]
    return data["count"][entry], data["baseline"][entry], data["CFD_timing"][entry], data["amplitude"][entry]


def load_information(npz_file_path):
    data = np.load(npz_file_path, allow_pickle=True)
    return data["count"], data["baseline"], data["CFD_timing"], data["amplitude"], data["event_number"]


def generate_TOF_matrix():
    pass


def generate_TOF_array(timing, amplitude, N):
    sorted_amps = [np.argsort(amplitude[i]) for i in range(0,8)]
    TOF_j = np.array([], dtype="float")
    for j in range(0, N):
        TOF0_j = np.average([timing[i][j] for i in range(0,4) if len(timing[i]) > j ])
        TOF1_j = np.average([timing[i][j] for i in range(4,8) if len(timing[i]) > j ])
        TOF_j  = np.append(TOF_j, [TOF1_j - TOF0_j], axis = None)
    return TOF_j
    
    