import os, sys
import re
from urllib.request import Request, urlopen
baseDir = os.path.dirname( __file__ )
libs = os.path.join( baseDir, "lib" )
if libs not in sys.path:
	sys.path.insert( 0, libs )
from bs4 import BeautifulSoup

class TabSet:

	lang: str
	stock_key_definition = {
		"title": {
			"en": "Company Name",
			"th": "ชื่อบริษัท",
		}, "last": {
			"en": "Last",
			"th": "ล่าสุด",
		}, "change": {
			"en": "Change",
			"th": "เปลี่ยนแปลง",
		}, "percentChange": {
			"en": "Change%",
			"th": "เปลี่ยนแปลง %",
		}, "prior": {
			"en": "Prior",
			"th": "วันก่อนหน้า",
		}, "open": {
			"en": "Open",
			"th": "เปิด",
		}, "high": {
			"en": "High",
			"th": "สูงสุด",
		}, "low": {
			"en": "Low",
			"th": "ต่ำสุด",
		}, "update": {
			"en": "Update",
			"th": "อัพเดท",
		}, "pe": {
			"en": "P/E",
			"th": "P/E",
		}, "dvd": {
			"en": "DVD",
			"th": "DVD",
		}, "pvv": {
			"en": "PVV",
			"th": "PVV",
		}, "marketcap": {
			"en": "Market Cap",
			"th": "มูลค่าตลาด",
		},
	}

	def __init__( self, **args ):
		self.lang = args["lang"] if "lang" in args else "th"

	@staticmethod
	def validate_and_align_stock_symbol( symbol ):
		symbol = TabSet.__clean_text( symbol ).upper()
		if re.search( "[A-Z]", symbol ) == None: return False
		if re.sub( "[0-9A-Z\-]+", "", symbol ) != "": return False
		return symbol

	def __clean_text( text ):
		without_str = ["\\n", "\\r", "\n", "\r" ]
		for s in without_str:
			text = text.replace( s, "" )
		return text.strip()

	def __compact_text( text ):
		return " ".join( TabSet.__clean_text( text ).split() )

	def __get_company_title( dom ):
		for node in dom.find_all( "div" ):
			if "title" in ( node.get( "class" ) or [] ):
				title = TabSet.__compact_text( node.get_text( " ", strip=True ) )
				if title:
					return title
		heading = dom.find( "h1" )
		return TabSet.__compact_text( heading.get_text( " ", strip=True ) ) if heading else ""

	def __get_label_value( dom, labels ):
		if isinstance( labels, str ):
			labels = [ labels ]
		for label in labels:
			label_node = dom.find(
				lambda tag: tag.name == "label"
				and TabSet.__compact_text( tag.get_text( " ", strip=True ) ) == label
			)
			if not label_node or not label_node.parent:
				continue
			spans = label_node.parent.find_all( "span" )
			if spans:
				return TabSet.__compact_text(
					" ".join( span.get_text( " ", strip=True ) for span in spans )
				)
			parent_text = TabSet.__compact_text( label_node.parent.get_text( " ", strip=True ) )
			return parent_text.replace( label, "", 1 ).strip()
		return ""

	def __get_last_update( dom ):
		for node in dom.find_all( True ):
			classes = node.get( "class" ) or []
			if "price-detail-date" not in classes and "quote-market-lastInfo" not in classes:
				continue
			text = TabSet.__compact_text( node.get_text( " ", strip=True ) )
			if "Last Update" in text:
				return text.replace( "Last Update :", "", 1 ).replace( "Last Update", "", 1 ).strip()
		return ""

	def request_stock_page( self, stock_symbol, **args ):
		if "info" not in args: args["info"] = "price"
		if args["info"] == "sprice": url = "https://www.set.or.th/en/market/product/stock/quote/{}/price".format( stock_symbol.lower() )
		elif args["info"] == "sinfo": url = "https://www.set.or.th/en/market/product/stock/quote/{}/factsheet".format( stock_symbol.lower() )
		else: return None
		try:
			request = Request( url, headers={
				"User-Agent": "Mozilla/5.0",
				"Accept-Language": "en-US,en;q=0.9",
			} )
			with urlopen( request, timeout=15 ) as page_request:
				if page_request.getcode() != 200: return None
				page_content = page_request.read().decode('utf-8')
		except Exception:
			return None
		soup = BeautifulSoup( page_content, "html.parser" )
		return soup

	def get_stock_price( self, stock_symbol ):
		dom = self.request_stock_page( stock_symbol, info="sprice" )
		if dom == None: return ""
		stock_price_info = {
			"title": "",
			"last": "",
			"change": "",
			"percentChange": "",
			"prior": "",
			"open": "",
			"high": "",
			"low": "",
			"update": "",
		}
		stock_price_info['title'] = TabSet.__get_company_title( dom )
		stock_price_info['last'] = TabSet.__get_label_value( dom, "Last" )
		change_text = TabSet.__get_label_value( dom, "Change" )
		change_match = re.match( r"(.+?)\s*\((.+)\)", change_text )
		if change_match:
			stock_price_info['change'] = change_match.group( 1 ).strip()
			stock_price_info['percentChange'] = change_match.group( 2 ).strip()
		else:
			stock_price_info['change'] = change_text
		stock_price_info['prior'] = TabSet.__get_label_value( dom, "Prior" )
		stock_price_info['open'] = TabSet.__get_label_value( dom, "Open" )
		stock_price_info['high'] = TabSet.__get_label_value( dom, "High" )
		stock_price_info['low'] = TabSet.__get_label_value( dom, "Low" )
		stock_price_info['update'] = TabSet.__get_last_update( dom )
		return stock_price_info

	def get_stock_info( self, stock_symbol ):
		dom = self.request_stock_page( stock_symbol, info="sinfo" )
		if dom == None: return ""
		stock_profile_info = {
			"title": "",
			"pe": "",
			"dvd": "",
			"pvv": "",
			"marketcap": "",
		}
		stock_profile_info['title'] = TabSet.__get_company_title( dom )
		if stock_profile_info['title'] in ( "", "-", "Change" ):
			stock_profile_info['title'] = stock_symbol.upper()
		stock_profile_info['pe'] = TabSet.__get_label_value( dom, "P/E (X)" )
		stock_profile_info['dvd'] = TabSet.__get_label_value( dom, "Dividend Yield (%)" )
		stock_profile_info['pvv'] = TabSet.__get_label_value( dom, "P/BV (X)" )
		stock_profile_info['marketcap'] = TabSet.__get_label_value( dom, "Market Cap (M.Baht)" )
		return stock_profile_info

	def stock_info_to_text( self, stock_info ):
		text_info = ""
		for key in stock_info.keys():
			if self.stock_key_definition.get( key ) != None:
				text_info += "{} : {}\n".format( self.stock_key_definition[ key ][ self.lang ], stock_info[key] )
		return text_info

""" if __name__ == '__main__':
	tabset = TabSet( )
	symbol = input("Please enter stock symbol")
	symbol = tabset.validate_and_align_stock_symbol(symbol)
	if symbol == False: continue
	stock_info = tabset.get_stock_price( symbol )
	if stock_info: print( tabset.stock_info_to_text( stock_info ) )
"""
