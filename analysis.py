# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
import pandas as pd

# Load DataFrames from CSV files back into original variables

rc19 = pd.read_csv('rc19.csv')
rc20 = pd.read_csv('rc20.csv')
orbit19 = pd.read_csv('orbit19.csv')
orbit20 = pd.read_csv('orbit20.csv')

# Explicitly convert time columns to datetime objects after loading
rc19['corr_time'] = pd.to_datetime(rc19['corr_time'], errors='coerce', utc=True).dt.as_unit('ns')
rc20['corr_time'] = pd.to_datetime(rc20['corr_time'], errors='coerce', utc=True).dt.as_unit('ns')
orbit19['UTC'] = pd.to_datetime(orbit19['UTC'], errors='coerce', utc=True).dt.as_unit('ns')
orbit20['UTC'] = pd.to_datetime(orbit20['UTC'], errors='coerce', utc=True).dt.as_unit('ns')

print("DataFrames successfully loaded from CSV files back into original variables.")

print("\nFirst 5 rows of rc19 after loading:")
display(rc19.head())
print("\nFirst 5 rows of rc20 after loading:")
display(rc20.head())
print("\nFirst 5 rows of orbit19 after loading:")
display(orbit19.head())
print("\nFirst 5 rows of orbit20 after loading:")
display(orbit20.head())
# %%
# Soyuz MS-15 (2019) — Soyuz-FG
L19 = pd.Timestamp("2019-09-25 13:57:42.701", tz="UTC")
events_2019 = {
    "Launch":              L19,
    "20 km\n(79 s)":  L19 + pd.Timedelta(seconds=79),
    "90 s":  L19 + pd.Timedelta(seconds=90),
    "Boosters sep\n(+01:58)":  pd.Timestamp("2019-09-25 13:59:40.501", tz="UTC"),  # Korolev cross
    "Fairing jettison\n(+02:37)":  pd.Timestamp("2019-09-25 14:00:20.181", tz="UTC"),
    "Core stage sep\n(+04:47)": L19 + pd.Timedelta(minutes=4, seconds=47), # 287 seconds after launch
    "S/C separation\n(+08:48)": L19 + pd.Timedelta(minutes=8, seconds=48), # 528 seconds after launch
    #"SAA":  pd.Timestamp("2019-09-25 15:00:51.000", tz="UTC"),  # 1-st SAA
    "Docking":              pd.Timestamp("2019-09-25 19:42:40", tz="UTC"),
    "Undocking\n(MS-13)":   pd.Timestamp("2020-02-06 05:50:28", tz="UTC"),
    "Landing\n(MS-13)":     pd.Timestamp("2020-02-06 09:12:23", tz="UTC"),
}

# Soyuz MS-17 (2020) — Soyuz-2.1a, 2-orbit ultrafast rendezvous
L20 = pd.Timestamp("2020-10-14 05:45:04", tz="UTC")
events_2020 = {
    "Launch":              L20,
    "20 km\n(79 s)":  L20 + pd.Timedelta(seconds=79),
    "90 s":  L20 + pd.Timedelta(seconds=90),
    "Boosters sep\n(+01:58)":  L20 + pd.Timedelta(seconds=118),
    "Fairing jettison\n(+02:37)":  L20 + pd.Timedelta(seconds=157),
    "Core stage sep\n(+04:47)": L20 + pd.Timedelta(seconds=287),
    "S/C separation\n(+08:48)": L20 + pd.Timedelta(seconds=528),
    "Docking":              pd.Timestamp("2020-10-14 08:48:43", tz="UTC"),
}
# %%
def draw_events(ax, events, tmin, tmax, color='black'):
    """Plots vertical lines with labels for events occurring within [tmin, tmax]."""
    ymin, ymax = ax.get_ylim()
    for name, t in events.items():
        if tmin <= t <= tmax:
            ax.axvline(t, linestyle="--", linewidth=1, color=color, alpha=0.7)
            ax.text(t, ymax, name,
                    rotation=90, va="top", ha="right",
                    fontsize=9, color=color,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.6))
