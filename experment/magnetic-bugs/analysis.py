"""
Deeper analysis of the magnetic bug navigation model.

Probes the parameter regime where compass model differences matter:
near the navigation phase boundary where Peclet number ~ O(1).

Usage:
    python analysis.py --peclet           # Peclet number study
    python analysis.py --differentiate    # Model comparison at the boundary
    python analysis.py --harmonics        # Spherical harmonic decomposition
    python analysis.py --critical-noise   # Critical noise per model
    python analysis.py --all              # Everything
"""

import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from landscape import Landscape
from compass import singlet_yield, CompassSensor
from ring_attractor import RingAttractor
from sim import make_quantum_compass, _ensure_spin_dynamics


# ── Vectorised fast simulation ─────────────────────────────────────
# The per-step Python loop in agent.py is the bottleneck for sweeps.
# This fast path skips the ring attractor and simulates the OU heading
# process directly, using the compass contrast as a parameter.
#
# The heading evolves as:
#   θ_{t+1} = θ_t + κ sin(θ_goal - θ_t + η_compass) dt + σ_θ √dt ξ
#
# where η_compass is the compass heading error.  For an N_cry sensor
# array with contrast C and per-molecule noise σ_sensor, the compass
# heading error std is approximately:
#   σ_compass ≈ 1 / (C * √N_cry * SNR_per_molecule)
#
# This is an OU process on the circle.  We simulate it with Euler-
# Maruyama for N_bugs in parallel (fully vectorised).

def fast_ensemble(n_bugs, duration, dt, kappa, sigma_theta,
                  contrast, n_cry, sigma_sensor, goal=3*np.pi/4,
                  speed=1.0, sigma_xy=0.05, seed=0):
    """Vectorised simulation of n_bugs navigating bugs.

    Returns mean heading error (degrees) and array of final distances.
    """
    rng = np.random.default_rng(seed)
    n_steps = int(duration / dt)
    sqrt_dt = np.sqrt(dt)

    # Initial conditions
    theta = rng.uniform(0, 2*np.pi, n_bugs)
    x = np.full(n_bugs, 500.0)
    y = np.full(n_bugs, 100.0)

    # Compass noise: approximate the compass heading error
    # The sensor array gives N_cry readings with noise σ_sensor.
    # The compass heading estimate has std ≈ σ_sensor / (C * mean * √(N_cry/n_ch))
    # For the ring attractor in the stable regime, this propagates roughly as-is.
    mean_yield = 0.5
    delta = contrast * mean_yield
    n_per_ch = n_cry / 8.0
    # Fisher information for cos 2α signal with Gaussian noise:
    # I(α) ∝ (dΦ/dα)² / σ² = (2δ sin 2α)² / (σ²/N_per_ch)
    # Averaged over α: <sin² 2α> = 1/2
    # → σ_heading ≈ σ_sensor / (δ * √(2 * N_per_ch))
    sigma_compass = sigma_sensor / (delta * np.sqrt(2 * n_per_ch)) if delta > 1e-10 else 10.0

    # Accumulate heading error for mean
    heading_errors_sum = np.zeros(n_bugs)

    for _ in range(n_steps):
        # Compass-corrupted heading estimate
        compass_noise = rng.normal(0, sigma_compass, n_bugs)
        heading_est = theta + compass_noise

        # Steering
        heading_error = goal - heading_est
        d_theta = kappa * np.sin(heading_error) * dt
        d_theta += sigma_theta * sqrt_dt * rng.standard_normal(n_bugs)
        theta = (theta + d_theta) % (2 * np.pi)

        # Position
        x += speed * np.cos(theta) * dt + sigma_xy * sqrt_dt * rng.standard_normal(n_bugs)
        y += speed * np.sin(theta) * dt + sigma_xy * sqrt_dt * rng.standard_normal(n_bugs)

        # Track heading error
        err = np.abs(((theta - goal) + np.pi) % (2*np.pi) - np.pi)
        heading_errors_sum += err

    mean_err_per_bug = heading_errors_sum / n_steps
    distances = np.sqrt((x - 500)**2 + (y - 100)**2)

    return np.degrees(np.mean(mean_err_per_bug)), distances


# ── 1. Peclet number study ─────────────────────────────────────────

