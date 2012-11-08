################################################################################
#                                                                              #
# This file is part of the gedit XML encode plugin.                            #
#                                                                              #
# The gedit XML encode plugin is free software: you can redistribute it and/or #
# modify it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or (at your   #
# option) any later version.                                                   #
#                                                                              #
# The gedit XML encode plugin is distributed in the hope that it will be       #
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General    #
# Public License for more details.                                             #
#                                                                              #
# You should have received a copy of the GNU General Public License along with #
# the gedit XML encode plugin.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                              #
################################################################################

"""gedit XML enocde plugin

This script is a plugin script intended to be used by gedit. It creates a few
new edit menu commands in gedit that replace all of the special XML characters
in a document or selection with their encoded entities.

The special XML characters and their entity replacements are:
    & => &amp;
    < => &lt;
    > => &gt;
    " => &quot;
    ' => &apos;
"""

from gi.repository import GObject, Gtk, Gedit, Peas

import gettext
import os

PLUGIN_MODULE_NAME = "xml-encode"

# Enable localization, if available
GETTEXT_PACKAGE = ""
_  = lambda s: s
P_ = lambda s1, s2, n: s1 if n == 1 else s2

# Menu user interface description
menu_ui = """
<ui>
  <menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_4">
        <menu name="XmlEncode" action="XmlEncode">
          <menuitem name="XmlEncodeDocument"  action="XmlEncodeDocument"/>
          <menuitem name="XmlEncodeSelection" action="XmlEncodeSelection"/>
        </menu>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

# XML special characters
xml_special_chars = {
    '&' : '&amp;',
    '<' : '&lt;',
    '>' : '&gt;',
    '"' : '&quot;',
    "'" : '&apos;',
}

class XmlEncodePlugin(GObject.Object, Gedit.WindowActivatable):
    """gedit plugin to replace XML special characters with their entities.
    
    All of the real work is done in the do_encode() function. There are two
    wrapper functions - encode_doc() and encode_sel() - which correspond to the
    menu commands.
    """
    
    __gtype_name__ = "XmlEncodePlugin"
    
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        """Initialize the plugin."""
        
        GObject.Object.__init__(self)
    
    def do_activate(self):
        """Activate the plugin.
        
        First initialize the translations - read the gettext domain from the
        plugin config file, then bind it, and set up some simple wrapper
        functions - then set up the menu UI.
        """
        
        self._init_translations()
        self._insert_menu()
    
    def do_deactivate(self):
        """Deactivate the plugin."""
        
        self._remove_menu()
    
    def do_update_state(self):
        """Update the plugin state.
        
        Check the active window - if any - and if it is editable, enable the
        menu commands. Otherwise, disable them.
        """
        
        view = self.window.get_active_view()
        self._action_group.set_sensitive(view is not None and view.get_editable())
    
    def _init_translations(self):
        """Initialize localization functions.
        
        First, get the plugin info, then get the custom data storing the gettext
        domain and the locale directory.
        
        Then bind the gettext domain, and set up some some handy functions for
        translating UI strings.
        """
        
        # Get the plugin info
        peas_plugin_info = Peas.Engine.get_default().get_plugin_info(PLUGIN_MODULE_NAME)
        if peas_plugin_info is not None:
            global GETTEXT_PACKAGE
            
            # In the future, when libpeas 1.6+ is ubiquitous:
            #GETTEXT_PACKAGE = peas_plugin_info.get_external_data("gettext-package")
            #localedir       = peas_plugin_info.get_external_data("localedir")
            
            # Sadly, we don't have get_external_data(), so, time to improvise
            ### Begin hack ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            user_data = {}
            try:
                for line in open(os.path.join(os.path.dirname(os.path.realpath(__file__)), PLUGIN_MODULE_NAME + ".plugin")):
                    if line.lstrip().startswith("X-"):
                        try:
                            setting, value = line[2:].split('=', 1)
                            user_data[setting.rstrip()] = value.strip()
                        except ValueError:
                            pass
            except IOError:
                pass
            
            GETTEXT_PACKAGE = "" if "gettext-package" not in user_data else user_data["gettext-package"]
            localedir       = "" if "localedir"       not in user_data else user_data["localedir"]
            ### End hack ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            if GETTEXT_PACKAGE and localedir:
                global _
                global P_
                
                gettext.bindtextdomain(GETTEXT_PACKAGE, localedir)
                _  = lambda s:         gettext.dgettext(GETTEXT_PACKAGE, s)
                P_ = lambda s1, s2, n: gettext.dngettext(GETTEXT_PACKAGE, s1, s2, n)
    
    def _insert_menu(self):
        """Insert the plugin menu items into the gedit edit menu.
        
        First set up the plugins actions. The plugin has only two-and-a-half
        actions. Two of the actions correspond to encoding XML special
        characters in the whole document, and just in the current selection (if
        any). A third "action" - which does nothing - is for the plugin's main
        menu item, and is just used for tranlating the UI.
        
        Once the actions are set up and added to the UI manager, the menu UI
        is added.
        """
        manager = self.window.get_ui_manager()
        self._action_group = Gtk.ActionGroup(name="GeditXmlEncodePluginActions")
        self._action_group.add_actions(
            [("XmlEncode",
                None,
                # TRANSLATORS: Main menu item text
                _("_XML Encode"), None,
                # TRANSLATORS: Main menu item help text
                _("Encode XML special characters as entities"),
                None),
            ("XmlEncodeDocument",
                None,
                # TRANSLATORS: Menu item text to encode whole document
                _("_Document"), None,
                _("Encode XML special characters in document"),
                lambda a, w: self.encode_doc(w)),
            ("XmlEncodeSelection",
                None,
                # TRANSLATORS: Menu item text to encode just selection
                _("_Selection"), None,
                _("Encode XML special characters in selection"),
                lambda a, w: self.encode_sel(w))],
            self.window)
        manager.insert_action_group(self._action_group)
        self._ui_id = manager.add_ui_from_string(menu_ui)
    
    def _remove_menu(self):
        """Remove the plugin's menu from gedit's menu.
        
        After removing the plugin menu itself, also remove the plugin's actions.
        Make sure gedit's UI is refreshed after these changes.
        """
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        manager.ensure_update()
    
    def encode_doc(self, window):
        """Encode XML special characters in the whole document.
        
        This is just a wrapper function around do_encode(), that calls that
        function with start and end parameters that cover the whole document.
        """
        doc = window.get_active_document()
        if doc is not None:
            self.do_encode(doc, 0, doc.get_char_count())
    
    def encode_sel(self, window):
        """Encode XML special characters in the current selection.
        
        This is just a wrapper function around do_encode(), that calls that
        function with start and end parameters that cover the current selection,
        if any. If there is no selection, nothing is done.
        """
        doc = window.get_active_document()
        if doc is not None:
            selection = doc.get_selection_bounds()
            if selection:
                begin_iter, end_iter = doc.get_selection_bounds()
                self.do_encode(doc, begin_iter.get_offset(), end_iter.get_offset())
    
    def do_encode(self, doc, begin, end):
        """Encode XML special characters in the given range.
        
        First the range bounds are checked to make sure they are valid. If the
        start offset is less than zero or greater than the end offset, just
        give up. If the end offset is beyond the end of the document, print a
        warning, then correct it, and continue.
        
        Then iterate through the document, doing all replacements.
        
        The special XML characters and their entity replacements are:
            & => &amp;
            < => &lt;
            > => &gt;
            " => &quot;
            ' => &apos;
        
        Once done, print a message stating how many replacements were done.
        """
        begin_iter, end_iter = doc.get_bounds()
        if begin < 0 or begin > end_iter.get_offset():
            print "(XmlEncode) ERROR: begin offset is invalid:", begin
            return
        elif end > end_iter.get_offset():
            print "(XmlEncode) WARNING: end offset is invalid:", end
            end = end_iter.get_offset()
        
        it = doc.get_iter_at_offset(begin)
        
        # Set a checkpoint for undo operations, so a single undo undoes the
        # whole replacement operation
        doc.begin_user_action()
        
        # Counter to keep track of the number of replacements
        count = 0
        
        while begin != end:
            char = it.get_char()
            
            if char in xml_special_chars:
                # The replacement is done in a very specific order, for good
                # reasons.
                # 
                # First, insert the entity code AFTER the character. Why after?
                # Well, if you insert before, and the character is at the start
                # of the selection, what you insert will appear BEFORE the
                # selection, rather than in it. But if you insert after, and the
                # character is at the end of the selection, what you insert will
                # still be within the selection (because the NEXT character
                # marks the end of the selection).
                # 
                # So now, if the character is in the selection, the inserted
                # entity text is also in the selection, even if the character is
                # the first or last character of the selection. (If it wasn't in
                # the selection, or there was no selection, then it didn't
                # matter, but no harm was done.)
                # 
                # Then you delete the character. If the character was at the
                # start of the selection, the start of the replacement text
                # becomes the new start of the selection. (And the character
                # can't be at the end of the selection, because if it was, the
                # inserted text became the new end of the selection.)
                doc.insert(doc.get_iter_at_offset(begin + len(char)), xml_special_chars[char])
                doc.delete(doc.get_iter_at_offset(begin), doc.get_iter_at_offset(begin + len(char)))
                
                # Now correct the offsets to take the fact that the replacement
                # text may not be the same size as the original text.
                size_change = len(xml_special_chars[char]) - len(char)
                begin += size_change
                end   += size_change
                
                # begin was moved, so we have to reset the iterator to keep up
                it = doc.get_iter_at_offset(begin)
                
                # And, count the replacement
                count += 1
            
            # Advance to the next character
            begin += 1
            it.forward_char();
        
        # Report how many replacements were done, if any
        if 0 == count:
            status_message = _("No XML special characters found")
        else:
            status_message = P_("Found and replaced one XML special character",
                                "Found and replaced %d XML special characters",
                                count)
            try:
                status_message = status_message % count
            except TypeError:
                pass
        
        statusbar = self.window.get_statusbar()
        context_id = statusbar.get_context_id('GeditXmlEncodePlugin')
        #statusbar.flash_message(context_id, status_message)
        
        # flash_message() is currently missing from the Python interface.
        # There is no point in working around this right now - all we needed it
        # for was to display an informative message.
        
        # Mark the end checkpoint
        doc.end_user_action()
