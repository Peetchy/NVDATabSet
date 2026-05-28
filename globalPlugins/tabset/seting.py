from io import StringIO
import os
import configobj
from configobj import validate
import globalVars

seting_filename = "tabset.ini"

_config = None

config_spec = StringIO( """
[stock_favorite]
	key_a = string( default="ADVANC" )
	key_b = string( default="AOT" )
	key_c = string( default="BBL" )
	key_d = string( default="BTS" )
	key_e = string( default="CPALL" )
	key_f = string( default="CPF" )
	key_g = string( default="CRC" )
	key_h = string( default="DTAC" )
	key_i = string( default="EA" )
	key_j = string( default="GPSC" )
	key_k = string( default="GULF" )
	key_l = string( default="INTUCH" )
	key_m = string( default="KBANK" )
	key_n = string( default="KTB" )
	key_o = string( default="KTC" )
	key_p = string( default="MINT" )
	key_q = string( default="OR" )
	key_r = string( default="PTT" )
	key_s = string( default="SCB" )
	key_t = string( default="SCC" )
	key_u = string( default="SCGP" )
	key_v = string( default="TISCO" )
	key_w = string( default="TTB" )
	key_x = string( default="TRUE" )
	key_y = string( default="TU" )
	key_z = string( default="VGI" )
	key_1 = string( default="AWC" )
	key_2 = string( default="BAM" )
	key_3 = string( default="BANPU" )
	key_4 = string( default="BDMS" )
	key_5 = string( default="BH" )
	key_6 = string( default="CENTEL" )
	key_7 = string( default="DELTA" )
	key_8 = string( default="GUNKUL" )
	key_9 = string( default="HMPRO" )
	key_0 = string( default="IRPC" )
	key_, = string( default="JAS" )
	key_. = string( default="JMART" )
	key_/ = string( default="KKP" )
	key_; = string( default="KCE" )
	key_' = string( default="MAJOR" )
	key_[ = string( default="PTG" )
	key_] = string( default="STA" )
	key_- = string( default="TCAP" )
	key_\ = string( default="TQM" )
[view_option]
	view_type = string( default="price" )
	view_lang = string( default="th" )

[more_option]
	copy_result_to_clipboard = boolean( default=False )
""" )

def get_seting( ):
	global _config
	if not _config:
		path = os.path.abspath( os.path.join( globalVars.appArgs.configPath, seting_filename ) )
		_config = configobj.ConfigObj( infile=path, configspec=config_spec, create_empty=True )
		val = validate.Validator( )
		_config.validate( val, copy=True )
		_config.write()
	return _config

def save_seting_favorite( fav_stock ):
	conf = get_seting( )
	for k in fav_stock.keys():
		if conf['stock_favorite']['key_'+ k ] != fav_stock[k]:
			conf['stock_favorite']['key_'+ k ] = fav_stock[k]
	conf.write()

def save_seting_lang( lang ):
	conf = get_seting( )
	if conf['view_option']['view_lang'] != lang:
		conf['view_option']['view_lang'] = lang
		conf.write()

def save_seting_view_type( type ):
	conf = get_seting( )
	if conf['view_option']['view_type'] != type:
		conf['view_option']['view_type'] = type
		conf.write()

def save_seting_copy_information_to_clipboard( state ):
	conf = get_seting( )
	if state == True or state == False and conf['more_option']['copy_result_to_clipboard'] != state:
		conf['more_option']['copy_result_to_clipboard'] = state
		conf.write()