def peclet_study(save_prefix=None):
    """Compare analytical Peclet number against simulated navigation."""
    kappa = 2.0
    L = 300.0
    sigma_range = np.logspace(-1.5, 0.7, 25)

    Pe_analytical = kappa * L / sigma_range**2

    n_bugs = 100
    duration = 200
    dt = 0.02

    mean_errors = []
    success_rates = []

    for sig in sigma_range:
        err, _ = fast_ensemble(
            n_bugs=n_bugs, duration=duration, dt=dt,
            kappa=kappa, sigma_theta=sig,
            contrast=0.15, n_cry=1000, sigma_sensor=0.02)
        # Re-run for success rate
        _, dists = fast_ensemble(
            n_bugs=n_bugs, duration=duration, dt=dt,
            kappa=kappa, sigma_theta=sig,
            contrast=0.15, n_cry=1000, sigma_sensor=0.02, seed=1)
        mean_errors.append(err)
        # Success: error < 15°
        # Use error from the run
        errs_individual, _ = fast_ensemble(
            n_bugs=n_bugs, duration=duration, dt=dt,
            kappa=kappa, sigma_theta=sig,
            contrast=0.15, n_cry=1000, sigma_sensor=0.02, seed=2)
        success_rates.append(1.0 if err < 15 else max(0, 1.0 - (err - 15)/75))
        print(f'  σ_θ={sig:.3f}  Pe={kappa*L/sig**2:.0f}  err={err:.1f}°')

    mean_errors = np.array(mean_errors)
    success_rates = np.array(success_rates)

    # Better success rate: run the ensemble and check individual bugs
    success_rates_real = []
    for sig in sigma_range:
        rng = np.random.default_rng(42)
        n_steps = int(duration / dt)
        sqrt_dt = np.sqrt(dt)
        theta = rng.uniform(0, 2*np.pi, n_bugs)
        goal = 3*np.pi/4
        err_sum = np.zeros(n_bugs)
        sigma_compass = 0.02 / (0.15 * 0.5 * np.sqrt(2 * 1000/8))
        for _ in range(n_steps):
            cn = rng.normal(0, sigma_compass, n_bugs)
            he = goal - (theta + cn)
            theta = (theta + kappa * np.sin(he) * dt +
                     sig * sqrt_dt * rng.standard_normal(n_bugs)) % (2*np.pi)
            err_sum += np.abs(((theta - goal) + np.pi) % (2*np.pi) - np.pi)
        per_bug = np.degrees(err_sum / n_steps)
        success_rates_real.append(np.mean(per_bug < 15))
    success_rates_real = np.array(success_rates_real)

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    ax = axes[0]
    ax.loglog(sigma_range, Pe_analytical, 'b-', lw=2,
              label=r'$Pe = \kappa L / \sigma_\theta^2$')
    ax.axhline(1, color='red', ls='--', lw=1.5, label='Pe = 1')
    ax.axhline(10, color='orange', ls=':', lw=1.5, label='Pe = 10')
    ax.set_xlabel(r'$\sigma_\theta$ (rad/$\sqrt{s}$)')
    ax.set_ylabel('Peclet number')
    ax.set_title('Peclet Number')
    ax.legend(fontsize=9)

    ax = axes[1]
    ax.semilogx(Pe_analytical, mean_errors, 'ko-', ms=4)
    ax.axhline(10, color='green', ls='--', lw=1, label=r'$10°$')
    ax.axhline(30, color='orange', ls='--', lw=1, label=r'$30°$')
    ax.axhline(90, color='red', ls=':', lw=1, alpha=0.5, label=r'$90°$ (random)')
    ax.axvline(1, color='red', ls='--', lw=1, alpha=0.3)
    ax.set_xlabel('Peclet number')
    ax.set_ylabel('Mean heading error (°)')
    ax.set_title('Navigation Accuracy vs Pe')
    ax.legend(fontsize=9)
    ax.set_ylim(0, 95)

    ax = axes[2]
    ax.semilogx(Pe_analytical, success_rates_real, 'go-', ms=4)
    ax.axvline(1, color='red', ls='--', lw=1, alpha=0.3, label='Pe = 1')
    ax.axvline(10, color='orange', ls=':', lw=1, alpha=0.3, label='Pe = 10')
    ax.set_xlabel('Peclet number')
    ax.set_ylabel('Success rate (error < 15°)')
    ax.set_title('Navigation Success vs Pe')
    ax.set_ylim(-0.05, 1.05)
    ax.legend(fontsize=9)

    fig.suptitle('Peclet Number Governs Navigation', fontsize=14)
    plt.tight_layout()
    if save_prefix:
        fig.savefig(f'{save_prefix}peclet.png', dpi=150)
        print(f'Saved {save_prefix}peclet.png')
    return fig


# ── 2. Model differentiation at the phase boundary ────────────────