# %%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

if 'orbit19' in globals() and 'rc19' in globals():
    tmin = events_2019["Launch"] - pd.Timedelta(hours=1)
    tmax = tmin + pd.Timedelta(days=7)

    z  = rc19.loc[(rc19["corr_time"] > tmin) & (rc19["corr_time"] < tmax)]
    zo = orbit19.loc[(orbit19["UTC"] > tmin) & (orbit19["UTC"] < tmax)]

    plt.figure(figsize=(20, 5))
    plt.rcParams.update({'font.size': 13})
    ax = plt.gca()
    ax.plot(z["corr_time"], z["flux"], color='tab:blue', lw=0.8, alpha=0.9, label="Flux")
    ax.set_yscale('log')
    ax.set_xlabel("UTC")
    ax.set_ylabel(r"Flux [cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", color='tab:blue')
    ax.tick_params(axis='y', labelcolor='tab:blue')
    ax.set_title("SPACEDOS – Soyuz MS-15 (2019), first week")
    ax.grid(which='both', alpha=0.3)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))

    ax2 = ax.twinx()
    ax2.plot(zo["UTC"], zo["L"], color='gray', lw=0.5, alpha=0.6, label="L-shell")
    ax2.set_ylabel("L-shell", color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')

    draw_events(ax, events_2019, tmin, tmax)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig("ms15_first_week.png", dpi=300)
    plt.show()
else:
    print("Dependency Missing: Please run the data loading cell for 'orbit19' and 'rc19' first.")
# %%import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

tmin = events_2020["Launch"] - pd.Timedelta(hours=1)
tmax = tmin + pd.Timedelta(days=7)

z  = rc20.loc[(rc20["corr_time"] > tmin) & (rc20["corr_time"] < tmax)]
zo = orbit20.loc[(orbit20["UTC"] > tmin) & (orbit20["UTC"] < tmax)]

plt.figure(figsize=(20, 5))
plt.rcParams.update({'font.size': 13})
ax = plt.gca()
ax.plot(z["corr_time"], z["flux"], color='tab:orange', lw=0.8, alpha=0.9, label="Flux")
ax.set_yscale('log')
ax.set_xlabel("UTC")
ax.set_ylabel(r"Flux [cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", color='tab:orange')
ax.tick_params(axis='y', labelcolor='tab:orange')
ax.set_title("SPACEDOS – Soyuz MS-17 (2020), first week incl. launch & docking")
ax.grid(which='both', alpha=0.3)
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))

ax2 = ax.twinx()
ax2.plot(zo["UTC"], zo["L"], color='gray', lw=0.5, alpha=0.6, label="L-shell")
ax2.set_ylabel("L-shell", color='gray')
ax2.tick_params(axis='y', labelcolor='gray')

draw_events(ax, events_2020, tmin, tmax)
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig("ms17_first_week.png", dpi=300)
plt.show()
# %%
import matplotlib.pyplot as plt
import matplotlib

fig, axes = plt.subplots(2, 1, figsize=(20, 9), sharex=True)
matplotlib.rcParams.update({'font.size': 13})

