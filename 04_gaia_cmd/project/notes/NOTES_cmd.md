# NOTES — Gaia CMD demo

## Decisions

- **Average parallax, not 1/parallax.** For a common-distance cluster the unbiased
  estimator is the (inverse-variance-weighted) mean parallax, inverted once. Averaging
  per-star distances d = 1/ϖ is biased upward when ϖ is noisy. The notebook shows both
  so the bias is visible, not hidden.
- **Cache the query.** A live Gaia query is flaky in a classroom (network, archive
  load, timeouts). We run it once and ship the CSV; the ADQL below makes it reproducible.
- **Membership by parallax + proper motion.** The Pleiades move together on the sky;
  cutting on proper motion and parallax removes most field stars and gives a clean CMD.

## The exact Gaia query (reproducible)

```sql
SELECT ra, dec, parallax, parallax_error, phot_g_mean_mag, bp_rp, pmra, pmdec
FROM gaiadr3.gaia_source
WHERE 1=CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 56.75, 24.12, 2.0))
  AND parallax BETWEEN 6.0 AND 9.0
  AND parallax_over_error > 10
  AND phot_g_mean_mag IS NOT NULL AND bp_rp IS NOT NULL
  AND pmra BETWEEN 15 AND 25 AND pmdec BETWEEN -55 AND -40
```
Run via `astroquery.gaia.Gaia.launch_job_async(adql).get_results()`.

## Numbers

- Synthetic cluster injected at 135.0 pc → recovered within 1%.
- Real Pleiades: 1033 members, median parallax 7.368 mas, robust distance 135.9 pc
  (literature 136.2 pc). Naive mean-of-1/ϖ runs slightly high (the bias).