def model_differentiation(save_prefix=None):
    """Run all compass models at noise levels near the phase boundary."""
    sigma_range = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0])
    n_cry = 50
    n_bugs = 200
    duration = 200
    dt = 0.02

    models = _ensure_spin_dynamics()
    model_names = ['toy_fad_o2', 'toy_fad_trp',
                   'intermediate_fad_o2', 'intermediate_fad_trp']

    # Get contrasts from quantum models
    RPC = models['_RadicalPairCompass']
    quantum_contrasts = {}
    for name in model_names:
        factory = models[name]
        qc = RPC(model=factory())
        quantum_contrasts[name] = qc.contrast

    results = {}

    # Analytical baseline C=0.15
    label = 'analytical (C=0.15)'
    errs = []
    for sig in sigma_range:
        err, _ = fast_ensemble(n_bugs=n_bugs, duration=duration, dt=dt,
                               kappa=2.0, sigma_theta=sig,
                               contrast=0.15, n_cry=n_cry, sigma_sensor=0.02)
        errs.append(err)
        print(f'  {label}  σ={sig:.2f}  err={err:.1f}°')
    results[label] = np.array(errs)

    # Quantum models — use their computed contrasts
    for name in model_names:
        C = quantum_contrasts[name]
        label = f'{name.replace("_"," ")} (C={C:.3f})'
        errs = []
        for sig in sigma_range:
            err, _ = fast_ensemble(n_bugs=n_bugs, duration=duration, dt=dt,
                                   kappa=2.0, sigma_theta=sig,
                                   contrast=C, n_cry=n_cry, sigma_sensor=0.02)
            errs.append(err)
            print(f'  {label}  σ={sig:.2f}  err={err:.1f}°')
        results[label] = np.array(errs)

    # Also run at biological contrasts (literature values with relaxation)
    for C_lit, label in [(0.01, '[FAD TrpH] lit. (C=0.01)'),
                          (0.15, '[FAD O₂] lit. (C=0.15)')]:
        errs = []
        for sig in sigma_range:
            err, _ = fast_ensemble(n_bugs=n_bugs, duration=duration, dt=dt,
                                   kappa=2.0, sigma_theta=sig,
                                   contrast=C_lit, n_cry=n_cry, sigma_sensor=0.02)
            errs.append(err)
            print(f'  {label}  σ={sig:.2f}  err={err:.1f}°')
        results[label] = np.array(errs)

    # Plot
    fig, ax = plt.subplots(figsize=(11, 7))
    colors = ['grey', '#2196F3', '#4CAF50', '#1565C0', '#2E7D32',
              '#FF9800', '#00BCD4']
    markers = ['s', 'o', '^', 'D', 'v', 'P', 'X']

    for (label, errs), color, marker in zip(results.items(), colors, markers):
        ax.plot(sigma_range, errs, color=color, marker=marker, ms=5,
                lw=2, label=label)

    ax.axhline(10, color='green', ls=':', lw=1, alpha=0.4)
    ax.axhline(30, color='orange', ls=':', lw=1, alpha=0.4)
    ax.axhline(90, color='red', ls=':', lw=1, alpha=0.3)
    ax.set_xlabel(r'Angular noise $\sigma_\theta$ (rad/$\sqrt{s}$)', fontsize=12)
    ax.set_ylabel('Mean heading error (°)', fontsize=12)
    ax.set_title(f'Model Differentiation: Computed vs Literature Contrasts\n'
                 f'($N_{{cry}} = {n_cry}$, $\\kappa = 2.0$)',
                 fontsize=13)
    ax.legend(fontsize=8, loc='upper left')
    ax.set_ylim(0, 95)
    ax.set_xscale('log')

    plt.tight_layout()
    if save_prefix:
        fig.savefig(f'{save_prefix}differentiate.png', dpi=150)
        print(f'Saved {save_prefix}differentiate.png')
    return fig


# ── 3. Spherical harmonic decomposition ───────────────────────────