for ax, rc, orb, events, color, label in [
    (axes[0], rc19, orbit19, events_2019, 'tab:blue',   "Soyuz MS-15 (2019)"),
    (axes[1], rc20, orbit20, events_2020, 'tab:orange', "Soyuz MS-17 (2020)"),
]:
    launch = events["Launch"]
    tmin = launch - pd.Timedelta(minutes=30)
    tmax = launch + pd.Timedelta(hours=6.6)

    z  = rc.loc[(rc["corr_time"] > tmin) & (rc["corr_time"] < tmax)].copy()
    zo = orb.loc[(orb["UTC"] > tmin) & (orb["UTC"] < tmax)].copy()
    z["t_hours"]  = (z["corr_time"] - launch).dt.total_seconds() / 3600.0
    zo["t_hours"] = (zo["UTC"] - launch).dt.total_seconds() / 3600.0

    ax.plot(z["t_hours"], z["flux"], color=color, lw=0.9, alpha=0.9, label=label)
    ax.set_yscale('log')
    ax.set_ylabel(r"Flux [cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", color=color)
    ax.tick_params(axis='y', labelcolor=color)
    ax.grid(which='both', alpha=0.3)
    ax.legend(loc='upper left')

    ax2 = ax.twinx()
    ax2.plot(zo["t_hours"], zo["L"], color='gray', lw=0.7, alpha=0.7, label="L-shell")
    ax2.set_ylabel("L-shell", color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')
    ax2.legend(loc='upper right')

    ymin, ymax = ax.get_ylim()
    for name, t in events.items():
        t_rel = (t - launch).total_seconds() / 3600.0
        if -0.5 <= t_rel <= 6.6:
            ax.axvline(t_rel, linestyle="--", linewidth=1, color='black', alpha=0.6)
            ax.text(t_rel, ymax, name,
                    rotation=90, va="top", ha="right", fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.6))

axes[1].set_xlabel("Time since launch [hours]")
fig.suptitle("SPACEDOS – first ~6.6 hours after launch, 2019 vs 2020", fontsize=15)
plt.tight_layout()
plt.savefig("launch_comparison_6h.png", dpi=300)
plt.show()


# %%
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

fig, axes = plt.subplots(1, 2, figsize=(20, 5), sharey=True)
matplotlib.rcParams.update({'font.size': 13})

for ax, rc, orb, events, color, label in [
    (axes[0], rc19, orbit19, events_2019, 'tab:blue',   "Soyuz MS-15 (2019)"),
    (axes[1], rc20, orbit20, events_2020, 'tab:orange', "Soyuz MS-17 (2020)"),
]:
    launch = events["Launch"]
    # Detail window: 5 minutes before to 1.2 hours (72 min) after launch
    tmin = launch - pd.Timedelta(minutes=5)
    tmax = launch + pd.Timedelta(hours=1.2)

    z  = rc.loc[(rc["corr_time"] > tmin) & (rc["corr_time"] < tmax)].copy()
    zo = orb.loc[(orb["UTC"] > tmin) & (orb["UTC"] < tmax)].copy()
    z["t_min"]  = (z["corr_time"] - launch).dt.total_seconds() / 60.0
    zo["t_min"] = (zo["UTC"] - launch).dt.total_seconds() / 60.0

    ax.plot(z["t_min"], z["flux"], marker='.', ms=3, lw=0.8, color=color, alpha=0.9, label=label)
    ax.set_yscale('log')
    ax.set_xlabel("Time since launch [min]")
    ax.set_ylabel(r"Flux [cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", color=color)
    ax.tick_params(axis='y', labelcolor=color)
    ax.grid(which='both', alpha=0.3)
    ax.legend(loc='upper left')
    ax.set_title(label)

    ax2 = ax.twinx()
    ax2.plot(zo["t_min"], zo["L"], color='gray', lw=0.7, alpha=0.7, label="L-shell")
    ax2.set_ylabel("L-shell", color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')
    ax2.legend(loc='upper right')

    # MODIFIED: Draw only events within the range of this specific detail plot
    ymin, ymax = ax.get_ylim()
    for name, t in events.items():
        t_rel_min = (t - launch).total_seconds() / 60.0
        if -5 <= t_rel_min <= 72:
            ax.axvline(t_rel_min, linestyle="--", linewidth=1, color='black', alpha=0.6)
            ax.text(t_rel_min, ymax, name, rotation=90, va="top", ha="right", fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.6))

