# -*- coding: UTF-8 -*-
'''
test_plugins.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
import unittest
import itertools

from core.controllers.w3afCore import w3afCore


class Test_w3afCore_plugins(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_getPluginTypes(self):
        w3af_core = w3afCore()
        plugin_types = w3af_core.plugins.getPluginTypes()
        expected = set( ['grep', 'output', 'mangle', 'audit', 'crawl',
                    'evasion', 'bruteforce', 'auth', 'infrastructure'] )
        self.assertEquals( set(plugin_types), expected )
        
    def test_getPluginListAudit(self):
        w3af_core = w3afCore()
        plugin_list = w3af_core.plugins.getPluginList('audit')

        expected = set(['sqli', 'xss', 'eval'])
        self.assertTrue( set(plugin_list).issuperset(expected) )   

    def test_getPluginListCrawl(self):
        w3af_core = w3afCore()
        plugin_list = w3af_core.plugins.getPluginList('crawl')

        expected = set(['web_spider', 'spider_man'])
        self.assertTrue( set(plugin_list).issuperset(expected) )   

    def test_getPluginInstance(self):
        w3af_core = w3afCore()
        plugin_inst = w3af_core.plugins.getPluginInstance('sqli','audit')

        self.assertEquals( plugin_inst.getName(), 'sqli' )

    def test_getPluginInstanceAll(self):
        w3af_core = w3afCore()
        
        for plugin_type in itertools.chain( w3af_core.plugins.getPluginTypes() , ['attack'] ):
            for plugin_name in w3af_core.plugins.getPluginList(plugin_type):
                plugin_inst = w3af_core.plugins.getPluginInstance(plugin_name, plugin_type)
                self.assertEquals( plugin_inst.getName(), plugin_name )

    def test_setPlugins(self):
        w3af_core = w3afCore()
        enabled = ['sqli']
        w3af_core.plugins.setPlugins(enabled,'audit')
        retrieved = w3af_core.plugins.getEnabledPlugins('audit')
        self.assertEquals( enabled, retrieved )

    def test_getAllEnabledPlugins(self):
        w3af_core = w3afCore()
        enabled_audit = ['sqli', 'xss']
        enabled_grep = ['private_ip']
        w3af_core.plugins.setPlugins(enabled_audit,'audit')
        w3af_core.plugins.setPlugins(enabled_grep,'grep')
        
        all_enabled = w3af_core.plugins.getAllEnabledPlugins()
        
        self.assertEquals( enabled_audit, all_enabled['audit'] )
        self.assertEquals( enabled_grep, all_enabled['grep'] )
    
    def test_plugin_options(self):
        w3af_core = w3afCore()
        plugin_inst = w3af_core.plugins.getPluginInstance('web_spider','crawl')
        options_1 = plugin_inst.getOptions()
        
        w3af_core.plugins.set_plugin_options('crawl', 'web_spider', options_1)
        options_2 = w3af_core.plugins.getPluginOptions('crawl', 'web_spider')
        
        self.assertEquals( options_1, options_2 )
    
    def test_plugin_options_invalid(self):
        w3af_core = w3afCore()
        self.assertRaises(TypeError, w3af_core.plugins.set_plugin_options, 'crawl', 'web_spider', None)
        
    def test_init_plugins(self):
        w3af_core = w3afCore()
        enabled = ['web_spider']
        w3af_core.plugins.setPlugins(enabled,'crawl')
        w3af_core.plugins.init_plugins()
        
        self.assertEquals( len(w3af_core.plugins.plugins['crawl']), 1 )
        
        plugin_inst = w3af_core.plugins.plugins['crawl'][0]
        self.assertEquals( plugin_inst.getName(), 'web_spider' )
                