def harmonic_decomposition(save_prefix=None):
    """Decompose Φ_S(θ) into Legendre polynomial components."""
    from numpy.polynomial.legendre import legval, legfit

    models = _ensure_spin_dynamics()
    RPC = models['_RadicalPairCompass']
    model_names = ['toy_fad_o2', 'toy_fad_trp',
                   'intermediate_fad_o2', 'intermediate_fad_trp']

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    all_coeffs = {}

    for ax, name in zip(axes.flat, model_names):
        factory = models[name]
        model = factory()
        compass = RPC(model=model, n_theta=500)
        thetas, yields = compass.yield_curve()

        x = np.cos(thetas)
        max_L = 8
        coeffs = legfit(x, yields, max_L)
        y_fit = legval(x, coeffs)

        coeffs_02 = np.zeros(max_L + 1)
        coeffs_02[0] = coeffs[0]
        coeffs_02[2] = coeffs[2]
        y_02 = legval(x, coeffs_02)

        total_var = np.var(yields)
        resid_02 = np.var(yields - y_02)
        resid_full = np.var(yields - y_fit)

        ax.plot(np.degrees(thetas), yields, 'b-', lw=2, label='quantum')
        ax.plot(np.degrees(thetas), y_02, 'r--', lw=1.5, label='L=0,2 only')
        ax.plot(np.degrees(thetas), y_fit, 'g:', lw=1.5, label=f'L=0..{max_L}')
        ax.set_xlabel(r'$\theta$ (°)')
        ax.set_ylabel(r'$\Phi_S$')
        ax.set_title(model['name'])
        ax.legend(fontsize=8)

        r2_02 = 100*(1 - resid_02/total_var) if total_var > 0 else 100
        r2_full = 100*(1 - resid_full/total_var) if total_var > 0 else 100
        info = (f'C = {compass.contrast:.3f}\n'
                f'L=0,2 captures {r2_02:.1f}%\n'
                f'L=0..{max_L} captures {r2_full:.1f}%')
        ax.text(0.02, 0.02, info, transform=ax.transAxes, fontsize=9,
                va='bottom', bbox=dict(boxstyle='round', fc='wheat', alpha=0.7))
        all_coeffs[name] = coeffs

    fig.suptitle('Legendre Decomposition of Singlet Yield Anisotropy', fontsize=14)
    plt.tight_layout()

    # Bar chart
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    max_L = 8
    x_pos = np.arange(max_L + 1)
    width = 0.18
    colors = ['#2196F3', '#4CAF50', '#1565C0', '#2E7D32']

    for i, (name, coeffs) in enumerate(all_coeffs.items()):
        rel = np.abs(coeffs) / np.abs(coeffs[0]) if np.abs(coeffs[0]) > 1e-10 else np.abs(coeffs)
        # Replace zeros with tiny value for log plot
        rel = np.maximum(rel, 1e-7)
        ax2.bar(x_pos + i * width, rel, width, label=name.replace('_', ' '),
                color=colors[i], alpha=0.8)

    ax2.set_xticks(x_pos + 1.5 * width)
    ax2.set_xticklabels([f'L={l}' for l in range(max_L + 1)])
    ax2.set_ylabel(r'$|c_L| / c_0$')
    ax2.set_title('Relative Legendre Coefficients')
    ax2.legend(fontsize=9)
    ax2.set_yscale('log')
    ax2.set_ylim(1e-5, 2)

    plt.tight_layout()
    if save_prefix:
        fig.savefig(f'{save_prefix}harmonics_fit.png', dpi=150)
        fig2.savefig(f'{save_prefix}harmonics_bar.png', dpi=150)
        print(f'Saved {save_prefix}harmonics_fit.png and {save_prefix}harmonics_bar.png')
    return fig, fig2


# ── 4. Critical noise per model ───────────────────────────────────

def critical_noise(save_prefix=None):
    """Find σ_θ* where mean heading error crosses 30° for each model."""
    models = _ensure_spin_dynamics()
    RPC = models['_RadicalPairCompass']
    model_names = ['toy_fad_o2', 'toy_fad_trp',
                   'intermediate_fad_o2', 'intermediate_fad_trp']

    n_bugs = 200
    duration = 200
    dt = 0.02
    n_cry = 50
    threshold = 30.0

    def run_error(contrast, sig):
        err, _ = fast_ensemble(n_bugs=n_bugs, duration=duration, dt=dt,
                               kappa=2.0, sigma_theta=sig,
                               contrast=contrast, n_cry=n_cry,
                               sigma_sensor=0.02, seed=42)
        return err

    def find_critical(contrast, label):
        lo, hi = 0.1, 5.0
        err_lo = run_error(contrast, lo)
        err_hi = run_error(contrast, hi)
        print(f'  {label}: err({lo})={err_lo:.1f}°, err({hi})={err_hi:.1f}°')
        if err_lo > threshold:
            return lo
        if err_hi < threshold:
            return hi
        for _ in range(10):
            mid = np.sqrt(lo * hi)
            err_mid = run_error(contrast, mid)
            print(f'    bisect σ={mid:.3f}  err={err_mid:.1f}°')
            if err_mid < threshold:
                lo = mid
            else:
                hi = mid
        return np.sqrt(lo * hi)

    results = {}

    # Literature contrasts
    for C, label in [(0.01, '[FAD TrpH] lit. (C=0.01)'),
                      (0.15, '[FAD O₂] lit. (C=0.15)')]:
        sig_star = find_critical(C, label)
        results[label] = sig_star
        print(f'  → σ* = {sig_star:.3f}')

    # Computed quantum contrasts
    for name in model_names:
        factory = models[name]
        qc = RPC(model=factory())
        label = f'{name.replace("_"," ")} (C={qc.contrast:.3f})'
        sig_star = find_critical(qc.contrast, label)
        results[label] = sig_star
        print(f'  → σ* = {sig_star:.3f}')

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = list(results.keys())
    vals = [results[k] for k in labels]
    colors = ['#FF9800', '#00BCD4', '#2196F3', '#4CAF50', '#1565C0', '#2E7D32']

    bars = ax.barh(range(len(labels)), vals, color=colors[:len(labels)])
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel(r'Critical noise $\sigma_\theta^*$ (rad/$\sqrt{s}$) at 30° threshold',
                  fontsize=11)
    ax.set_title(f'Noise Tolerance by Compass Model ($N_{{cry}} = {n_cry}$)')

    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', ha='left', va='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    if save_prefix:
        fig.savefig(f'{save_prefix}critical_noise.png', dpi=150)
        print(f'Saved {save_prefix}critical_noise.png')
    return fig