fig.suptitle("SPACEDOS – first ~1 hour after launch (SAA passage)", fontsize=15)
plt.tight_layout()
plt.savefig("saa_passage_detail.png", dpi=300)
plt.show()


# %%
# Define the highlighted time ranges in hours relative to launch
highlight_ranges = [
    {'start': 52.5, 'end': 62},
    {'start': 30, 'end': 38},
    {'start': 6, 'end': 14}
]

# %%
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

fig, axes = plt.subplots(2, 1, figsize=(20, 9), sharex=False)
matplotlib.rcParams.update({'font.size': 13})

for i, (ax, rc, orb, events, color, label) in enumerate([
    (axes[0], rc19, orbit19, events_2019, 'tab:blue',   "Soyuz MS-15 (2019)"),
    (axes[1], rc20, orbit20, events_2020, 'tab:orange', "Soyuz MS-17 (2020)"),
]):
    launch = events["Launch"]
    tmin = launch - pd.Timedelta(minutes=30)
    tmax = launch + pd.Timedelta(hours=72)

    z  = rc.loc[(rc["corr_time"] > tmin) & (rc["corr_time"] < tmax)].copy()
    zo = orb.loc[(orb["UTC"] > tmin) & (orb["UTC"] < tmax)].copy()
    z["t_hours"]  = (z["corr_time"] - launch).dt.total_seconds() / 3600.0
    zo["t_hours"] = (zo["UTC"] - launch).dt.total_seconds() / 3600.0

    ax.plot(z["t_hours"], z["flux"], color=color, lw=0.9, alpha=0.9, label=label)
    ax.set_yscale('log')
    ax.set_ylabel(r"Flux [cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", color=color)
    ax.tick_params(axis='y', labelcolor=color)
    ax.grid(which='both', alpha=0.3)
    ax.legend(loc='upper left')
    ax.set_title(label + " – first ~72 hours after launch")

    # Draw highlighted ranges from the highlight_ranges variable
    for j, h_range in enumerate(highlight_ranges):
        start_h_hr = h_range['start']
        end_h_hr = h_range['end']
        if i == 0 and j == 0: # Add label only for the first highlight span to avoid repetitive legend entries
            ax.axvspan(start_h_hr, end_h_hr, color='lightgray', alpha=0.5, label='Highlighted ranges')
        else:
            ax.axvspan(start_h_hr, end_h_hr, color='lightgray', alpha=0.5)

    ax2 = ax.twinx()
    ax2.plot(zo["t_hours"], zo["L"], color='gray', lw=0.5, alpha=0.6, label="L-shell")
    ax2.set_ylabel("L-shell", color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')
    ax2.legend(loc='upper right')

    # MODIFIED: Draw only events within the range of this specific plot (-0.5h to 72h)
    ymin, ymax = ax.get_ylim()
    for name, t in events.items():
        t_rel = (t - launch).total_seconds() / 3600.0
        if -0.5 <= t_rel <= 72:
            ax.axvline(t_rel, linestyle="--", linewidth=1, color='black', alpha=0.6)
            ax.text(t_rel, ymax, name, rotation=90, va="top", ha="right", fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.6))

axes[1].set_xlabel("Time since launch [hours]")
fig.suptitle("SPACEDOS – 72h Flux Overview", fontsize=15)
plt.tight_layout()
plt.savefig("72h_overview_highlighted.png", dpi=300)
plt.show()

# %%
import numpy as np
from scipy.optimize import curve_fit

def parabolic_fit(x, a, b, c):
    return a * x**2 + b * x + c

def calculate_shift_error(popt, pcov):
    a, b, _ = popt
    if np.isclose(a, 0): return np.nan
    df_da = b / (2 * a**2)
    df_db = -1 / (2 * a)
    var_a, var_b, cov_ab = pcov[0, 0], pcov[1, 1], pcov[0, 1]
    var_shift = (df_da**2 * var_a) + (df_db**2 * var_b) + (2 * df_da * df_db * cov_ab)
    return np.sqrt(var_shift) if var_shift >= 0 else np.nan

