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

geditpluginexec_PYTHON = xml-encode.py
geditpluginexec_DATA = xml-encode.plugin

EXTRA_DIST = xml-encode.plugin.desktop.in

xml-encode.plugin: xml-encode.plugin.desktop.in Makefile \
	$(INTLTOOL_MERGE) $(wildcard $(top_srcdir)/po/*po); \
	$(INTLTOOL_MERGE) $(top_srcdir)/po $< $@ -d -u -c $(top_builddir)/po/.intltool-merge-cache
	@echo -e "\n# Private plugin data" >>$@
	@echo "X-gettext-package=$(GETTEXT_PACKAGE)" >>$@
	@echo "X-datadir=$(geditplugindatadir)" >>$@
	@echo "X-localedir=$(localedir)" >>$@

# Remove the optimized compiled object (.pyo) because gedit doesn't use it.
# TODO: Maybe better as:
#   @( cd "${geditpluginexecdir}" && rm -f xml-encode.pyo )
install-exec-hook:
	@rm -f $(geditpluginexecdir)/xml-encode.pyo