# ── 5. N_cry sweep: sensor population trade-off ───────────────────

def ncry_sweep(save_prefix=None):
    """Sweep N_cry for C=0.01 and C=0.15 at several noise levels.

    Answers: how many cryptochrome molecules does the weak compass
    need to match the strong one?

    Also computes the analytical compass noise σ_compass(N_cry, C)
    and the effective total noise σ_eff = √(σ_θ² + κ² σ_compass²)
    to verify the threshold prediction.
    """
    n_cry_range = np.array([5, 10, 20, 50, 100, 200, 500, 1000,
                            2000, 5000, 10000])
    sigma_thetas = [0.3, 0.5, 1.0]
    contrasts = {'[FAD O₂] C=0.15': 0.15,
                 '[FAD TrpH] C=0.01': 0.01}
    n_bugs = 200
    duration = 200
    dt = 0.02
    sigma_sensor = 0.02

    results = {}  # {(label, sigma): array of errors}

    for sig in sigma_thetas:
        for label, C in contrasts.items():
            key = (label, sig)
            errs = []
            for n_cry in n_cry_range:
                err, _ = fast_ensemble(
                    n_bugs=n_bugs, duration=duration, dt=dt,
                    kappa=2.0, sigma_theta=sig,
                    contrast=C, n_cry=n_cry, sigma_sensor=sigma_sensor)
                errs.append(err)
                print(f'  {label}  σ={sig}  N_cry={n_cry:5d}  err={err:.1f}°')
            results[key] = np.array(errs)

    # ── Analytical prediction ──
    # σ_compass(N, C) = σ_sensor / (C * mean * √(2N/8))
    # The heading error from compass alone is approximately σ_compass
    # The total effective error rate combines motor + compass:
    #   σ_eff² ≈ σ_θ² + (κ * σ_compass)² * dt  [not quite right dimensionally]
    # More carefully: compass adds ~σ_compass rad error per reading,
    # steering gain κ converts this to κ*σ_compass rad/s torque noise,
    # which acts like additional σ_θ.
    # Effective: σ_eff = √(σ_θ² + (κ * σ_compass)²) approximately.
    # But the σ_compass is per-step, not per-√s... let's just show the
    # compass noise vs motor noise comparison.

    mean_yield = 0.5
    n_ch = 8

    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5), sharey=True)

    for ax, sig in zip(axes, sigma_thetas):
        for (label, C), color, ls in zip(
                contrasts.items(),
                ['#00BCD4', '#FF9800'],
                ['-', '--']):
            key = (label, sig)
            ax.semilogx(n_cry_range, results[key], color=color,
                        marker='o', ms=5, lw=2, ls=ls, label=label)

        ax.set_xlabel(r'$N_{cry}$ (cryptochrome molecules)', fontsize=11)
        ax.set_title(f'$\\sigma_\\theta = {sig}$ rad/$\\sqrt{{s}}$', fontsize=12)
        ax.axhline(10, color='green', ls=':', lw=1, alpha=0.4)
        ax.axhline(30, color='orange', ls=':', lw=1, alpha=0.4)
        ax.legend(fontsize=9)

        # Mark the N_cry where C=0.01 first matches C=0.15's asymptote
        err_high = results[('[FAD O₂] C=0.15', sig)]
        err_low = results[('[FAD TrpH] C=0.01', sig)]
        asymptote = err_high[-1]  # C=0.15 at N=10000 (saturated)
        # Find crossover
        for i, (el, nc) in enumerate(zip(err_low, n_cry_range)):
            if el <= asymptote * 1.1:  # within 10% of asymptote
                ax.axvline(nc, color='red', ls=':', lw=1, alpha=0.5)
                ax.text(nc * 1.1, asymptote + 2,
                        f'N*≈{nc}', fontsize=9, color='red')
                break

    axes[0].set_ylabel('Mean heading error (°)', fontsize=11)
    axes[0].set_ylim(0, 70)

    fig.suptitle('Sensor Population Compensates for Low Contrast', fontsize=14)
    plt.tight_layout()

    # ── Second figure: compass noise vs motor noise ──
    fig2, ax2 = plt.subplots(figsize=(9, 6))

    n_cry_fine = np.logspace(0.5, 4.5, 100)
    for label, C in contrasts.items():
        delta = C * mean_yield
        sigma_c = sigma_sensor / (delta * np.sqrt(2 * n_cry_fine / n_ch))
        ax2.loglog(n_cry_fine, np.degrees(sigma_c), lw=2, label=label)

    for sig in sigma_thetas:
        ax2.axhline(np.degrees(sig), ls='--', lw=1, alpha=0.6,
                     label=f'$\\sigma_\\theta = {sig}$')

    ax2.set_xlabel(r'$N_{cry}$', fontsize=12)
    ax2.set_ylabel(r'Compass heading noise $\sigma_{compass}$ (°)', fontsize=12)
    ax2.set_title('Compass Noise vs Motor Noise', fontsize=13)
    ax2.legend(fontsize=9)
    ax2.set_ylim(0.1, 500)
    ax2.set_xlim(3, 30000)

    # Shade the "compass-limited" region
    ax2.fill_between(n_cry_fine,
                     np.degrees(sigma_thetas[0]) * np.ones_like(n_cry_fine),
                     500, alpha=0.05, color='red')
    ax2.text(5, 200, 'compass-limited\n(σ_compass > σ_θ)',
             fontsize=10, color='red', alpha=0.6)
    ax2.text(5000, 0.3, 'motor-limited\n(σ_compass < σ_θ)',
             fontsize=10, color='green', alpha=0.6)

    plt.tight_layout()

    if save_prefix:
        fig.savefig(f'{save_prefix}ncry_sweep.png', dpi=150)
        fig2.savefig(f'{save_prefix}ncry_noise.png', dpi=150)
        print(f'Saved {save_prefix}ncry_sweep.png and {save_prefix}ncry_noise.png')
    return fig, fig2