def find_precise_peak(shifts, correlations):
    shifts_arr, correlations_arr = np.array(shifts), np.array(correlations)
    max_corr_idx = np.nanargmax(correlations_arr)
    window_size = 2
    start_idx = max(0, max_corr_idx - window_size)
    end_idx = min(len(shifts_arr) - 1, max_corr_idx + window_size)
    x_data, y_data = shifts_arr[start_idx : end_idx + 1], correlations_arr[start_idx : end_idx + 1]

    try:
        popt, pcov = curve_fit(parabolic_fit, x_data, y_data, p0=[-0.0001, 0, correlations_arr[max_corr_idx]])
        precise_shift = -popt[1] / (2 * popt[0])
        return precise_shift, parabolic_fit(precise_shift, *popt), calculate_shift_error(popt, pcov)
    except:
        return float(shifts_arr[max_corr_idx]), float(correlations_arr[max_corr_idx]), np.nan

def calculate_shifted_correlation(flux_df, l_shell_df, time_shift_seconds):
    """
    Calculates the Pearson correlation between flux and L-shell with a given time shift.

    Args:
        flux_df (pd.DataFrame): DataFrame with 'corr_time' (datetime) and 'flux'.
        l_shell_df (pd.DataFrame): DataFrame with 'UTC' (datetime) and 'L'.
        time_shift_seconds (int): Time shift in seconds to apply to FLUX data.

    Returns:
        float: Pearson correlation coefficient.
    """
    # Create a copy of flux_df to apply shift, avoid modifying original
    shifted_flux_df = flux_df.copy()
    shifted_flux_df['time_to_use'] = shifted_flux_df['corr_time'] + pd.Timedelta(seconds=time_shift_seconds)

    # Sort both dataframes by their time columns for merge_asof
    shifted_flux_df_sorted = shifted_flux_df.sort_values(by='time_to_use')
    l_shell_df_sorted = l_shell_df.sort_values(by='UTC') # L-shell is NOT shifted

    # Merge shifted flux and unshifted L-shell data. 'left_on' is shifted_flux_df's time, 'right_on' is L-shell's time.
    # 'direction='nearest' finds the closest match within tolerance.
    merged_df = pd.merge_asof(
        shifted_flux_df_sorted,
        l_shell_df_sorted[['UTC', 'L']], # Use unshifted UTC for L-shell
        left_on='time_to_use',
        right_on='UTC',
        direction='nearest',
        tolerance=pd.Timedelta(seconds=5) # Allow 5 seconds difference for matching flux (10s integration)
    )

    # Drop rows where 'flux' or 'L' might be NaN if no match was found within tolerance or original NaNs
    merged_df = merged_df.dropna(subset=['flux', 'L'])

    if len(merged_df) > 1: # Need at least 2 points to calculate correlation
        return merged_df['flux'].corr(merged_df['L'])
    else:
        return np.nan # Not enough data for correlation
# %%
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

# Ensure shifts_corr_range is defined (from cell 0586ed78)
# This defines the range of time shifts to test (-3 minutes to +3 minutes with 5s step)
shifts_corr_range = np.arange(-240, 240, 5)

# Lists to store correlations for all highlight ranges
all_correlations_2019 = []
all_correlations_2020 = []

print("Calculating and plotting correlations for each highlight range...")

