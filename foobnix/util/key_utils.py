'''
Created on Oct 21, 2010

@author: ivan
'''

from gi.repository import Gtk
from gi.repository import Gdk

KEY_DELETE = 'Delete'
KEY_RETURN = 'Return'

def is_key(event, key_const):
    const = Gdk.keyval_name(event.keyval) #@UndefinedVariable
    #LOG.debug("KEY", const)
    return const == key_const

def get_key(event):
    const = Gdk.keyval_name(event.keyval) #@UndefinedVariable
    #LOG.debug("KEY", const)    
    return const

def is_key_enter(e):
    return is_key(e, 'Return') or is_key(e, 'KP_Enter')

def is_key_control(event): 
    return event.state & Gdk.ModifierType.CONTROL_MASK   #@UndefinedVariable

def is_key_shift(event): 
    return event.state & Gdk.ModifierType.SHIFT_MASK     #@UndefinedVariable

def is_key_super(event): 
    return event.state & Gdk.ModifierType.SUPER_MASK    #@UndefinedVariable

def is_key_alt(event):
    return event.state & Gdk.ModifierType.MOD1_MASK     # | Gtk.gdk.MOD2_MASK #@UndefinedVariable

def is_modificator(event):
    if is_key_control(event) or is_key_shift(event) or is_key_super(event) or is_key_alt(event):
        return True