# ── 6. Full simulation validation at C=0.01 ──────────────────────

def validate_fast_vs_full(save_prefix=None):
    """Compare the fast Gaussian approximation against the full
    ring-attractor simulation at C=0.01 (marginal compass).

    The ring attractor's nonlinear winner-take-all dynamics may filter
    compass noise better than the Gaussian model predicts.
    """
    from agent import Bug

    sigma_range = np.array([0.1, 0.3, 0.5, 0.8, 1.0])
    n_cry = 50
    n_runs = 30
    duration = 200
    dt = 0.02
    landscape = Landscape()

    contrasts_to_test = [0.01, 0.15]
    results = {}

    for C in contrasts_to_test:
        # Fast simulation
        fast_errs = []
        for sig in sigma_range:
            err, _ = fast_ensemble(
                n_bugs=200, duration=duration, dt=dt,
                kappa=2.0, sigma_theta=sig,
                contrast=C, n_cry=n_cry, sigma_sensor=0.02)
            fast_errs.append(err)
        results[(C, 'fast')] = np.array(fast_errs)

        # Full ring attractor simulation
        full_errs = []
        for sig in sigma_range:
            run_errors = []
            for seed in range(n_runs):
                bug = Bug(
                    x0=500, y0=100, goal_heading=3*np.pi/4, speed=1.0,
                    kappa=2.0, sigma_theta=sig, sigma_xy=0.05,
                    compass_params={'contrast': C, 'n_cry': n_cry,
                                    'sigma_sensor': 0.02},
                    seed=seed
                )
                bug.run(landscape, duration=duration, dt=dt)
                run_errors.append(bug.mean_heading_error())
            err = np.degrees(np.mean(run_errors))
            full_errs.append(err)
            print(f'  C={C}  σ={sig}  full={err:.1f}°  fast={results[(C,"fast")][len(full_errs)-1]:.1f}°')
        results[(C, 'full')] = np.array(full_errs)

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), sharey=True)

    for ax, C in zip(axes, contrasts_to_test):
        fast = results[(C, 'fast')]
        full = results[(C, 'full')]
        ax.plot(sigma_range, fast, 'b--o', ms=6, lw=2, label='fast (Gaussian)')
        ax.plot(sigma_range, full, 'r-s', ms=6, lw=2, label='full (ring attractor)')

        # Relative difference
        diff = full - fast
        for i, (s, d) in enumerate(zip(sigma_range, diff)):
            if abs(d) > 0.5:
                ax.annotate(f'{d:+.1f}°', (s, full[i]),
                            textcoords='offset points', xytext=(8, 5),
                            fontsize=8, color='purple')

        ax.set_xlabel(r'$\sigma_\theta$ (rad/$\sqrt{s}$)', fontsize=11)
        ax.set_title(f'C = {C} ($N_{{cry}}$ = {n_cry})', fontsize=12)
        ax.legend(fontsize=10)
        ax.axhline(30, color='orange', ls=':', lw=1, alpha=0.4)
        ax.set_ylim(0, 70)

    axes[0].set_ylabel('Mean heading error (°)', fontsize=11)

    fig.suptitle('Fast Simulation vs Full Ring Attractor', fontsize=14)
    plt.tight_layout()

    if save_prefix:
        fig.savefig(f'{save_prefix}validate_fast.png', dpi=150)
        print(f'Saved {save_prefix}validate_fast.png')
    return fig


