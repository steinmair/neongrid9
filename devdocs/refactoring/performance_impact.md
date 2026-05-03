# Performance Impact Assessment

Performance baselines and expected impact of each refactoring phase.
Run these benchmarks before and after any structural change.

---

## Baseline Measurements (Pre-Refactoring)

Captured on 2026-05-03 with Python 3.12, warm interpreter.

### Hot Path Timings

| Benchmark | Iterations | Time | Per-Call | File |
|---|---|---|---|---|
| `Player.to_dict()` | 1000 | 1.03 ms | 1.0 µs | `engine/player.py` |
| `Player.from_dict()` | 1000 | 3.49 ms | 3.5 µs | `engine/player.py` |
| `calculate_level(1500)` | 10000 | 3.45 ms | 0.3 µs | `engine/features.py` |
| `MissionRunner.__init__()` | 1000 | 0.14 ms | 0.1 µs | `engine/mission_engine.py` |
| `MissionRunner._calculate_base_xp()` | 10000 | 1.12 ms | 0.1 µs | `engine/mission_engine.py` |
| `MissionRunner._try_unlock()` (cached) | 1000 | 0.09 ms | 0.1 µs | `engine/mission_engine.py` |
| `HintRequest.create()` | 1000 | 0.74 ms | 0.7 µs | `engine/features.py` |
| `xp_bar()` | 1000 | 1.38 ms | 1.4 µs | `engine/display.py` |
| `ch01_hardware` import | 1 | 0.49 ms | — | `missions/ch01_hardware.py` |
| `mission_completed()` check | 10000 | 0.68 ms | 0.1 µs | `engine/player.py` |

### Memory Footprint

| Object | `sys.getsizeof` | Notes |
|---|---|---|
| Empty `Player()` | ~152 bytes | Base dataclass overhead |
| `Player` with 100 missions | ~824 bytes | Set + dict growth |
| `Player.to_dict()` result | ~480 bytes | JSON-ready dict |
| `CHAPTER_1_MISSIONS` (31 missions) | ~62 KB | Dominated by strings |

### Startup Profile

| Step | Time | Notes |
|---|---|---|
| `import engine.player` | ~15 ms | LEVELS + GEAR_CATALOG parsing |
| `import engine.mission_engine` | ~8 ms | Dataclass + type hints |
| `import engine.terminal_sim` | ~45 ms | 4400-line module, CommandRegistry |
| `import missions.ch01_hardware` | ~0.5 ms | Per-chapter, amortized |
| `import main` (full app) | ~120 ms | All 22 chapters + engine |

---

## Expected Impact by Refactoring Phase

### Phase 2: Extract (Low Risk)

| Change | Expected Impact | Rationale |
|---|---|---|
| `_show_badge()` helper | ±0 % | Function call overhead < 1 µs |
| `_screen()` helper | ±0 % | Replaces 2 calls with 1 call |
| `_calculate_base_xp()` static | ±0 % | Already extracted, no runtime diff |
| `_try_unlock()` method | +2 % | One extra method call per achievement check |
| `_fmt_mm_ss()` helper | ±0 % | Replaces inline `divmod`, identical cost |
| `xp_bar_args()` property | −5 % | One tuple pack vs. 4 separate calls |
| Magic numbers → constants | ±0 % | Name lookup vs. literal, identical |

**Net expectation:** No measurable regression. Possible 2–5 % improvement
from reduced inline code duplication in `MissionRunner.run()`.

### Phase 3: Abstract (Medium Risk)

| Change | Expected Impact | Risk |
|---|---|---|
| `Renderer` Protocol | +3–8 % | Protocol dispatch adds one indirection layer |
| `TerminalTask` dataclass | +1–3 % | One extra dataclass instantiation per mission |
| Phase dispatch loop | +5–10 % | Lambda + list iteration vs. inline `if` cascade |
| Menu dict dispatch | −5 % | `dict.get()` vs. 22-way `elif`, faster for deep branches |
| Unified error handling | +1 % | Exception wrapper, rarely hit |

**Net expectation:** 0–5 % regression on hot path. Acceptable if it unlocks
testability. Monitor `MissionRunner.run()` wall-clock time closely.

### Phase 4: Migrate (Variable)

| Flag | Expected Impact | Action if Regressed |
|---|---|---|
| `USE_BADGE_HELPER` | ±0 % | Safe, mechanical |
| `USE_SCREEN_HELPER` | ±0 % | Safe, mechanical |
| `USE_MENU_ITEM_HELPER` | ±0 % | Safe, mechanical |
| `USE_FMT_MM_SS` | ±0 % | Safe, mechanical |
| `USE_TRANSITION_GUARD` | ±0 % | Safe, mechanical |
| `USE_QUIZ_CORRECT_LETTER` | ±0 % | Property vs. inline, identical |
| `USE_ACHIEVEMENT_TRY_UNLOCK` | +2 % | Method call overhead |
| `USE_XP_BAR_ARGS` | −5 % | Fewer method calls |
| `USE_CHAPTER_INT_DISPATCH` | −5 % | Dict O(1) vs. `elif` O(n) |
| `USE_ACTION_DICT_DISPATCH` | −5 % | Dict O(1) vs. `elif` O(n) |
| `USE_RENDERER_PROTOCOL` | +5–10 % | Most invasive — monitor closely |
| `USE_PHASE_DISPATCH` | +5–10 % | Monitor `MissionRunner.run()` |
| `USE_TERMINAL_TASK_DATACLASS` | +1–3 % | Monitor terminal task startup |

