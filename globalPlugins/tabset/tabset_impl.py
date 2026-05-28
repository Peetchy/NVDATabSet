import threading
from . import tabset

class TabSetNVDAImplementation( threading.Thread, tabset.TabSet ):

	def __init__( self, *args, **kwargs ):
		super( TabSetNVDAImplementation, self ).__init__( *args, **kwargs )
		self._stopEvent = threading.Event()
		self.stock_symbol = ""
		self.view_type = ""
		self.stock_text_info = ""

	def stop( self ):
		self._stopEvent.set()

	def run( self ):
		stock_info = None
		if self.view_type == "price": stock_info = self.get_stock_price( self.stock_symbol )
		elif self.view_type == "info": stock_info = self.get_stock_info( self.stock_symbol )
		if stock_info:
			self.stock_text_info = self.stock_info_to_text( stock_info )
