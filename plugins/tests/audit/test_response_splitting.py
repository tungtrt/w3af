'''
test_response_splitting.py

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

from ..helper import PluginTest, PluginConfig


class TestResponseSplitting(PluginTest):
    
    direct_url = 'http://moth/w3af/audit/response_splitting/response_splitting.php'
    error_url = 'http://moth/w3af/audit/response_splitting/response_splitting_err.php' 
    
    _run_configs = {
        'cfg_direct': {
            'target': direct_url + '?header=None',
            'plugins': {
                 'audit': (PluginConfig('response_splitting'),),
                 }
            },

        'cfg_error': {
            'target': error_url + '?header=None',
            'plugins': {
                 'audit': (PluginConfig('response_splitting'),),
                 }
            }
        }
    
    def test_found_direct(self):
        cfg = self._run_configs['cfg_direct']
        self._scan(cfg['target'], cfg['plugins'])
        vulns = self.kb.getData('response_splitting', 'response_splitting')
        self.assertEquals(1, len(vulns), vulns)
        
        # Now some tests around specific details of the found vuln
        vuln = vulns[0]
        self.assertEquals('Response splitting vulnerability', vuln.getName())
        self.assertEquals(self.direct_url, str(vuln.getURL()))
        self.assertEquals('header', vuln.getVar())
    
    def test_found_error(self):
        cfg = self._run_configs['cfg_error']
        self._scan(cfg['target'], cfg['plugins'])
        vulns = self.kb.getData('response_splitting', 'response_splitting')
        self.assertEquals(1, len(vulns), vulns)
        
        # Now some tests around specific details of the found vuln
        vuln = vulns[0]
        self.assertEquals('Parameter modifies headers', vuln.getName())
        self.assertEquals(self.error_url, str(vuln.getURL()))
        self.assertEquals('header', vuln.getVar())
                