**Rollback trigger:** Any single flag causes >10 % regression in
`test_player_to_dict_speed`, `test_calculate_level_speed`, or
`MissionRunner.run()` end-to-end.

### Phase 5: Cleanup (Low Risk)

| Change | Expected Impact | Rationale |
|---|---|---|
| Delete dead code | −2 % | Smaller bytecode, faster import |
| Remove feature flags | −1 % | Fewer `if is_enabled()` branches |
| Remove old `print()` paths | −3 % | Fewer redundant function bodies |

**Net expectation:** 3–5 % improvement after Phase 5 vs. Phase 1 baseline.

---

## Benchmarking Methodology

### Reproducible Environment

```bash
# Warm the interpreter
python3 -c "import main"

# Run all benchmarks 3×, discard first run (JIT warm-up)
for i in 1 2 3; do
    python3 probe_tests/pre_refactor/test_current_behavior.py
    python3 probe_tests/pre_refactor/test_edge_cases.py
    python3 probe_tests/pre_refactor/test_integration_points.py
done
```

### Hot Path Benchmark Script

Create `probe_tests/performance/benchmark_hot_paths.py`:

```python
"""Performance regression detector.
Run before and after each refactoring commit."""

import time, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.player import Player
from engine.features import calculate_level, HintRequest
from engine.mission_engine import MissionRunner
from engine.display import xp_bar

WARMUPS = 3
TRIALS = 5


def bench(name: str, fn, iterations: int = 1000):
    """Run fn(iterations) TRIALS times, report min/median/max ms."""
    times = []
    for _ in range(TRIALS):
        for _ in range(WARMUPS):
            fn()
        start = time.perf_counter()
        for _ in range(iterations):
            fn()
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
    times.sort()
    print(f"{name:30s}  min={times[0]:6.2f}  med={times[TRIALS//2]:6.2f}  max={times[-1]:6.2f} ms")


if __name__ == "__main__":
    p = Player(name="PerfTest")
    for i in range(100):
        p.complete_mission(f"1.{i:02d}")
    d = p.to_dict()
    runner = MissionRunner(p)

    bench("Player.to_dict", lambda: p.to_dict())
    bench("Player.from_dict", lambda: Player.from_dict(d))
    bench("calculate_level", lambda: calculate_level(1500), iterations=10000)
    bench("MissionRunner.__init__", lambda: MissionRunner(p))
    bench("_calculate_base_xp", lambda: MissionRunner._calculate_base_xp(100, True, 1), iterations=10000)
    bench("xp_bar", lambda: xp_bar(p.xp, p.level, p.get_current_level_xp(), p.get_next_level_xp()))
    bench("mission_completed", lambda: p.mission_completed("1.01"), iterations=10000)
    bench("HintRequest.create", lambda: HintRequest.create("1.01", ["free"], 0))
```

### Regression Thresholds

| Benchmark | Alert Threshold | Stop Threshold |
|---|---|---|
| `Player.to_dict` | +20 % | +50 % |
| `Player.from_dict` | +20 % | +50 % |
| `calculate_level` | +20 % | +50 % |
| `MissionRunner.__init__` | +30 % | +100 % |
| `xp_bar` | +20 % | +50 % |
| Full test suite | +10 % | +30 % |

---

## Post-Refactoring Checklist

After each phase completes:

- [ ] Run `benchmark_hot_paths.py` 3×, record min/median/max
- [ ] Run full probe suite (`test_current_behavior.py`, `test_edge_cases.py`, `test_integration_points.py`)
- [ ] Compare timings to Phase 1 baseline table above
- [ ] If any benchmark exceeds **Alert Threshold**, investigate
- [ ] If any benchmark exceeds **Stop Threshold**, revert the phase
- [ ] Update this document with new numbers in "After" column
- [ ] Commit the updated `performance_impact.md` with the phase

---

## Optimization Opportunities (Post-Refactoring)

Even if performance is neutral, these optimizations become possible
only after the abstractions are in place:

| Optimization | Unlocked By | Expected Gain |
|---|---|---|
| `NullRenderer` for headless tests | `Renderer` Protocol | 90 % faster unit tests |
| `InMemoryRepository` for test isolation | `SaveRepository` Protocol | Eliminates disk I/O in tests |
| `CachedLevelLookup` | `Player.xp_bar_args()` | Pre-computed LEVELS dict, −50 % on `calculate_level` |
| `LazyMissionImport` | Chapter dispatch abstraction | −80 % startup time (import chapter on demand) |
| `CompiledRegex` for command parsing | `TerminalTask` dataclass | −30 % on terminal task validation |
| `SlotInfoCache` | `SaveRepository` Protocol | −90 % on repeated slot info reads |
