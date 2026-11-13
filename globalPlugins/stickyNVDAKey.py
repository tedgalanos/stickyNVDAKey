# Sticky NVDA Key
# Makes the NVDA modifier key (Insert / Numpad Insert / Caps Lock)
# sticky, like the JAWS "Insert Key Mode" checkbox, without needing
# Windows Sticky Keys to be turned on.
#
# How it works
# -----------
# NVDA already contains sticky NVDA-modifier code in
# source/keyboardHandler.py (stickyNVDAModifier /
# stickyNVDAModifierLocked), but it only runs when Windows reports
# that Windows Sticky Keys is on:
#     stickyKeysFlags = winUser.getSystemStickyKeys().dwFlags
#     if stickyKeysFlags & winUser.SKF_STICKYKEYSON: ...
# This add-on does NOT change Windows, and does NOT re-implement
# NVDA's latch/lock logic. It only makes NVDA *think* Sticky Keys
# is on, for NVDA's own query, so NVDA's own tested code runs:
# press Insert once -> it latches for the next key (with a beep),
# press Insert twice -> it locks until pressed again,
# press any other key -> the latch is released after that key.
# That is the same trick Tyler Spivey's 2019 "stickyModifier"
# add-on used; this is a rebuilt, maintained version for NVDA
# 2024.1-2026.3, with a real on/off setting in NVDA Settings
# (like the JAWS checkbox) and a toggle command.
#
# Turning the add-on off in Settings, or disabling / uninstalling
# it, restores NVDA's original function and clears any latched
# NVDA modifier, so the key cannot be left stuck down.

import addonHandler
import config
import globalPluginHandler
import gui
import keyboardHandler
import ui
import winUser
import wx
from logHandler import log
from scriptHandler import script

addonHandler.initTranslation()

CONFIG_SECTION = "stickyNVDAKey"

_confspec = {
	"enabled": "boolean(default=true)",
	"lockOnDoublePress": "boolean(default=true)",
	"beepOnLatch": "boolean(default=true)",
}

# Cached settings, read by the patched function on every key press.
# They are plain booleans on purpose: the keyboard hook path must
# stay fast and must not touch config, speech, or the GUI.
_enabled = True
_lockEnabled = True
_beepEnabled = True

_originalGetSystemStickyKeys = None
_isPatched = False


def _refreshFromConfig():
	"""Copy the saved settings into the cached flags."""
	global _enabled, _lockEnabled, _beepEnabled
	try:
		section = config.conf[CONFIG_SECTION]
		_enabled = bool(section["enabled"])
		_lockEnabled = bool(section["lockOnDoublePress"])
		_beepEnabled = bool(section["beepOnLatch"])
	except Exception:
		log.debugWarning("Sticky NVDA Key: could not read config, using defaults")
		_enabled = True
		_lockEnabled = True
		_beepEnabled = True


def _patchedGetSystemStickyKeys():
	"""NVDA's view of the Windows Sticky Keys flags.

	Returns the real flags, with SKF_STICKYKEYSON (and, if enabled,
	SKF_TRISTATE for double-press locking and SKF_AUDIBLEFEEDBACK
	for the latch/unlatch beeps) added when this add-on is enabled.
	Windows itself is never changed.
	"""
	sk = _originalGetSystemStickyKeys()
	if _enabled:
		sk.dwFlags |= winUser.SKF_STICKYKEYSON
		if _lockEnabled:
			sk.dwFlags |= winUser.SKF_TRISTATE
		else:
			sk.dwFlags &= ~winUser.SKF_TRISTATE
		if _beepEnabled:
			sk.dwFlags |= winUser.SKF_AUDIBLEFEEDBACK
		else:
			sk.dwFlags &= ~winUser.SKF_AUDIBLEFEEDBACK
	return sk


def _installPatch():
	global _originalGetSystemStickyKeys, _isPatched
	if _isPatched:
		return
	_originalGetSystemStickyKeys = winUser.getSystemStickyKeys
	winUser.getSystemStickyKeys = _patchedGetSystemStickyKeys
	_isPatched = True


