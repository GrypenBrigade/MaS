"""
Steady-State Simulation: M/M/1 Queue
Applies: Replication/Deletion, Batch Means, and Welch Methods
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

# ─────────────────────────────────────────────
# SIMULATION: M/M/1 Queue
# ─────────────────────────────────────────────
# Arrival rate λ, Service rate μ, utilization ρ = λ/μ
# Theoretical steady-state mean wait = ρ / (μ - λ)

LAMBDA = 0.8   # arrival rate
MU     = 1.0   # service rate
RHO    = LAMBDA / MU
THEORETICAL_MEAN = RHO / (MU - LAMBDA)   # = 4.0 minutes

print(f"M/M/1 Queue  |  λ={LAMBDA}, μ={MU}, ρ={RHO}")
print(f"Theoretical steady-state mean wait: {THEORETICAL_MEAN:.4f} min\n")


def mm1_queue(n_customers: int, rng: np.random.Generator) -> np.ndarray:
    """
    Simulate M/M/1 queue and return waiting times for each customer.
    Uses interarrival ~ Exp(λ), service ~ Exp(μ).
    """
    interarrivals = rng.exponential(1 / LAMBDA, n_customers)
    services      = rng.exponential(1 / MU,     n_customers)

    arrival_times  = np.cumsum(interarrivals)
    wait_times     = np.zeros(n_customers)
    departure_times = np.zeros(n_customers)

    departure_times[0] = arrival_times[0] + services[0]
    for i in range(1, n_customers):
        start = max(arrival_times[i], departure_times[i - 1])
        wait_times[i]      = start - arrival_times[i]
        departure_times[i] = start + services[i]

    return wait_times


# ═══════════════════════════════════════════════════════════════
# METHOD 1 — REPLICATION / DELETION
# ═══════════════════════════════════════════════════════════════
def replication_deletion(n_reps: int, n_customers: int, warmup: int,
                         seed: int = 42):
    """
    Run n_reps independent replications, discard first `warmup`
    customers from each, return per-replication means.
    """
    rng = np.random.default_rng(seed)
    rep_means = []
    all_reps  = []

    for _ in range(n_reps):
        waits = mm1_queue(n_customers, rng)
        all_reps.append(waits)
        rep_means.append(waits[warmup:].mean())

    rep_means = np.array(rep_means)
    grand_mean = rep_means.mean()
    se = rep_means.std(ddof=1) / np.sqrt(n_reps)
    t_crit = stats.t.ppf(0.975, df=n_reps - 1)
    ci = (grand_mean - t_crit * se, grand_mean + t_crit * se)

    return grand_mean, ci, rep_means, all_reps


# ═══════════════════════════════════════════════════════════════
# METHOD 2 — BATCH MEANS
# ═══════════════════════════════════════════════════════════════
def batch_means(n_customers: int, warmup: int, n_batches: int,
                seed: int = 99):
    """
    Single long run; discard warmup; split into n_batches of equal size.
    Check lag-1 autocorrelation of batch means.
    """
    rng   = np.random.default_rng(seed)
    waits = mm1_queue(n_customers, rng)
    trimmed = waits[warmup:]

    batch_size = len(trimmed) // n_batches
    usable     = batch_size * n_batches
    batches    = trimmed[:usable].reshape(n_batches, batch_size)
    b_means    = batches.mean(axis=1)

    grand_mean = b_means.mean()
    se = b_means.std(ddof=1) / np.sqrt(n_batches)
    t_crit = stats.t.ppf(0.975, df=n_batches - 1)
    ci = (grand_mean - t_crit * se, grand_mean + t_crit * se)

    # Lag-1 autocorrelation of batch means
    lag1 = np.corrcoef(b_means[:-1], b_means[1:])[0, 1]

    return grand_mean, ci, b_means, waits, batch_size, lag1


# ═══════════════════════════════════════════════════════════════
# METHOD 3 — WELCH METHOD (warmup detection)
# ═══════════════════════════════════════════════════════════════
def welch_method(n_reps: int, n_customers: int, window: int, seed: int = 7):
    """
    Multiple replications → ensemble average at each index →
    moving average to smooth → identify stabilisation point.
    """
    rng  = np.random.default_rng(seed)
    reps = np.array([mm1_queue(n_customers, rng) for _ in range(n_reps)])

    # Ensemble mean at each customer index
    ensemble = reps.mean(axis=0)

    # Moving average (symmetric window, truncated at edges)
    n = len(ensemble)
    smoothed = np.zeros(n)
    for i in range(n):
        lo = max(0, i - window)
        hi = min(n, i + window + 1)
        smoothed[i] = ensemble[lo:hi].mean()

    # Detect warmup: first index where smoothed stays within 5% of
    # its own long-run average (last 20% of the series)
    long_run = smoothed[int(0.8 * n):].mean()
    tol = 0.05 * long_run
    stable_idx = n // 2   # fallback
    for i in range(n):
        if np.all(np.abs(smoothed[i:] - long_run) < tol):
            stable_idx = i
            break

    return ensemble, smoothed, stable_idx, long_run


# ─────────────────────────────────────────────
# RUN ALL THREE METHODS
# ─────────────────────────────────────────────
N_REPS      = 20
N_CUSTOMERS = 5_000
WARMUP      = 500
N_BATCHES   = 30
WINDOW      = 30          # Welch moving-average half-width
LONG_RUN    = 50_000      # customers for single batch-means run

print("=" * 55)
print("METHOD 1 — REPLICATION / DELETION")
print("=" * 55)
rd_mean, rd_ci, rd_rep_means, rd_all_reps = replication_deletion(
    N_REPS, N_CUSTOMERS, WARMUP)
print(f"  Replications    : {N_REPS}")
print(f"  Customers/rep   : {N_CUSTOMERS}  |  Warmup: {WARMUP}")
print(f"  Grand mean      : {rd_mean:.4f}")
print(f"  95% CI          : ({rd_ci[0]:.4f}, {rd_ci[1]:.4f})")
print(f"  Theoretical     : {THEORETICAL_MEAN:.4f}\n")

print("=" * 55)
print("METHOD 2 — BATCH MEANS")
print("=" * 55)
bm_mean, bm_ci, bm_batch_means, bm_waits, bm_bsize, bm_lag1 = batch_means(
    LONG_RUN, WARMUP, N_BATCHES)
print(f"  Total customers : {LONG_RUN}  |  Warmup: {WARMUP}")
print(f"  Batches         : {N_BATCHES}  |  Batch size: {bm_bsize}")
print(f"  Grand mean      : {bm_mean:.4f}")
print(f"  95% CI          : ({bm_ci[0]:.4f}, {bm_ci[1]:.4f})")
print(f"  Lag-1 autocorr  : {bm_lag1:.4f}  (want ≈ 0)")
print(f"  Theoretical     : {THEORETICAL_MEAN:.4f}\n")

print("=" * 55)
print("METHOD 3 — WELCH METHOD")
print("=" * 55)
wl_ens, wl_smooth, wl_d, wl_lr = welch_method(N_REPS, N_CUSTOMERS, WINDOW)
print(f"  Replications    : {N_REPS}")
print(f"  Moving avg win  : ±{WINDOW}")
print(f"  Suggested warmup: {wl_d} customers")
print(f"  Long-run avg    : {wl_lr:.4f}")
print(f"  Theoretical     : {THEORETICAL_MEAN:.4f}\n")


# ─────────────────────────────────────────────
# PLOTTING
# ─────────────────────────────────────────────
DARK   = "#0f1117"
PANEL  = "#1a1d27"
BORDER = "#2a2d3a"
ACCENT = "#4f9cf9"     # blue
GREEN  = "#3ecf8e"     # green
AMBER  = "#f5a623"     # amber
RED    = "#f75f5f"
WHITE  = "#e8eaf0"
MUTED  = "#7c7f8e"

plt.rcParams.update({
    "figure.facecolor":  DARK,
    "axes.facecolor":    PANEL,
    "axes.edgecolor":    BORDER,
    "axes.labelcolor":   WHITE,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
    "text.color":        WHITE,
    "grid.color":        BORDER,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "font.family":       "monospace",
})

fig = plt.figure(figsize=(18, 14), facecolor=DARK)
fig.suptitle("Steady-State Simulation  ·  M/M/1 Queue  (λ=0.8, μ=1.0)",
             fontsize=16, color=WHITE, fontweight="bold", y=0.98)

gs = gridspec.GridSpec(3, 3, figure=fig,
                       hspace=0.55, wspace=0.38,
                       top=0.93, bottom=0.06,
                       left=0.07, right=0.97)


# ── Helper ──────────────────────────────────
def style_ax(ax, title, xlabel, ylabel):
    ax.set_title(title, color=WHITE, fontsize=10, pad=8)
    ax.set_xlabel(xlabel, color=MUTED, fontsize=8)
    ax.set_ylabel(ylabel, color=MUTED, fontsize=8)
    ax.grid(True)
    ax.tick_params(labelsize=7)


def draw_theoretical(ax):
    ax.axhline(THEORETICAL_MEAN, color=RED, lw=1.4,
               ls="--", label=f"Theoretical ({THEORETICAL_MEAN:.2f})")


# ══════════════════════════════════════
# ROW 0  —  REPLICATION / DELETION
# ══════════════════════════════════════

# 0-A: All replications (raw traces, first 300 customers)
ax0a = fig.add_subplot(gs[0, 0])
for i, rep in enumerate(rd_all_reps[:8]):
    ax0a.plot(rep[:300], lw=0.6, alpha=0.55,
              color=plt.cm.cool(i / 8))
ax0a.axvline(WARMUP, color=AMBER, lw=1.5, ls="--",
             label=f"Warmup = {WARMUP}")
draw_theoretical(ax0a)
ax0a.set_xlim(0, 300)
ax0a.set_ylim(0, 35)
ax0a.legend(fontsize=6, loc="upper right")
style_ax(ax0a,
         "Rep/Deletion · Raw Traces (8 reps)",
         "Customer Index", "Wait Time (min)")

# 0-B: Per-replication means + grand mean
ax0b = fig.add_subplot(gs[0, 1])
x_reps = np.arange(1, N_REPS + 1)
ax0b.bar(x_reps, rd_rep_means, color=ACCENT, alpha=0.75, width=0.6)
ax0b.axhline(rd_mean, color=GREEN, lw=1.8,
             label=f"Grand mean={rd_mean:.3f}")
ax0b.fill_between([0.5, N_REPS + 0.5], rd_ci[0], rd_ci[1],
                  color=GREEN, alpha=0.12, label="95% CI")
draw_theoretical(ax0b)
ax0b.legend(fontsize=6)
ax0b.set_xlim(0.5, N_REPS + 0.5)
style_ax(ax0b,
         "Rep/Deletion · Per-Rep Means",
         "Replication #", "Mean Wait (min)")

# 0-C: CI comparison bar
ax0c = fig.add_subplot(gs[0, 2])
methods = ["Rep/Del", "Batch\nMeans", "Theoretical"]
means   = [rd_mean,  bm_mean,  THEORETICAL_MEAN]
ci_lo   = [rd_ci[0], bm_ci[0], THEORETICAL_MEAN]
ci_hi   = [rd_ci[1], bm_ci[1], THEORETICAL_MEAN]
colors  = [ACCENT, GREEN, RED]
for j, (m, lo, hi, c, lbl) in enumerate(
        zip(means, ci_lo, ci_hi, colors, methods)):
    ax0c.barh(j, hi - lo, left=lo, height=0.4, color=c, alpha=0.35)
    ax0c.plot([m], [j], "o", color=c, ms=7, label=lbl)
    ax0c.text(hi + 0.05, j, f"{m:.3f}", va="center",
              fontsize=7, color=c)
ax0c.set_yticks(range(3))
ax0c.set_yticklabels(methods, fontsize=8)
ax0c.legend(fontsize=6, loc="lower right")
style_ax(ax0c,
         "CI Comparison — All Methods",
         "Mean Wait (min)", "")
ax0c.grid(True, axis="x")
ax0c.grid(False, axis="y")

# ══════════════════════════════════════
# ROW 1  —  BATCH MEANS
# ══════════════════════════════════════

# 1-A: Full single run with warmup + batch boundaries
ax1a = fig.add_subplot(gs[1, 0])
display_n = min(5000, LONG_RUN)
ax1a.plot(bm_waits[:display_n], lw=0.4, color=GREEN, alpha=0.6)
ax1a.axvline(WARMUP, color=AMBER, lw=1.5, ls="--",
             label=f"Warmup = {WARMUP}")
draw_theoretical(ax1a)
ax1a.legend(fontsize=6)
ax1a.set_xlim(0, display_n)
style_ax(ax1a,
         f"Batch Means · Single Run (first {display_n:,} shown)",
         "Customer Index", "Wait Time (min)")

# 1-B: Batch means across the 30 batches
ax1b = fig.add_subplot(gs[1, 1])
x_b = np.arange(1, N_BATCHES + 1)
ax1b.bar(x_b, bm_batch_means, color=GREEN, alpha=0.75, width=0.6)
ax1b.axhline(bm_mean, color=ACCENT, lw=1.8,
             label=f"Grand mean={bm_mean:.3f}")
ax1b.fill_between([0.5, N_BATCHES + 0.5], bm_ci[0], bm_ci[1],
                  color=ACCENT, alpha=0.12, label="95% CI")
draw_theoretical(ax1b)
ax1b.legend(fontsize=6)
ax1b.set_xlim(0.5, N_BATCHES + 0.5)
style_ax(ax1b,
         f"Batch Means · {N_BATCHES} Batches (size={bm_bsize:,})",
         "Batch #", "Batch Mean Wait (min)")

# 1-C: Lag-1 autocorrelation scatter
ax1c = fig.add_subplot(gs[1, 2])
ax1c.scatter(bm_batch_means[:-1], bm_batch_means[1:],
             color=GREEN, alpha=0.65, s=30, edgecolors=BORDER, lw=0.5)
# Fit line
m_fit, b_fit, *_ = stats.linregress(bm_batch_means[:-1], bm_batch_means[1:])
xs = np.linspace(bm_batch_means.min(), bm_batch_means.max(), 50)
ax1c.plot(xs, m_fit * xs + b_fit, color=AMBER, lw=1.4,
          label=f"Lag-1 r = {bm_lag1:.3f}")
ax1c.legend(fontsize=7)
style_ax(ax1c,
         "Batch Means · Lag-1 Autocorrelation",
         "Batch Mean (i)", "Batch Mean (i+1)")

# ══════════════════════════════════════
# ROW 2  —  WELCH METHOD
# ══════════════════════════════════════

# 2-A: All replications + ensemble average
ax2a = fig.add_subplot(gs[2, 0])
x_cust = np.arange(N_CUSTOMERS)
for i, rep in enumerate(
        np.random.default_rng(7).permutation(
            np.array([mm1_queue(N_CUSTOMERS,
                                np.random.default_rng(7 + i))
                      for i in range(N_REPS)]))[:6]):
    ax2a.plot(x_cust[:800], rep[:800], lw=0.5, alpha=0.3,
              color=AMBER)
ax2a.plot(x_cust[:800], wl_ens[:800], color=WHITE, lw=1.3,
          label="Ensemble mean")
ax2a.axvline(wl_d, color=RED, lw=1.5, ls="--",
             label=f"Detected warmup={wl_d}")
ax2a.legend(fontsize=6)
style_ax(ax2a,
         "Welch · Raw Reps + Ensemble Mean",
         "Customer Index (first 800)", "Wait Time (min)")

# 2-B: Smoothed ensemble + warmup detection
ax2b = fig.add_subplot(gs[2, 1])
ax2b.plot(x_cust, wl_ens, color=MUTED, lw=0.6, alpha=0.5,
          label="Ensemble mean (raw)")
ax2b.plot(x_cust, wl_smooth, color=AMBER, lw=2.0,
          label=f"Smoothed (w=±{WINDOW})")
ax2b.axhline(wl_lr, color=GREEN, lw=1.3, ls=":",
             label=f"Long-run avg={wl_lr:.3f}")
ax2b.axvline(wl_d, color=RED, lw=1.5, ls="--",
             label=f"d* = {wl_d}")
ax2b.fill_betweenx([0, 30], 0, wl_d,
                   color=RED, alpha=0.07, label="Warmup zone")
draw_theoretical(ax2b)
ax2b.set_ylim(0, 25)
ax2b.legend(fontsize=6, loc="upper right")
style_ax(ax2b,
         "Welch · Moving Average + Warmup Detection",
         "Customer Index", "Mean Wait (min)")

# 2-C: Absolute deviation from long-run (log scale)
ax2c = fig.add_subplot(gs[2, 2])
deviation = np.abs(wl_smooth - wl_lr)
ax2c.semilogy(x_cust, deviation + 1e-6, color=AMBER, lw=1.2)
ax2c.axvline(wl_d, color=RED, lw=1.5, ls="--",
             label=f"d* = {wl_d}")
ax2c.axhline(0.05 * wl_lr, color=GREEN, lw=1.2, ls=":",
             label="5% tolerance")
ax2c.legend(fontsize=7)
style_ax(ax2c,
         "Welch · |Smoothed − Long-Run| (log scale)",
         "Customer Index", "|Deviation| (min)")

# ── Row labels on left margin ────────────
label_props = dict(color=WHITE, fontsize=11, fontweight="bold",
                   ha="center", va="center", rotation=90,
                   bbox=dict(facecolor=BORDER, edgecolor="none",
                             boxstyle="round,pad=0.4"))
for row, txt in enumerate(["METHOD 1\nRep/Deletion",
                            "METHOD 2\nBatch Means",
                            "METHOD 3\nWelch"]):
    fig.text(0.012, 0.82 - row * 0.31, txt, **label_props)

plt.savefig("steady_state_simulation.png",
            dpi=150, bbox_inches="tight", facecolor=DARK)
print("Plot saved to steady_state_simulation.png")