# ── 7. Relaxation + navigation: does the threshold survive? ──────

def relaxation_navigation(save_prefix=None):
    """Navigation performance with relaxation-suppressed contrasts.

    Uses pre-computed contrast values from the spin relaxation analysis
    to check whether the C ~ 0.1 navigation threshold survives with
    realistic decoherence.
    """
    # Pre-computed contrasts from the relaxation analysis.
    # Format: (label, C_no_relax, C_T2_3us, C_T2_1us, C_asym)
    # "asym" = FAD T2=3µs, partner T2=1µs
    relaxed_data = {
        'toy FAD-O₂':   {'none': 0.391, 'T2=10µs': None, 'T2=3µs': 0.275, 'T2=1µs': 0.165, 'asym': 0.193},
        'toy FAD-TrpH':  {'none': 0.210, 'T2=10µs': None, 'T2=3µs': 0.155, 'T2=1µs': 0.095, 'asym': 0.120},
        'inter FAD-O₂': {'none': 0.448, 'T2=10µs': None, 'T2=3µs': 0.304, 'T2=1µs': 0.176, 'asym': 0.217},
        'inter FAD-TrpH': {'none': 0.245, 'T2=10µs': 0.211, 'T2=3µs': 0.158, 'T2=1µs': 0.084, 'asym': 0.115},
    }

    # Relaxation scenarios to compare
    scenarios = ['none', 'T2=3µs', 'T2=1µs']

    sigma_range = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0])
    n_cry = 50
    n_bugs = 200
    duration = 200
    dt = 0.02

    # ── Figure 1: Navigation curves per relaxation scenario ──
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

    model_colors = {
        'toy FAD-O₂': '#2196F3',
        'toy FAD-TrpH': '#4CAF50',
        'inter FAD-O₂': '#1565C0',
        'inter FAD-TrpH': '#2E7D32',
    }

    for ax, scenario in zip(axes, scenarios):
        # Literature baselines
        for C_lit, label, color, ls in [
            (0.15, '[FAD O₂] lit.', '#00BCD4', '--'),
            (0.01, '[FAD TrpH] lit.', '#FF9800', '--'),
        ]:
            errs = []
            for sig in sigma_range:
                err, _ = fast_ensemble(n_bugs=n_bugs, duration=duration, dt=dt,
                                       kappa=2.0, sigma_theta=sig,
                                       contrast=C_lit, n_cry=n_cry, sigma_sensor=0.02)
                errs.append(err)
            ax.plot(sigma_range, errs, color=color, ls=ls, marker='x', ms=5,
                    lw=1.5, label=label)

        # Quantum models with relaxation
        for model_name, contrasts in relaxed_data.items():
            C = contrasts.get(scenario)
            if C is None:
                continue
            errs = []
            for sig in sigma_range:
                err, _ = fast_ensemble(n_bugs=n_bugs, duration=duration, dt=dt,
                                       kappa=2.0, sigma_theta=sig,
                                       contrast=C, n_cry=n_cry, sigma_sensor=0.02)
                errs.append(err)
            label = f'{model_name} (C={C:.3f})'
            ax.plot(sigma_range, errs, color=model_colors[model_name],
                    marker='o', ms=4, lw=2, label=label)

        ax.axhline(10, color='green', ls=':', lw=1, alpha=0.4)
        ax.axhline(30, color='orange', ls=':', lw=1, alpha=0.4)
        ax.axhline(90, color='red', ls=':', lw=1, alpha=0.3)
        ax.set_xlabel(r'$\sigma_\theta$ (rad/$\sqrt{s}$)', fontsize=11)
        title = 'No relaxation' if scenario == 'none' else scenario + ' both'
        ax.set_title(title, fontsize=12)
        ax.set_xscale('log')
        ax.legend(fontsize=7, loc='upper left')

    axes[0].set_ylabel('Mean heading error (°)', fontsize=11)
    axes[0].set_ylim(0, 95)

    fig.suptitle(f'Relaxation + Navigation ($N_{{cry}} = {n_cry}$): '
                 'Does the Threshold Survive?', fontsize=14)
    plt.tight_layout()

    # ── Figure 2: Contrast bar chart across scenarios ──
    fig2, ax2 = plt.subplots(figsize=(11, 6))
    threshold_C = 0.10
    x_pos = np.arange(len(relaxed_data))
    width = 0.2
    scen_colors = {'none': '#4CAF50', 'T2=3µs': '#FF9800', 'T2=1µs': '#F44336', 'asym': '#9C27B0'}

    for i, scenario in enumerate(scenarios + ['asym']):
        vals = []
        for model_name in relaxed_data:
            c = relaxed_data[model_name].get(scenario)
            vals.append(c if c is not None else 0)
        bars = ax2.bar(x_pos + i * width, vals, width,
                       label=scenario if scenario != 'none' else 'no relaxation',
                       color=scen_colors.get(scenario, 'grey'), alpha=0.8)

    ax2.axhline(threshold_C, color='red', ls='--', lw=2, alpha=0.7,
                label=f'navigation threshold C ≈ {threshold_C}')
    ax2.set_xticks(x_pos + 1.5 * width)
    ax2.set_xticklabels(list(relaxed_data.keys()), fontsize=10)
    ax2.set_ylabel('Contrast C', fontsize=12)
    ax2.set_title('Contrast Suppression by Spin Relaxation', fontsize=13)
    ax2.legend(fontsize=9)
    ax2.set_ylim(0, 0.5)

    plt.tight_layout()

    if save_prefix:
        fig.savefig(f'{save_prefix}relax_navigation.png', dpi=150)
        fig2.savefig(f'{save_prefix}relax_contrasts.png', dpi=150)
        print(f'Saved {save_prefix}relax_navigation.png and {save_prefix}relax_contrasts.png')
    return fig, fig2


