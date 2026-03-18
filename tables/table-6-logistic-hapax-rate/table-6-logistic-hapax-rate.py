

import os
import json
import random
from pathlib import Path
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

FILES = [
    ("PubMed_human_Open.json",                "Human"),
    ("PubMed_gptneo-125M_fewshot_Open.json", "GPT-Neo 125M"),
    ("PubMed_gptneo-1.3B_fewshot_Open.json", "GPT-Neo 1.3B"),
    ("PubMed_gptneo-2.7B_fewshot_Open.json", "GPT-Neo 2.7B"),
]

TOKEN_CAP_PER_SUBLIST = 225
RANDOM_SEED = 42
N_TRIALS = 3

OUT_DIR      = "analysis"
PLOT_HAP_LOG = "hapax_logistic_all_open_logN.png"   # hapax vs log N
PLOT_HAP_LIN = "hapax_logistic_all_open_N.png"      # hapax vs N
PARAM_CSV    = "hapax_logistic_params_open.csv"

os.makedirs(OUT_DIR, exist_ok=True)
# 


def h_logistic_u(u, alpha_h, beta_h, gamma_h):
    """
    Logistic hapax-rate model:

        h(u) = beta_h + (1 - beta_h) / (1 + exp(gamma_h * (u - alpha_h)))
    """
    u = np.asarray(u, dtype=float)
    return beta_h + (1.0 - beta_h) / (1.0 + np.exp(gamma_h * (u - alpha_h)))


def load_docs(path):

    p = Path(path)
    if not p.exists() and Path(str(p) + ".json").exists():
        p = Path(str(p) + ".json")
    if not p.exists():
        raise FileNotFoundError(p)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{p} is not list[list[str]].")
    return data, p.name


def cumulative_hapax_rate(docs, cap_per_sublist, seed):
    docs = list(docs)  # copy so we don't mutate original

    random.seed(seed)
    random.shuffle(docs)  # shuffle SUBLISTS

    capped = []
    for sub in docs:
        if not isinstance(sub, list):
            continue
        if not sub:
            continue
        capped.append(sub[:cap_per_sublist])

    counts = Counter()
    N_list, H_list, U_list = [], [], []
    N = 0

    for sub in capped:
        for w in sub:
            N += 1
            counts[w] += 1

        V = len(counts)
        if V > 0:
            hapax = sum(1 for c in counts.values() if c == 1)
            hapax_rate = hapax / V
        else:
            hapax_rate = np.nan

        N_list.append(float(N))
        H_list.append(float(hapax_rate))
        U_list.append(float(np.log(max(N, 1))))  # natural log

    N_arr = np.array(N_list, dtype=float)
    H_arr = np.array(H_list, dtype=float)
    U_arr = np.array(U_list, dtype=float)
    return N_arr, H_arr, U_arr