for i, r_dict in enumerate(highlight_ranges):
    start_h = r_dict['start']
    end_h = r_dict['end']
    print(f"\n  Processing range: {start_h} to {end_h} hours after launch")

    # --- Prepare data for 2019 ---
    launch_2019 = events_2019['Launch']
    tmin_2019_range = launch_2019 + pd.Timedelta(hours=start_h)
    tmax_2019_range = launch_2019 + pd.Timedelta(hours=end_h)

    # Use rc19 with its already shifted 'corr_time' for this correlation
    z19_range_current = rc19.loc[(rc19['corr_time'] >= tmin_2019_range) & (rc19['corr_time'] <= tmax_2019_range)].copy()
    zo19_range = orbit19.loc[(orbit19['UTC'] >= tmin_2019_range) & (orbit19['UTC'] <= tmax_2019_range)].copy()

    correlations_2019_current_range = []
    for shift in shifts_corr_range:
        corr_19 = calculate_shifted_correlation(z19_range_current, zo19_range, shift)
        correlations_2019_current_range.append(corr_19)
    all_correlations_2019.append(correlations_2019_current_range)

    # --- Prepare data for 2020 ---
    launch_2020 = events_2020['Launch']
    tmin_2020_range = launch_2020 + pd.Timedelta(hours=start_h)
    tmax_2020_range = launch_2020 + pd.Timedelta(hours=end_h)

    # Use rc20 with its already shifted 'corr_time' for this correlation
    z20_range_current = rc20.loc[(rc20['corr_time'] >= tmin_2020_range) & (rc20['corr_time'] <= tmax_2020_range)].copy()
    zo20_range = orbit20.loc[(orbit20['UTC'] >= tmin_2020_range) & (orbit20['UTC'] <= tmax_2020_range)].copy()

    correlations_2020_current_range = []
    for shift in shifts_corr_range:
        corr_20 = calculate_shifted_correlation(z20_range_current, zo20_range, shift)
        correlations_2020_current_range.append(corr_20)
    all_correlations_2020.append(correlations_2020_current_range)

    # --- Plotting for the current highlight range ---
    plt.figure(figsize=(12, 6))
    matplotlib.rcParams.update({'font.size': 12})

    plt.plot(shifts_corr_range, correlations_2019_current_range, marker='o', linestyle='-', label='2019 (Soyuz MS-15)', color='tab:blue')
    plt.plot(shifts_corr_range, correlations_2020_current_range, marker='x', linestyle='--', label='2020 (Soyuz MS-17)', color='tab:orange')

    plt.title(f'Correlation between Flux and L-shell vs. Time Shift ({start_h}-{end_h} hours after launch)')
    plt.xlabel('L-shell Time Shift [s]')
    plt.ylabel('Pearson Correlation Coefficient')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.axvline(0, color='grey', linestyle=':', linewidth=0.8)
    plt.tight_layout()
    plt.savefig(f"correlation_vs_shift_{start_h}h_to_{end_h}h.png", dpi=300)
    plt.show()

print("\nAll correlation calculations and plots complete.")

# %%
optimal_shifts_results = []

for i, r_dict in enumerate(highlight_ranges):
    start_h = r_dict['start']
    end_h = r_dict['end']

    # 2019
    shifts_19 = shifts_corr_range
    corrs_19 = all_correlations_2019[i]
    precise_shift_19_val, max_corr_19_val, error_19_val = find_precise_peak(shifts_19, corrs_19)

    # 2020
    shifts_20 = shifts_corr_range
    corrs_20 = all_correlations_2020[i]
    precise_shift_20_val, max_corr_20_val, error_20_val = find_precise_peak(shifts_20, corrs_20)

    optimal_shifts_results.append({
        'Range_Start_h': start_h,
        'Range_End_h': end_h,
        '2019_Optimal_Shift_s': precise_shift_19_val,
        '2019_Max_Correlation': max_corr_19_val,
        '2019_Shift_Error_s': error_19_val,
        '2020_Optimal_Shift_s': precise_shift_20_val,
        '2020_Max_Correlation': max_corr_20_val,
        '2020_Shift_Error_s': error_20_val,
    })

df_optimal_shifts = pd.DataFrame(optimal_shifts_results)