def _clearStickyState():
	"""Release any latched/locked NVDA modifier in NVDA core."""
	try:
		sticky = getattr(keyboardHandler, "stickyNVDAModifier", None)
		if sticky is not None:
			try:
				keyboardHandler.currentModifiers.discard(sticky)
			except Exception:
				pass
			keyboardHandler.stickyNVDAModifier = None
			keyboardHandler.stickyNVDAModifierLocked = False
	except Exception:
		log.debugWarning("Sticky NVDA Key: could not clear sticky state", exc_info=True)


def _removePatch():
	global _originalGetSystemStickyKeys, _isPatched
	if not _isPatched:
		return
	_clearStickyState()
	try:
		winUser.getSystemStickyKeys = _originalGetSystemStickyKeys
	finally:
		_originalGetSystemStickyKeys = None
		_isPatched = False


class StickyNVDAKeySettingsPanel(gui.settingsDialogs.SettingsPanel):
	# Translators: Title of the Sticky NVDA Key settings panel.
	title = _("Sticky NVDA Key")

	def makeSettings(self, settingsSizer):
		helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: Label of the checkbox that turns the sticky NVDA key on or off.
		self.enabledCheckBox = helper.addItem(
			wx.CheckBox(
				self,
				label=_("&Make the NVDA key sticky, like JAWS Insert Key Mode"),
			)
		)
		self.enabledCheckBox.SetValue(config.conf[CONFIG_SECTION]["enabled"])
		# Translators: Label of the checkbox for locking the NVDA key with a double press.
		self.lockCheckBox = helper.addItem(
			wx.CheckBox(
				self,
				label=_("Press the NVDA key twice to &lock it (press again to unlock)"),
			)
		)
		self.lockCheckBox.SetValue(config.conf[CONFIG_SECTION]["lockOnDoublePress"])
		# Translators: Label of the checkbox for beeping when the NVDA key latches.
		self.beepCheckBox = helper.addItem(
			wx.CheckBox(
				self,
				label=_("&Beep when the NVDA key latches or unlatches"),
			)
		)
		self.beepCheckBox.SetValue(config.conf[CONFIG_SECTION]["beepOnLatch"])

	def onSave(self):
		config.conf[CONFIG_SECTION]["enabled"] = self.enabledCheckBox.GetValue()
		config.conf[CONFIG_SECTION]["lockOnDoublePress"] = self.lockCheckBox.GetValue()
		config.conf[CONFIG_SECTION]["beepOnLatch"] = self.beepCheckBox.GetValue()
		_refreshFromConfig()
		if not _enabled:
			_clearStickyState()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Translators: Category for the Sticky NVDA Key command in the Input Gestures dialog.
	scriptCategory = _("Sticky NVDA Key")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		config.conf.spec[CONFIG_SECTION] = _confspec
		_refreshFromConfig()
		try:
			_installPatch()
		except Exception:
			log.error("Sticky NVDA Key: could not install patch", exc_info=True)
		try:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
				StickyNVDAKeySettingsPanel
			)
		except Exception:
			log.debugWarning(
				"Sticky NVDA Key: could not add settings panel", exc_info=True
			)

	def terminate(self):
		try:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
				StickyNVDAKeySettingsPanel
			)
		except Exception:
			pass
		try:
			_removePatch()
		except Exception:
			log.debugWarning(
				"Sticky NVDA Key: could not remove patch", exc_info=True
			)
		super().terminate()

	@script(
		# Translators: Description of the command that toggles the sticky NVDA key.
		description=_("Toggles whether the NVDA key is sticky"),
		gesture="kb:control+alt+shift+k",
	)
	def script_toggleStickyNVDAKey(self, gesture):
		newValue = not config.conf[CONFIG_SECTION]["enabled"]
		config.conf[CONFIG_SECTION]["enabled"] = newValue
		_refreshFromConfig()
		if not newValue:
			_clearStickyState()
		# Translators: Announced when the sticky NVDA key is turned on or off.
		ui.message(_("Sticky NVDA key on") if newValue else _("Sticky NVDA key off"))
