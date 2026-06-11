# NOTES — photometry demo

## Decisions

- **"Center" aperture, not fractional.** Counting whole pixels whose center is inside
  the circle maps *exactly* onto `photutils method='center'`, giving an unambiguous
  cross-check. Fractional-pixel ("exact") apertures are more accurate but the geometry
  would obscure the core idea.
- **Median sky annulus.** M67 is crowded; a mean sky would be biased high by stray
  neighbor flux in the ring. The median is robust to a few contaminating pixels.
- **Relative photometry is the testable quantity.** A fixed aperture loses the same
  fraction of every (same-PSF) star's light, so magnitude *differences* are recovered
  exactly even though absolute aperture flux is not. The synthetic test asserts on
  differences, not absolute flux.

## Dead end / gotcha (the wrong turn)

First aperture mask used `(dx² + dy²) <= r²`. Against `photutils method='center'` the
raw sums disagreed by ~1.3% — too much for "same method." Plotting the differing
pixels showed they all sit at distance *exactly* r: our `<=` included a ring of edge
pixels that photutils' strict `<` excludes. Changing to `< r²` gave bit-exact
agreement (max fractional difference 0). The photutils cross-check is what exposed a
convention bug a standalone pipeline would have hidden.

## Numbers

- Synthetic: relative magnitudes recovered to < 0.02 mag.
- Real M67: 15 brightest stars measured; our aperture sums match photutils to 0
  (machine precision). Brightest instrumental mags ≈ 11 (arbitrary ZP=25).
