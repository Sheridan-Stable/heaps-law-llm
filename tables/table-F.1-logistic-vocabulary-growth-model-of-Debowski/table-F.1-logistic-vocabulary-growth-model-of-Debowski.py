###
title: "table-F.1-logistic-vocabulary-growth-model-of-Debowski"
author: "Uyen 'Rachel' Lai and Paul Sheridan"
###

import os
import json
import csv
import random
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit

FILES = [
    ("PubMed_human_Close.json",                "Human"),
    ("PubMed_gptneo-125M_fewshot_Close.json", "GPT-Neo 125M"),
    ("PubMed_gptneo-1.3B_fewshot_Close.json", "GPT-Neo 1.3B"),
    ("PubMed_gptneo-2.7B_fewshot_Close.json", "GPT-Neo 2.7B"),
]

TOKEN_CAP_PER_SUBLIST = 225   
FIXED_SEEDS = [42, 123, 999]  # three shuffled versions per file, deterministic

OUT_DIR              = "analysis"
PLOT_LOGLOG          = "g_paper_fit_loglog.png"
PLOT_LINEAR          = "g_paper_fit_linear.png"
PARAMS_CSV           = "g_paper_params.csv"
PARAMS_SUMMARY_CSV   = "g_paper_params_summary.csv"
# ----------------------------------------

COLOR_MAP = {
    "Human":         "#D55E00",  # reddish
    "GPT-Neo 125M":  "#0072B2",  # blue
    "GPT-Neo 1.3B":  "#009E73",  # green
    "GPT-Neo 2.7B":  "#E69F00",  # orange
}
EMPIRICAL_GREY = "0.6"         


def g_paper(n, alpha, beta, gamma):

    n = np.asarray(n, dtype=float)
    n = np.maximum(n, 1.0)           
    nprime = np.exp(-alpha) * n
    # g = 2^((1-beta)/gamma) * n' / ( (n'^gamma + 1)^((1-beta)/gamma) )
    c = 2.0 ** ((1.0 - beta) / gamma)
    return c * nprime / ((np.power(nprime, gamma) + 1.0) ** ((1.0 - beta) / gamma))


def cumulative_NV_from_sublists(docs, cap_per_sublist, seed):

    docs = [sub for sub in docs if isinstance(sub, list) and sub]

    rng = random.Random(seed)
    rng.shuffle(docs)

    capped = [sub[:cap_per_sublist] for sub in docs]

    N = 0
    seen = set()
    NV = []
    for sub in capped:
        N += len(sub)
        seen.update(sub)
        NV.append([N, len(seen)])
    return np.array(NV, dtype=float), capped


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

