import sys, os
import globalPluginHandler
import addonHandler
import api
import time
import threading
import winsound
import ui
import wx
import gui
from gui.settingsDialogs import NVDASettingsDialog, SettingsDialog, SettingsPanel
from logHandler import log
from scriptHandler import script
from . import seting
from . import tabset_impl

addon_name = "NVDA TabSet"

def playsound ( actionName ):
	soundPath = os.path.join( os.path.dirname( __file__ ), "media\\{}.wav".format( actionName ) )
	if os.path.exists( soundPath ):
		winsound.PlaySound( soundPath, winsound.SND_ASYNC )

class GlobalPlugin( globalPluginHandler.GlobalPlugin ):

	enableTabset = False
	scriptCategory = addon_name

	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )
		self._tabsetGestureIdentifiers = []
		if TSPanel not in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.append( TSPanel )

	def terminate( self ):
		try:
			self._removeTabsetGestureBindings()
			if TSPanel in NVDASettingsDialog.categoryClasses:
				NVDASettingsDialog.categoryClasses.remove( TSPanel )
		finally:
			super().terminate()

	def _removeTabsetGestureBindings( self ):
		for gestureIdentifier in self._tabsetGestureIdentifiers:
			try:
				self.removeGestureBinding( gestureIdentifier )
			except LookupError:
				pass
		self._tabsetGestureIdentifiers = []

	def script_viewStock( self, gesture ):
		keypress = gesture._get_mainKeyName()
		symbol = self._config['stock_favorite']['key_'+ keypress ]
		view_type = self._config['view_option']['view_type']
		lang = self._config['view_option']['view_lang']
		threading.Thread( target=self.getStockInfo, args=( symbol, view_type, lang )).start()

	def getStockInfo( self, symbol, viewType, lang ):
		tabset = tabset_impl.TabSetNVDAImplementation()
		tabset.stock_symbol = symbol
		tabset.view_type = viewType
		tabset.lang = lang
		tabset.start()
		i=0
		while tabset.is_alive( ):
			time.sleep(0.1)
			i+=1
			if i == 10:
				playsound( "loading" )
				i = 0
		tabset.join()
		if tabset.stock_text_info:
			playsound( "complete" )
			ui.message( symbol + "\n" + tabset.stock_text_info )
			if self._config['more_option']['copy_result_to_clipboard']: api.copyToClip( tabset.stock_text_info )
		else:
			playsound( "fail" )

	@script(
		description="Open NVDA Tabset Setting.",
		category=addon_name
	)
	def script_activateNVDATabSetSettingsDialog(self, gesture):
		if self.enableTabset is True:
			self.script_tabset( None )
		wx.CallAfter( gui.mainFrame._popupSettingsDialog, NVDASettingsDialog, TSPanel )

	@script(
		description="Toggle NVDA TabSet on or off.",
		category=addon_name,
		gesture="kb:nvda+alt+t"
	)
	def script_tabset( self, gesture ):
		self.enableTabset = not self.enableTabset
		if self.enableTabset is True:
			playsound( "start" )
			ui.message( addon_name )
			self._config = seting.get_seting()
			self._tabsetGestureIdentifiers = []
			for k in self._config['stock_favorite']:
				gestureIdentifier = "kb:{}".format( k[4:] )
				self.bindGesture( gestureIdentifier, "viewStock" )
				self._tabsetGestureIdentifiers.append( gestureIdentifier )
			for gestureIdentifier, scriptName in (
				( "kb:escape", "tabset" ),
				( "kb:=", "activateNVDATabSetSettingsDialog" ),
			):
				self.bindGesture( gestureIdentifier, scriptName )
				self._tabsetGestureIdentifiers.append( gestureIdentifier )
		else:
			playsound( "close" )
			self._removeTabsetGestureBindings()
			ui.message( "{} Closed".format( addon_name ) )

