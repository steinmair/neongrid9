# Trace 5: Display Rendering Interface

## Interface Surface

`engine/display.py` exports 20+ functions that render to stdout:

**Screen management:** `clear()`, `header()`, `chapter_header()`, `mission_header()`, `boss_intro()`, `level_up_screen()`
**Text output:** `typewrite()`, `slow_print()`, `show_story()`, `show_code()`, `show_info()`, `show_warn()`, `show_error()`, `show_success()`, `show_exam_tip()`, `show_memory_tip()`, `show_hint()`, `show_achievements()`, `show_transition()`, `show_ascii_art()`, `show_xp_gain()`
**Layout:** `box()`, `xp_bar()`, `show_progress()`
**Input:** `prompt_continue()`, `prompt_input()`

**Called by:** `engine.mission_engine`, `engine.terminal_sim`, `main.py`
**Depends on:** `os`, `sys`, `time` (stdlib only)

---

## Entry Point

Every major action in the game triggers display functions:

- `main.py:show_boot_sequence()` — print() + time.sleep()
- `mission_engine:MissionRunner.run()` — ~15 different display calls
- `terminal_sim:run_terminal()` — prompt_input(), show_error(), show_success()
- `main.py:game_hub()` — clear(), xp_bar(), print()

---

## Execution Path

### Screen Clearing

```
clear()
    |
    +-- os.system('cls' if os.name == 'nt' else 'clear')
```

**Note:** Uses os.system() with hardcoded strings. See vulnerability assessment.

### Animated Text

```
typewrite(text, delay=0.018, color=C.WHITE)
    |
    +-- For each character in text:
         +-- sys.stdout.write(color + ch + C.RESET)
         +-- sys.stdout.flush()
         +-- time.sleep(delay)
    +-- print()  # newline at end
```

### Story Display

```
show_story(speaker, text)
    |
    +-- Print magenta speaker box: "+--[ SPEAKER ]"
    +-- For each line in text.split('\n'):
         +-- print(magenta + "|  " + line + reset)
              +-- time.sleep(delay * len(line))  # LINEAR delay per character count
    +-- Print "+--"
```

**Finding:** The delay in show_story() is `delay * len(line)`. For a 100-character line at 0.015 delay, that's 1.5 seconds per line. A story with 10 lines takes ~15 seconds of forced waiting.

### Code Block

```
show_code(code, lang="bash")
    |
    +-- Print "+--[bash]"
    +-- For each line: print(green + "|  " + line + reset)
    +-- Print "+--"
```

### User Input

```
prompt_input(label="terminal", valid_choices=None)
    |
    +-- Loop:
         +-- response = input(C.PROMPT + f"  [{label}]> " + C.RESET).strip()
         +-- If valid_choices is not None:
              +-- if response.lower() in valid_choices: return response.lower()
              +-- else: print warning and continue
         +-- If no validation: return response as-is
```

### XP Bar

```
xp_bar(current, level, level_xp, next_xp, width=40)
    |
    +-- pct = (current - level_xp) / (next_xp - level_xp)
    +-- filled = int(width * pct)
    +-- bar = "#" * filled + "-" * (width - filled)
    +-- print(f"  LVL {level:02d}  [{bar}]  {current} XP")
```

---

## Resource Management

- **Stdout/Stdin:** Global file descriptors. Never explicitly closed.
- **ANSI codes:** Static strings in class C. Pre-computed at import.
- **Time:** time.sleep() blocks the process. No background threads.
- **Screen state:** No internal buffer. Each function writes directly to stdout.

---

## Error Path

Display functions do not raise exceptions:

- os.system('clear'): Could fail in restricted environments (SSH without TTY, Docker without terminal). Failure is silently ignored.
- input(): Raises EOFError if stdin is closed (piped input). Not caught.
- sys.stdout.write(): Could raise UnicodeEncodeError if terminal encoding doesn't support characters. Not caught.
- time.sleep(): Could be interrupted by KeyboardInterrupt. In typewrite(), this would leave partially printed text.

---

## Performance Characteristics