print("Optimal Shifts and Max Correlations for Each Highlight Range:")
display(df_optimal_shifts[['Range_Start_h', 'Range_End_h', '2019_Optimal_Shift_s', '2019_Shift_Error_s', '2020_Optimal_Shift_s', '2020_Shift_Error_s']])

# Define precise_shift_19 and precise_shift_20 from the first highlight range for consistency with prior notebook state
precise_shift_19 = df_optimal_shifts.loc[0, '2019_Optimal_Shift_s']
precise_shift_20 = df_optimal_shifts.loc[0, '2020_Optimal_Shift_s']

# Also define error_19 and error_20 here for use in subsequent cells
error_19 = df_optimal_shifts.loc[2, '2019_Shift_Error_s']
error_20 = df_optimal_shifts.loc[2, '2020_Shift_Error_s']
# %%
# tady se vybira, z jakeho casoveho rozsahu se pouzije korelace
precise_shift_19 = df_optimal_shifts.loc[0, '2019_Optimal_Shift_s']
#precise_shift_19 = -180
precise_shift_20 = df_optimal_shifts.loc[0, '2020_Optimal_Shift_s']
#precise_shift_20 = 72
# %%
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

if 'precise_shift_19' in globals():
    fig, axes = plt.subplots(2, 1, figsize=(15, 10), sharex=True)
    matplotlib.rcParams.update({'font.size': 12})

    plot_data = [
        (rc19, events_2019, 'tab:blue',   "Soyuz MS-15 (2019)", precise_shift_19),
        (rc20, events_2020, 'tab:orange', "Soyuz MS-17 (2020)", precise_shift_20),
    ]

    for i, (rc, events, color, label, time_shift) in enumerate(plot_data):
        ax = axes[i]
        launch = events["Launch"]
        # Detail window: 5 minutes before to 30 minutes after launch
        tmin_display = launch - pd.Timedelta(minutes=5)
        tmax_display = launch + pd.Timedelta(minutes=130)

        # 1. Filter and shift radiation flux
        z = rc.loc[(rc["corr_time"] >= tmin_display - pd.Timedelta(seconds=time_shift)) &
                   (rc["corr_time"] <= tmax_display - pd.Timedelta(seconds=time_shift))].copy()
        z["t_min_shifted"] = (z["corr_time"] + pd.Timedelta(seconds=time_shift) - launch).dt.total_seconds() / 60.0

        # Plot Flux
        ax.plot(z["t_min_shifted"], z["flux"], color=color, marker='o', lw=1.5, alpha=0.9, label=f'Flux (shifted {time_shift:.1f}s)')
        ax.set_yscale('log')
        ax.set_ylabel(r"Flux [cm$^{-2}$ s$^{-1}$ sr$^{-1}$]", color=color)
        ax.tick_params(axis='y', labelcolor=color)
        ax.grid(which='both', alpha=0.3)
        ax.set_title(f"{label} Alignment (T-5 to T+30 min)")
        ax.set_xlim(-5, 30)

        # --- MODIFIED: Draw vertical event lines (black, dashed, labels at bottom) ---
        ymin, ymax = ax.get_ylim()
        for name, t in events.items():
            t_rel_min = (t - launch).total_seconds() / 60.0
            if -5 <= t_rel_min <= 130:
                ax.axvline(t_rel_min, linestyle="--", linewidth=1.2, color='black', alpha=0.8)
                # Placing text at the bottom (ymin)
                ax.text(t_rel_min, ymin * 1.1, name, rotation=90, va="bottom", ha="right",
                        fontsize=9, color='black', bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7))

        ax.legend(loc='upper left')

    axes[1].set_xlabel("Time since launch [minutes]")
    plt.tight_layout()
    plt.savefig("alignment_launch_simplified.png", dpi=300)
    plt.show()

    if 'df_dose' in globals():
        print("\n--- Flight Phase Dose Comparison Summary ---")
        display(df_dose)
else:
    print("Run peak fitting cell 02dfc3fa first.")
# %%