class TSPanel( SettingsPanel ):

	title = addon_name
	helpId = addon_name.replace(" ", "")

	def makeSettings( self, settingsSizer ):
		settingHelper = gui.guiHelper.BoxSizerHelper( self, sizer=settingsSizer )
		self._config = seting.get_seting()
		settingHelper.addItem( wx.StaticText( self, label="Favorite Stock" ))
		self.favorite_stock_lbox = settingHelper.addItem(
			wx.ListBox( self, choices = self.get_favorite_stock_symbol(), style=wx.LB_SINGLE )
		)
		self.edit_fav_stock_btn = settingHelper.addItem( wx.Button( self, label="Edit Stock" ) )
		self.edit_fav_stock_btn.Bind( wx.EVT_BUTTON, self.edit_favorite_stock_symbol )
		settingHelper.addItem( wx.StaticText( self, label="Display stock data by " ))
		self.view_type_lbox = settingHelper.addItem(
			wx.ListBox( self, choices=[ "Stock Price", "Stock Information" ], style=wx.LB_SINGLE )
		)
		settingHelper.addItem( wx.StaticText( self, label="Set language to " ))
		self.view_lang_lbox = settingHelper.addItem(
			wx.ListBox( self, choices=[ "English-US", "Thai-ภาษาไทย" ], style=wx.LB_SINGLE )
		)
		self.copy_to_clipboard_cbox = settingHelper.addItem( wx.CheckBox( self, label="Copy stock information to clipboard." ) )
		self.favorite_stock_lbox.SetSelection( 0 )
		self.view_lang_lbox.SetSelection( 0 ) if self._config['view_option']['view_lang'] == 'en' else self.view_lang_lbox.SetSelection( 1 )
		self.view_type_lbox.SetSelection( 0 ) if self._config['view_option']['view_type'] == 'price' else self.view_type_lbox.SetSelection( 1 )
		if self._config['more_option']['copy_result_to_clipboard'] == True: self.copy_to_clipboard_cbox.SetValue( True )

	def onSave( self ):
		viewType = "price" if self.view_type_lbox.GetSelection() == 0 else "info"
		seting.save_seting_view_type( viewType )
		viewLang = "en" if self.view_lang_lbox.GetSelection() == 0 else "th"
		seting.save_seting_lang( viewLang )
		copyInfoState = self.copy_to_clipboard_cbox.GetValue()
		seting.save_seting_copy_information_to_clipboard( copyInfoState )

	def edit_favorite_stock_symbol( self, evt ):
		# cstock = self.favorite_stock_lbox.GetSelection()
		editStock = EditFavoriteStockDialog( self, multiInstanceAllowed=True )
		ret = editStock.ShowModal( )
		if ret == wx.ID_OK:
			self.Freeze()
			self.onPanelActivated()
			self._sendLayoutUpdatedEvent()
			self.Thaw()

	def get_favorite_stock_symbol( self ):
		symbols = []
		for k in self._config['stock_favorite']:
			symbols.append( k[4:].upper() +" : "+ self._config['stock_favorite'][k].upper() )
		return symbols

	def update_stock_symbol( self, key, newSymbol ):
		seting.save_seting_favorite( {
			""+key.lower(): newSymbol,
		} )

	def update_current_selection_text( self, keyWithSymbol ):
		self.favorite_stock_lbox.SetString( self.favorite_stock_lbox.GetSelection( ), keyWithSymbol )

class EditFavoriteStockDialog( SettingsDialog ):

	title = "Edit Favorite Stock."

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		stockSelectionList = self.Parent.favorite_stock_lbox
		currentStockSelectionTexts = stockSelectionList.GetString( stockSelectionList.GetSelection() ).replace( " ", "" ).split( ":" )
		self.keyMap = currentStockSelectionTexts[0]
		self.currentStockSymbol = currentStockSelectionTexts[-1]
		self.editFavStockEdb = sHelper.addLabeledControl( "New Stock Name for key {}.".format( self.keyMap ), wx.TextCtrl )
		self.editFavStockEdb.SetValue( self.currentStockSymbol )

	def postInit( self ):
		self.editFavStockEdb.SetFocus()

	def onOk( self, evt ):
		newSymbol = tabset_impl.TabSetNVDAImplementation.validate_and_align_stock_symbol( self.editFavStockEdb.GetValue() )
		if newSymbol == False:
			ui.message( "Invalid Stock name.")
			return
		if self.IsModal():
			self.Parent.update_stock_symbol( self.keyMap, newSymbol )
			self.Parent.update_current_selection_text( self.keyMap +" : "+ newSymbol )
		super( EditFavoriteStockDialog, self ).onOk( evt )