- clear(): ~10-50 ms (system call).
- typewrite(): O(n * delay) where n = text length. A 500-character text at 0.018s = 9 seconds.
- show_story(): O(lines * avg_line_length * delay). Can be 10-30 seconds per story.
- prompt_input(): Blocks indefinitely. No timeout.
- xp_bar(): O(width). Instant.
- **Overall:** The display layer dominates wall-clock time. A typical mission spends 80%+ of its time in time.sleep() waiting for animations or user input.

---

## Observable Effects

- Terminal screen is cleared and redrawn.
- ANSI colors appear (if terminal supports them).
- Text appears character-by-character in typewrite().
- User must press Enter to continue at prompt_continue().
- Cursor waits at prompt_input().

---

## Why This Design

The display layer is intentionally thin and stateless. It does not manage a screen buffer, a windowing system, or a rendering loop. It prints ANSI-escaped strings directly to stdout because that is the simplest cross-platform way to create a "pretty" terminal application without dependencies. The C color class uses hardcoded ANSI escape sequences because they are universally supported in modern terminals.

---

## Assessment

### What feels incomplete

**The issue:** No fallback for terminals that do not support ANSI escape codes. If the terminal is `dumb` or `xterm-mono`, the output will show raw escape sequences like `[38;5;51m` mixed with the text.

**ELI5:** Imagine sending a color-coded letter to someone who is colorblind. They can still read the words, but the formatting instructions are printed as gibberish between the sentences.

**Impact:** On Windows Command Prompt (pre-Windows Terminal), certain terminals, or CI logs, the output is unreadable. This breaks the game experience for users on older Windows or minimal terminals.

**Robust Fixes:**
1. Detect terminal capabilities using `os.environ.get('TERM')` or `sys.stdout.isatty()`.
2. If not a TTY or TERM is `dumb`, set all `C.*` attributes to empty strings (no-color mode).
3. Alternatively, accept a `--no-color` CLI flag.
4. Use the `colorama` library (optional dependency) for Windows compatibility.

---

### What feels vulnerable

**The issue:** clear() uses `os.system('clear')` / `os.system('cls')` which shells out to the OS. While the argument is hardcoded here, this pattern is a security anti-pattern.

**ELI5:** Imagine asking a stranger to clean your room by saying "Hey, do whatever is written on this note." If someone swapped the note, they could make the stranger do something dangerous.

**Impact:** In restricted environments (AppArmor, SELinux), os.system() may be blocked entirely, causing the game to fail at startup. Also, os.system() is slower than native ANSI clearing.

**Robust Fixes:**
1. Replace os.system('clear') with ANSI escape sequence `\033[2J\033[H` (clear screen + home cursor).
2. On Windows, use `ctypes.windll.kernel32` to clear the console without shelling out.
3. Never use os.system() in any part of the codebase.

---

### What feels like bad design

**The issue:** Animation delays (time.sleep()) are hardcoded inside display functions, making them untestable and inaccessible.

**ELI5:** Imagine a movie where the director glued the pause button to the remote control. Every time you watch the movie, it pauses at the same spots for the same amount of time, and there's no way to fast-forward or skip.

**Impact:**
- **Testing:** Automated tests must wait for time.sleep() to finish. A test suite that covers 10 missions would spend minutes doing nothing.
- **Accessibility:** Users with motor impairments or reading difficulties cannot speed up or skip animations.
- **Speedrunners:** The hardcoded delays add unavoidable overhead to speedrun times.
- **CI/CD:** Running the game in a headless test environment is impossible because input() blocks forever.

**Robust Fixes:**
1. Extract delay parameters to module-level constants or a Config object: `TYPEWRITE_DELAY = 0.018`.
2. Add an `animate: bool = True` parameter to every display function. Tests and speedruns can pass `animate=False`.
3. Implement a `DisplayDriver` abstraction with two implementations: `AnimatedDisplay` (uses time.sleep()) and `InstantDisplay` (no delays).
4. For input(), create an `InputDriver` interface that can be mocked in tests with pre-programmed responses.
