#!/usr/bin/python

import unittest
import sys
from os import system
from subprocess import Popen
from time import sleep
import config
from support import *
from tcpdump import TcpDump

class TestSupport:
    br=config.br
    mote=config.mote
    platform=config.platform
    tcpdump=TcpDump()
    ip_6lbr=None
    ip_mote="aaaa::" + config.lladdr_mote

    def setUp(self):
        self.platform.setUp()
        self.br.setUp()
        self.mote.setUp()

    def tearDown(self):
        self.mote.tearDown()
        self.br.tearDown()
        self.platform.tearDown()

    def set_mode(self, mode, nvm_file):
        return self.br.set_mode(mode, nvm_file)

    def start_ra(self, itf):
        return self.platform.start_ra(itf)

    def stop_ra(self):
        return self.platform.stop_ra()

    def start_6lbr(self, log):
        return self.br.start_6lbr(log)

    def stop_6lbr(self):
        return self.br.stop_6lbr()

    def start_mote(self, load):
        return self.mote.start_mote(load)

    def stop_mote(self):
        return self.mote.stop_mote()

    def ping(self, target):
        return self.platform.ping(target)

    def wait_mote_in_6lbr(self, count):
        return True

    def wait_ping(self, count, target):
        for n in range(count):
            if (self.ping(target)):
                return True
        return False

    def ping_6lbr(self):
        return self.ping( self.ip_6lbr )

    def wait_ping_6lbr(self, count):
        return self.wait_ping( count, self.ip_6lbr )

    def ping_mote(self):
        return self.ping( self.ip_mote )

    def wait_ping_mote(self, count):
        return self.wait_ping( count, self.ip_mote )

class TestScenarios:
    support=TestSupport()

    def test_S0(self):
        """
        Check 6LBR start-up anbd connectivity
        """
        self.assertTrue(self.support.start_6lbr('test_S0.log'), "Could not start 6LBR")
        self.set_up_network()
        self.assertTrue(self.support.wait_ping_6lbr(40), "6LBR is not responding")
        self.tear_down_network()
        self.assertTrue(self.support.stop_6lbr(), "Could not stop 6LBR")

    @unittest.skip("test")
    def test_S1(self):
        """
        Ping from the computer to the mote when the PC knows the BR but the BR does not know the
        mote.
        """
        self.assertTrue(self.support.start_6lbr('test_S1.log'), "Could not start 6LBR")
        self.assertTrue(self.support.set_up_network(), "Could not set up network")
        self.assertTrue(self.support.start_mote('default'), "Could not start up mote")
        self.assertTrue(self.support.wait_mote_in_6lbr(30), "Mote not detected")
        self.assertTrue(self.support.wait_ping_mote(60), "Mote is not responding")
        self.assertTrue(self.support.stop_mote(), "Could not stop mote")
        self.assertTrue(self.support.tear_down_network(), "Could not tear down network")
        self.assertTrue(self.support.stop_6lbr(), "Could not stop 6LBR")

    @unittest.skip("test")
    def test_S2(self):
        """
        Ping from the computer to the mote when the PC does not know the BR and the BR knows
        the mote.
        """
        self.assertTrue(self.support.start_6lbr('test_S2.log'), "Could not start 6LBR")
        self.assertTrue(self.support.start_mote('default'), "Could not start up mote")
        self.assertTrue(self.support.wait_mote_in_6lbr(30), "Mote not detected")
        self.assertTrue(self.support.set_up_network(), "Could not set up network")
        self.assertTrue(self.support.wait_ping_mote(60), "Mote is not responding")
        self.assertTrue(self.support.stop_mote(), "Could not stop mote")
        self.assertTrue(self.support.tear_down_network(), "Could not tear down network")
        self.assertTrue(self.support.stop_6lbr(), "Could not stop 6LBR")

    @unittest.skip("test")
    def test_S3(self):
        """
        Ping from the computer to the mote when everyone is known but the mote has been disconnected.
        """
        self.assertTrue(self.support.start_6lbr('test_S3.log'), "Could not start 6LBR")
        self.assertTrue(self.support.start_mote('default'), "Could not start up mote")
        self.assertTrue(self.support.wait_mote_in_6lbr(30), "Mote not detected")
        self.assertTrue(self.support.set_up_network(), "Could not set up network")
        self.assertTrue(self.support.wait_ping_mote(60), "Mote is not responding")
        self.assertTrue(self.support.stop_mote(), "Could not stop mote")
        self.assertFalse(self.support.wait_ping_mote(10), "Mote is still responding")
        self.assertTrue(self.support.tear_down_network(), "Could not tear down network")
        self.assertTrue(self.support.stop_6lbr(), "Could not stop 6LBR")

    @unittest.skip("test")
    def test_S4(self):
        """
        Starting from a stable RPL topology, restart the border router and observe how it attaches
        to the RPL DODAG.
        """
        self.assertTrue(self.support.start_6lbr('test_S4_a.log'), "Could not start 6LBR")
        self.assertTrue(self.support.start_mote('default'), "Could not start up mote")
        self.assertTrue(self.support.wait_mote_in_6lbr(30), "Mote not detected")
        self.assertTrue(self.support.set_up_network(), "Could not set up network")
        self.assertTrue(self.support.wait_ping_mote(60), "Mote is not responding")
        self.assertTrue(self.support.tear_down_network(), "Could not tear down network")
        self.assertTrue(self.support.stop_6lbr(), "Could not stop 6LBR")
        self.assertTrue(self.support.start_6lbr('test_S4_b.log'), "Could not start 6LBR")
        self.assertTrue(self.support.set_up_network(), "Could not set up network")
        self.assertTrue(self.support.wait_ping_mote(60), "Mote is not responding")
        self.assertTrue(self.support.stop_mote(), "Could not stop mote")
        self.assertTrue(self.support.tear_down_network(), "Could not tear down network")
        self.assertTrue(self.support.stop_6lbr(), "Could not stop 6LBR")

    @unittest.skip("test")
    def test_S5(self):
        """
        Wait for a DAD between the computer and the BR, then disconnect and reconnect the com-
        puter and observe the reaction of the BR to a computer's DAD.
        """
        pass

    @unittest.skip("test")
    def test_S6(self):
        """
        Observe the NUDs between the computer and the BR.
        """
        pass

    @unittest.skip("test")
    def test_S7(self):
        """
        Test the Auconfiguration process of the BR in bridge mode and observe its ability to take a
        router prefix (by using the computer as a router), and deal with new RA once configured.
        """
        pass

    @unittest.skip("test")
    def test_S8(self):
        """
        Observe the propagation of the RIO in the WSN side (when supported in the WPAN).
        """
        pass

    @unittest.skip("test")
    def test_S9(self):
        """
        Test the using of the default router.
        """
        pass