def fit_g_paper(N, V):

    N = np.asarray(N, float)
    V = np.asarray(V, float)
    m = (N > 0) & (V > 0)
    x, y = N[m], V[m]
    if x.size < 5:
        return np.nan, np.nan, np.nan, np.nan

    lo = max(1, x.size // 10)
    hi = max(lo + 3, x.size * 8 // 10)
    b_guess = float(np.polyfit(np.log(x[lo:hi]), np.log(y[lo:hi]), 1)[0])
    b_guess = min(max(b_guess, 0.05), 0.95)

    g_guess = 0.5

    n0_guess = float(np.percentile(x, 40))
    a_guess = np.log(max(n0_guess, 1.0))

    p0 = [a_guess, b_guess, g_guess]
    bounds = ([-50.0, 1e-3, 1e-3], [50.0, 0.999, 5.0])

    popt, pcov = curve_fit(g_paper, x, y, p0=p0, bounds=bounds, maxfev=200000)
    alpha, beta, gamma = map(float, popt)   

    yhat = g_paper(x, alpha, beta, gamma)
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return alpha, beta, gamma, r2


def process_one_file(file_path, label, seed, rep_index):

    docs, fname = load_docs(file_path)
    NV, capped = cumulative_NV_from_sublists(docs, TOKEN_CAP_PER_SUBLIST, seed)
    N, V = NV[:, 0], NV[:, 1]

    all_words = [w for sub in capped for w in sub]
    stats = {
        "vocab_size": len(set(all_words)),
        "total_words": len(all_words),
        "singletons": sum(1 for c in Counter(all_words).values() if c == 1),
    }

    alpha, beta, gamma, r2 = fit_g_paper(N, V)
    return {
        "file": fname,
        "label": label,          # base label (e.g. "Human")
        "display_label": f"{label} (rep {rep_index})",
        "base_label": label,
        "replicate": rep_index,
        "seed": seed,
        "N": N,
        "V": V,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "R2": r2,
        **stats,
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    results = []
    for path, label in FILES:
        for rep_index, seed in enumerate(FIXED_SEEDS, start=1):
            res = process_one_file(path, label, seed, rep_index)
            results.append(res)
            print(
                f"{label} (rep {rep_index}, seed={seed}): "
                f"alpha={res['alpha']:.4f}, beta={res['beta']:.4f}, "
                f"gamma={res['gamma']:.4f}, R^2={res['R2']:.4f}, "
                f"N={int(res['N'][-1]):,}, V={int(res['V'][-1]):,}"
            )

    plt.figure(figsize=(6, 6))
    ax = plt.gca()

    seen_labels = set()

    for r in results:
        N, V = r["N"], r["V"]
        base_label = r["base_label"]

        ax.loglog(
            N,
            V,
            color=EMPIRICAL_GREY,
            linewidth=1.0,
            alpha=0.7,
        )

        nfit = np.logspace(np.log10(max(1.0, N.min())), np.log10(N.max()), 600)
        vfit = g_paper(nfit, r["alpha"], r["beta"], r["gamma"])

        if base_label not in seen_labels:
            fit_label = f"{base_label}: β={r['beta']:.3f}, γ={r['gamma']:.3f}"
            seen_labels.add(base_label)
        else:
            fit_label = None  # no extra legend entries

        ax.loglog(
            nfit,
            vfit,
            linestyle='-',
            linewidth=1.6,
            color=COLOR_MAP.get(base_label, "k"),
            label=fit_label,
        )

    ax.set_xlabel("Corpus size")
    ax.set_ylabel("Vocabulary size")
    ax.set_title("Closed vocabulary setting")
    ax.grid(True, which="both", linestyle=":", alpha=0.5)

    empirical_handle = Line2D(
        [0],
        [0],
        color=EMPIRICAL_GREY,
        linewidth=1.0,
        label="Empirical data",
    )
    fit_handles, fit_labels = ax.get_legend_handles_labels()
    handles = [empirical_handle] + fit_handles
    labels = ["Empirical data"] + fit_labels

    ax.legend(
        handles,
        labels,
        fontsize=7,
        frameon=True,
        framealpha=0.95,
        borderpad=0.3,
        labelspacing=0.2,
        handlelength=1.3,
        loc="lower right",
    )

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, PLOT_LOGLOG), dpi=220)
    plt.close()

    # -------- linear plot --------
    plt.figure(figsize=(6, 6))
    ax = plt.gca()

    seen_labels = set()

    for r in results:
        N, V = r["N"], r["V"]
        base_label = r["base_label"]

        ax.plot(
            N,
            V,
            color=EMPIRICAL_GREY,
            linewidth=0.9,
            alpha=0.7,
        )

        nfit = np.linspace(max(1.0, N.min()), N.max(), 600)
        vfit = g_paper(nfit, r["alpha"], r["beta"], r["gamma"])

        if base_label not in seen_labels:
            fit_label = f"{base_label}: β={r['beta']:.3f}, γ={r['gamma']:.3f}"
            seen_labels.add(base_label)
        else:
            fit_label = None

        ax.plot(
            nfit,
            vfit,
            linestyle='-',
            linewidth=1.6,
            color=COLOR_MAP.get(base_label, "k"),
            label=fit_label,
        )

    ax.set_xlabel("Corpus size")
    ax.set_ylabel("Vocabulary size")
    ax.set_title("Open vocabulary setting")
    ax.grid(True, linestyle=":", alpha=0.5)

    empirical_handle = Line2D(
        [0],
        [0],
        color=EMPIRICAL_GREY,
        linewidth=0.9,
        label="Empirical data",
    )
    fit_handles, fit_labels = ax.get_legend_handles_labels()
    handles = [empirical_handle] + fit_handles
    labels = ["Empirical data"] + fit_labels

    ax.legend(
        handles,
        labels,
        fontsize=7,
        frameon=True,
        framealpha=0.95,
        borderpad=0.3,
        labelspacing=0.2,
        handlelength=1.3,
        loc="lower right",
    )

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, PLOT_LINEAR), dpi=220)
    plt.close()

    csv_path = os.path.join(OUT_DIR, PARAMS_CSV)
    need_header = (not os.path.exists(csv_path)) or os.stat(csv_path).st_size == 0
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if need_header:
            w.writerow(
                [
                    "file_name",
                    "label",
                    "replicate",
                    "seed",
                    "alpha",
                    "beta",
                    "gamma",
                    "R2",
                    "vocab_size",
                    "total_words",
                    "singleton_count",
                ]
            )
        for r in results:
            w.writerow(
                [
                    r["file"],
                    r["label"],
                    r["replicate"],
                    r["seed"],
                    f"{r['alpha']:.6f}",
                    f"{r['beta']:.6f}",
                    f"{r['gamma']:.6f}",
                    f"{r['R2']:.6f}",
                    r["vocab_size"],
                    r["total_words"],
                    r["singletons"],
                ]
            )

    grouped = defaultdict(list)
    for r in results:
        grouped[r["label"]].append(r)

    summary_path = os.path.join(OUT_DIR, PARAMS_SUMMARY_CSV)
    need_header_sum = (not os.path.exists(summary_path)) or os.stat(summary_path).st_size == 0
    with open(summary_path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if need_header_sum:
            w.writerow(
                [
                    "label",
                    "n_reps",
                    "alpha_mean",
                    "alpha_sd",
                    "beta_mean",
                    "beta_sd",
                    "gamma_mean",
                    "gamma_sd",
                    "R2_mean",
                    "R2_sd",
                ]
            )

        print("\nSummary (mean ± sd over replicates):")
        for label, reps in grouped.items():
            alphas = np.array([x["alpha"] for x in reps], dtype=float)
            betas  = np.array([x["beta"]  for x in reps], dtype=float)
            gammas = np.array([x["gamma"] for x in reps], dtype=float)
            r2s    = np.array([x["R2"]    for x in reps], dtype=float)

            a_mean, a_sd = float(alphas.mean()), float(alphas.std(ddof=1))
            b_mean, b_sd = float(betas.mean()),  float(betas.std(ddof=1))
            g_mean, g_sd = float(gammas.mean()), float(gammas.std(ddof=1))
            r_mean, r_sd = float(r2s.mean()),    float(r2s.std(ddof=1))

            w.writerow(
                [
                    label,
                    len(reps),
                    f"{a_mean:.6f}",
                    f"{a_sd:.6f}",
                    f"{b_mean:.6f}",
                    f"{b_sd:.6f}",
                    f"{g_mean:.6f}",
                    f"{g_sd:.6f}",
                    f"{r_mean:.6f}",
                    f"{r_sd:.6f}",
                ]
            )

            print(
                f"  {label}: "
                f"alpha = {a_mean:.4f} ± {a_sd:.4f}, "
                f"beta = {b_mean:.4f} ± {b_sd:.4f}, "
                f"gamma = {g_mean:.4f} ± {g_sd:.4f}, "
                f"R^2 = {r_mean:.5f} ± {r_sd:.5f}"
            )

    print("\nSaved:")
    print(f"  {os.path.join(OUT_DIR, PLOT_LOGLOG)}")
    print(f"  {os.path.join(OUT_DIR, PLOT_LINEAR)}")
    print(f"  {csv_path}")
    print(f"  {summary_path}")


if __name__ == "__main__":
    main()
