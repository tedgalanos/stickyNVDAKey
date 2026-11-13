# Sticky NVDA Key

Makes the NVDA modifier key sticky, like the JAWS "Insert Key Mode"
checkbox, without needing Windows Sticky Keys to be turned on.

Press the NVDA key (Insert by default, or Numpad Insert / Caps Lock
if you have those set as NVDA keys) once and let it go, then press
the next key. Press Insert twice quickly to lock it on, and press
it again to unlock.

## Install

Download `stickyNVDAKey-1.0.0.nvda-addon` from the latest release
on this repository's Releases page and open it while NVDA is
running. NVDA will ask you to confirm, then restart.

Works with NVDA 2024.1 through 2026.3.

## How to use it

- Insert, then N — opens the NVDA menu (NVDA+N)
- Insert, then T — reads the window title (NVDA+T)

You will hear a high beep when the NVDA key latches, and a low
beep when it unlatches.

Press Insert twice quickly to lock it on, so you can run several
NVDA commands in a row without pressing Insert each time.
Press Insert again to unlock it.

## Turning it on and off

It is on by default when the add-on is installed.

- NVDA menu, Preferences, Settings, Sticky NVDA Key:
  uncheck "Make the NVDA key sticky" — this is the JAWS-style
  checkbox. The other two checkboxes there turn the double-press
  lock and the latch beeps on or off.
- Or press Control+Alt+Shift+K anywhere to toggle it on or off.
  NVDA will say "Sticky NVDA key on" or "Sticky NVDA key off".

## Notes

- Do not run JAWS and NVDA at the same time, since both grab the
  Insert key.
- If you have the old stickyModifier add-on installed, remove or
  disable it first — it is out of date for NVDA 2026.
- This does not change Windows Sticky Keys, and it does not change
  how Control, Alt, Shift or the Windows key behave. It only
  affects the NVDA key, inside NVDA.

## How it works, briefly

NVDA already has sticky NVDA-key code, but it only runs when
Windows says Windows Sticky Keys is on. This add-on makes NVDA
think Sticky Keys is on, for NVDA's own check only, so NVDA's
own latch/lock code runs. It is a rebuilt version of Tyler
Spivey's 2019 "stickyModifier" add-on, updated for NVDA 2024.1
to 2026.3, with a settings panel and a toggle command.

## Building the add-on file

From the root of this repository:

```sh
zip -r stickyNVDAKey-1.0.0.nvda-addon manifest.ini globalPlugins doc
```

## License

GNU General Public License, version 2. See `LICENSE`.

## Author

Ted Galanos