# ── Main ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Deeper analysis of magnetic bug')
    parser.add_argument('--peclet', action='store_true')
    parser.add_argument('--differentiate', action='store_true')
    parser.add_argument('--harmonics', action='store_true')
    parser.add_argument('--critical-noise', action='store_true')
    parser.add_argument('--ncry', action='store_true')
    parser.add_argument('--validate-fast', action='store_true')
    parser.add_argument('--relax-nav', action='store_true')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--save', type=str, default='fig_',
                        help='Save prefix (default: fig_)')
    args = parser.parse_args()

    run_all = args.all or not any([args.peclet, args.differentiate,
                                    args.harmonics, args.critical_noise,
                                    args.ncry, args.validate_fast,
                                    args.relax_nav])

    if args.peclet or run_all:
        print('=== Peclet number study ===')
        peclet_study(save_prefix=args.save)

    if args.harmonics or run_all:
        print('\n=== Harmonic decomposition ===')
        harmonic_decomposition(save_prefix=args.save)

    if args.differentiate or run_all:
        print('\n=== Model differentiation at boundary ===')
        model_differentiation(save_prefix=args.save)

    if args.critical_noise or run_all:
        print('\n=== Critical noise per model ===')
        critical_noise(save_prefix=args.save)

    if args.ncry or run_all:
        print('\n=== N_cry sweep ===')
        ncry_sweep(save_prefix=args.save)

    if args.validate_fast or run_all:
        print('\n=== Validate fast vs full simulation ===')
        validate_fast_vs_full(save_prefix=args.save)

    if args.relax_nav or run_all:
        print('\n=== Relaxation + navigation ===')
        relaxation_navigation(save_prefix=args.save)

    print('\nDone.')


if __name__ == '__main__':
    main()