def fit_hapax_logistic(U, H):

    U = np.asarray(U, float)
    H = np.asarray(H, float)

    m = np.isfinite(U) & np.isfinite(H) & (H > 0) & (H < 1)
    u_data = U[m]
    h_data = H[m]

    if u_data.size < 10:
        raise RuntimeError("Not enough usable points to fit hapax model.")

    k_tail = max(5, u_data.size // 5)
    beta_guess = float(np.median(h_data[-k_tail:]))
    beta_guess = float(np.clip(beta_guess, 0.01, 0.99))

    target_mid = 0.5 * (1.0 + beta_guess)
    idx_mid = int(np.argmin(np.abs(h_data - target_mid)))
    alpha_guess = float(u_data[idx_mid])

    gamma_guess = 1.0  # modest starting slope

    p0 = [alpha_guess, beta_guess, gamma_guess]
    bounds = ([-50.0, 1e-3, 1e-3], [50.0, 0.999, 10.0])

    popt, pcov = curve_fit(
         h_logistic_u
    c_u,
        u_data,
        h_data,
        p0=p0,
        bounds=bounds,
        maxfev=200000
    )
    alpha_h, beta_h, gamma_h = map(float, popt)

    h_hat = h_logistic_u(u_data, alpha_h, beta_h, gamma_h)
    ss_res = float(np.sum((h_data - h_hat) ** 2))
    ss_tot = float(np.sum((h_data - np.mean(h_data)) ** 2))
    R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return alpha_h, beta_h, gamma_h, R2


def main():
    results = []   
    curves  = []

    for path, label in FILES:
        docs, fname = load_docs(path)
        print(f"Processing {label} from {fname} ...")

        params_trials = []
        N_all = []
        U_all = []
        H_all = []

        seeds = [RANDOM_SEED + i for i in range(N_TRIALS)]

        for trial_idx, seed in enumerate(seeds, start=1):
            print(f"  Trial {trial_idx} with seed={seed}")
            N, H_emp, U = cumulative_hapax_rate(
                docs,
                cap_per_sublist=TOKEN_CAP_PER_SUBLIST,
                seed=seed
            )

            alpha_h, beta_h, gamma_h, R2 = fit_hapax_logistic(U, H_emp)
            params_trials.append((alpha_h, beta_h, gamma_h, R2))

            N_all.append(N)
            U_all.append(U)
            H_all.append(H_emp)

            print(
                f"    {label} trial {trial_idx} (hapax-fit): "
                f"alpha_h={alpha_h:.4f}, beta_h={beta_h:.4f}, "
                f"gamma_h={gamma_h:.4f}, R^2={R2:.4f}"
            )

        params_trials = np.array(params_trials)  
        alphas = params_trials[:, 0]
        betas  = params_trials[:, 1]
        gammas = params_trials[:, 2]
        R2s    = params_trials[:, 3]

        alpha_mean, alpha_sd = float(alphas.mean()), float(alphas.std(ddof=1))
        beta_mean,  beta_sd  = float(betas.mean()),  float(betas.std(ddof=1))
        gamma_mean, gamma_sd = float(gammas.mean()), float(gammas.std(ddof=1))
        R2_mean, R2_sd       = float(R2s.mean()),    float(R2s.std(ddof=1))

        N_all_concat = np.concatenate(N_all)
        U_all_concat = np.concatenate(U_all)
        H_all_concat = np.concatenate(H_all)

        print(
            f"{label} (mean over {N_TRIALS} trials): "
            f"alpha_h={alpha_mean:.4f} ± {alpha_sd:.4f}, "
            f"beta_h={beta_mean:.4f} ± {beta_sd:.4f}, "
            f"gamma_h={gamma_mean:.4f} ± {gamma_sd:.4f}, "
            f"R^2={R2_mean:.4f} ± {R2_sd:.4f}"
        )

        results.append({
            "file": fname,
            "label": label,
            "alpha_h_mean": alpha_mean,
            "alpha_h_sd": alpha_sd,
            "beta_h_mean": beta_mean,
            "beta_h_sd": beta_sd,
            "gamma_h_mean": gamma_mean,
            "gamma_h_sd": gamma_sd,
            "R2_mean": R2_mean,
            "R2_sd": R2_sd,
            "N_max": int(N_all_concat.max()),
            "U_min": float(U_all_concat.min()),
            "U_max": float(U_all_concat.max())
        })

        curves.append((label, N_all_concat, U_all_concat, H_all_concat,
                       alpha_mean, beta_mean, gamma_mean))

    plt.figure(figsize=(10, 6))

    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

    for (label, N_all_concat, U_all_concat, H_all_concat,
         alpha_h, beta_h, gamma_h), color in zip(curves, colors):

        plt.scatter(
            U_all_concat, H_all_concat,
            s=4,
            alpha=0.25,
            color=color,
        )
        u_grid = np.linspace(float(U_all_concat.min()), float(U_all_concat.max()), 600)
        h_model = h_logistic_u(u_grid, alpha_h, beta_h, gamma_h)
        plt.plot(
            u_grid, h_model,
            linewidth=2,
            color=color,
            label=f"{label}"
        )

    plt.xlabel("log N")
    plt.ylabel("hapax rate  (#hapax / V)")
    plt.title("Logistic hapax-rate fits (independent, 3-trial mean) — PubMed Human vs GPT-Neo — log N")
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    fig_path_log = os.path.join(OUT_DIR, PLOT_HAP_LOG)
    plt.savefig(fig_path_log, dpi=220)
    plt.close()

    plt.figure(figsize=(10, 6))

    for (label, N_all_concat, U_all_concat, H_all_concat,
         alpha_h, beta_h, gamma_h), color in zip(curves, colors):

        plt.scatter(
            N_all_concat, H_all_concat,
            s=4,
            alpha=0.25,
            color=color,
        )
        n_grid = np.linspace(float(N_all_concat.min()), float(N_all_concat.max()), 600)
        u_grid = np.log(n_grid)
        h_model = h_logistic_u(u_grid, alpha_h, beta_h, gamma_h)
        plt.plot(
            n_grid, h_model,
            linewidth=2,
            color=color,
            label=f"{label}"
        )

    plt.xlabel("N  (tokens)")
    plt.ylabel("hapax rate  (#hapax / V)")
    plt.title("Logistic hapax-rate fits (independent, 3-trial mean) — PubMed Human vs GPT-Neo — linear N")
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    fig_path_lin = os.path.join(OUT_DIR, PLOT_HAP_LIN)
    plt.savefig(fig_path_lin, dpi=220)
    plt.close()

    import csv
    csv_path = os.path.join(OUT_DIR, PARAM_CSV)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "file_name", "label",
            "alpha_h_mean", "alpha_h_sd",
            "beta_h_mean",  "beta_h_sd",
            "gamma_h_mean", "gamma_h_sd",
            "R2_mean",      "R2_sd",
            "N_max", "U_min", "U_max"
        ])
        for r in results:
            w.writerow([
                r["file"], r["label"],
                f"{r['alpha_h_mean']:.6f}",
                f"{r['alpha_h_sd']:.6f}",
                f"{r['beta_h_mean']:.6f}",
                f"{r['beta_h_sd']:.6f}",
                f"{r['gamma_h_mean']:.6f}",
                f"{r['gamma_h_sd']:.6f}",
                f"{r['R2_mean']:.6f}",
                f"{r['R2_sd']:.6f}",
                r["N_max"],
                f"{r['U_min']:.6f}",
                f"{r['U_max']:.6f}",
            ])

    print("\nSaved:")
    print(" ", fig_path_log)
    print(" ", fig_path_lin)
    print(" ", csv_path)


if __name__ == "__main__":
    main()
