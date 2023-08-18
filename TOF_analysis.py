import numpy as np, progressbar, sys
from regina_analysis import *

# Scale factors
h_factor = 1./500.e6*1.e9
v_factor = 1./16384.*2.*1.e3
npz_file_path  = sys.argv[1]

# Load time information
print("Loading file...", end="\r")
run_number = get_run_number(npz_file_path)
count, baseline, timing, amplitude, event_number = load_information(npz_file_path)
number_of_events = int(1.*len(count))
print("Loading file... Done.")

# Find TOF channels and keep pulses of higher amplitudes
# timing = timing_in
timing = [timing[:][i] for i in range(8,16)]
amplitude = [amplitude[:][i] for i in range(8,16)]
# timing = [timing[i][abs(amplitude[i]) > 40] for i in range(0,8)]

# Start progress bar
widgets=[f'TOF analysis: ', progressbar.Percentage(), progressbar.Bar('\u2587', '|', '|'), ' ', progressbar.Timer()]            
bar = progressbar.ProgressBar(widgets=widgets, maxval=number_of_events).start()

# Start analysis
TOF_1 = np.array([], dtype="float")
TOF_2 = np.array([], dtype="float")
save_event_number = []
skipped_events = []
for i in range(0, number_of_events):
    bar.update(i)
    try:
        TOF = generate_TOF_array(timing[i], amplitude[i], 2)
        TOF_1 = np.append(TOF_1, [TOF[0]], axis=None)
        TOF_2 = np.append(TOF_2, [TOF[1]], axis=None)
        save_event_number = np.append(save_event_number, [event_number[i][0]], axis=None)
    except IndexError:
        skipped_events.append(i)

if len(skipped_events) > 0:
    write_warning(run_number, skipped_events)

print("\033[K\033[F")
print(f"Saving to file: ../data/TOF_{run_number}.npz")
np.savez_compressed(f"../data/TOF_{run_number}.npz", TOF_1=TOF_1, TOF_2=TOF_2, event_number=save_event_number)

    