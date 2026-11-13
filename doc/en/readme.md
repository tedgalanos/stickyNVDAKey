# Sticky NVDA Key

Makes the NVDA modifier key sticky, like the JAWS "Insert Key Mode"
checkbox, without needing Windows Sticky Keys to be turned on.

## How to use it

Press the NVDA key (Insert by default, or Numpad Insert / Caps Lock
if you have those set as NVDA keys in NVDA Settings, Keyboard)
once and let it go, then press the next key.

Examples, one key at a time:

- Insert, then N — opens the NVDA menu (NVDA+N)
- Insert, then T — reads the window title (NVDA+T)
- Insert, then Shift+T — reads the window title in the other
  direction, using Windows Sticky Keys for Shift if you have that on

You will hear a high beep when the NVDA key latches, and a low
beep when it unlatches.

Press Insert twice quickly to lock it on, so you can run several
NVDA commands in a row without pressing Insert each time.
Press Insert again to unlock it.

Pressing Insert twice quickly with nothing after it still sends
a plain Insert to the application, as NVDA normally does.

## Turning it on and off

It is on by default when the add-on is installed.

- NVDA menu, Preferences, Settings, Sticky NVDA Key:
  uncheck "Make the NVDA key sticky" — this is the JAWS-style
  checkbox. The other two checkboxes there turn the double-press
  lock and the latch beeps on or off.
- Or press Control+Alt+Shift+K anywhere to toggle it on or off.
  NVDA will say "Sticky NVDA key on" or "Sticky NVDA key off".
  Control, Alt and Shift are ordinary Windows modifiers, so
  Windows Sticky Keys already makes that combination pressable
  one key at a time.

## Notes

- This does not change Windows Sticky Keys, and it does not
  change how Control, Alt, Shift or the Windows key behave.
  It only affects the NVDA key, inside NVDA.
- It works with whichever keys you have checked as NVDA keys
  in NVDA Settings, Keyboard: Insert, Numpad Insert, Caps Lock.
- Disabling or uninstalling the add-on restores NVDA's normal
  behaviour and clears any latched NVDA key.

## How it works, briefly

NVDA already has sticky NVDA-key code, but it only runs when
Windows says Windows Sticky Keys is on. This add-on makes NVDA
think Sticky Keys is on, for NVDA's own check only, so NVDA's
own latch/lock code runs. It is a rebuilt version of Tyler
Spivey's 2019 "stickyModifier" add-on, updated for NVDA 2024.1
to 2026.3, with a settings panel and a toggle command.