@unittest.skip("test")
class SmartBridgeManual(unittest.TestCase,TestScenarios):
    def setUp(self):
        self.support=TestSupport()
        self.support.ip_6lbr='aaaa::' + config.lladdr_6lbr
        self.support.setUp()
        self.support.set_mode('SMART-BRIDGE', 'manual.dat')

    def tearDown(self):
        self.tear_down_network()
        self.support.tearDown()

    def set_up_network(self):
        self.assertTrue( self.support.platform.configure_if(self.support.br.itf, "aaaa::200"), "")

    def tear_down_network(self):
        self.assertTrue( self.support.platform.unconfigure_if(self.support.br.itf), "")

@unittest.skip("test")
class SmartBridgeAuto(unittest.TestCase,TestScenarios):
    def setUp(self):
        self.support=TestSupport()
        self.support.ip_6lbr='aaaa::' + config.lladdr_6lbr
        self.support.setUp()
        self.support.set_mode('SMART-BRIDGE', 'auto.dat')

    def tearDown(self):
        self.support.tearDown()

    def set_up_network(self):
        #self.support.platform.accept_ra(self.support.br.itf)
        self.assertTrue( self.support.platform.configure_if(self.support.br.itf, "aaaa::200"), "")
        self.assertTrue( self.support.start_ra(self.support.br.itf), "")

    def tear_down_network(self):
        self.assertTrue( self.support.stop_ra(), "")

#@unittest.skip("test")
class Router(unittest.TestCase,TestScenarios):
    def setUp(self):
        self.support=TestSupport()
        self.support.ip_6lbr='bbbb::100'
        self.support.setUp()
        self.support.set_mode('ROUTER', 'router.dat')

    def tearDown(self):
        self.support.tearDown()
        
    def set_up_network(self):
        self.assertTrue(self.support.platform.accept_ra(self.support.br.itf), "Could not enable RA configuration support")
        if self.support.platform.support_rio():
            self.assertTrue(self.support.platform.accept_rio(self.support.br.itf), "Could not enable RIO support")
        self.assertTrue(self.support.tcpdump.expect_ra(self.support.br.itf, 30), "")
        self.assertTrue(self.support.platform.check_prefix(self.support.br.itf, 'bbbb::'), "Interface not configured")
        if not self.support.platform.support_rio():
            self.assertTrue(self.support.platform.add_route("aaaa::", gw=self.support.ip_6lbr), "Could not add route")

    def tear_down_network(self):
        if not self.support.platform.support_rio():
            self.assertTrue(self.support.platform.rm_route("aaaa::", gw=self.support.ip_6lbr), "Could not remove route")

@unittest.skip("test")
class RouterNoRa(unittest.TestCase,TestScenarios):
    def setUp(self):
        self.support=TestSupport()
        self.support.ip_6lbr='bbbb::100'
        self.support.setUp()
        self.support.set_mode('ROUTER', 'router_no_ra.dat')

    def tearDown(self):
        self.support.tearDown()

    def set_up_network(self):
        self.assertTrue( self.support.platform.configure_if(self.support.br.itf, "bbbb::200"), "")
        self.assertTrue( self.support.platform.add_route("aaaa::", gw=self.support.ip_6lbr), "")

    def tear_down_network(self):
        self.assertTrue( self.support.platform.rm_route("aaaa::", gw=self.support.ip_6lbr), "")
        self.assertTrue( self.support.platform.unconfigure_if(self.support.br.itf), "")

if __name__ == '__main__':
    unittest.main()