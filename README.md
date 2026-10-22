<p align="center">
  <b>Planck's Constant — Virtual Lab Simulation</b><br>
  <i>A browser-based circuit lab for determining Planck's constant from the LED's I–V characteristic.</i>
</p>

<p align="center">
  <a href="https://plancks-constant-iitk.vercel.app"><img src="https://img.shields.io/badge/deploy-Vercel-black" alt="Deployed on Vercel"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://github.com/AryanRajMaurya/plancks-constant-iitk"><img src="https://img.shields.io/badge/build-passing-success" alt="CI"></a>
</p>

---

## What it is

A physics virtual lab: the student builds the experimental circuit on a
canvas, wires the components together, takes a set of readings and gets
Planck's constant out of the slope of the LED's current–voltage graph.

Everything happens in the browser. There is no build step, no framework and
no server: `index.html` and a handful of scripts.

## The experiment

The measurement uses the standard method. A cell, a potentiometer and an
ammeter set the current through an LED; a voltmeter reads the voltage across
it. For a diode, the current follows

```
I = I₀ · (exp(qV / (nkT)) − 1)
```

and with `h = q / (nk)` the graph of `ln(I / I₀)` against `V` is a straight
line whose gradient gives Planck's constant. The simulation fits that line
for you and reports the slope.

The student places components, connects them, takes readings into the
observations table, and the graph is drawn from those readings.

## What you can build

| Component | What it does in the simulation |
| --- | --- |
| Cell | The supply. Multi-cell symbol with `+ve` and `-ve` terminals |
| Potentiometer | Sets the current through the circuit |
| LED | The device under test, with a knee voltage and a glow that responds to the current |
| Galvanometer | Reads the current |
| Point | A terminal for making connections |
| Connection | A wire between two points, drawn with a tilt |
| Tap key | The thermistor and the two-way key |

There is undo, redo and reset, a step-by-step procedure panel that walks
through the experiment, and an observations table that feeds the graph.

## Running it locally

The page loads its scripts with `defer` and reads the DOM as it parses, so
it has to be served over HTTP. Opening `index.html` from the filesystem
will not work.

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

Any static server works. There is nothing to install and nothing to build.

## Checking it

```bash
python3 tools/check-page.py
```

The check walks every local reference in `index.html` and confirms the file
exists, and parses every script. Both of those failure modes are invisible
until a student opens the page and something is missing, so they are
checked on every push.

## Layout

```
index.html              the page, and all of its markup and styling
js/javascript.js        the simulation: components, wiring, the observations table
js/graph*.ob.js         the dataset plot and its linear fit
js/*.min.js             jQuery, Popper and Bootstrap, vendored
css/                    Bootstrap and the page styles
image/                  the graph paper background and the formula
tools/check-page.py     the reference and syntax check
```

## License

MIT — see [LICENSE](LICENSE).

Built by [Aryan Raj Maurya](https://github.com/AryanRajMaurya) for the IIT
Kanpur Virtual Labs programme.
