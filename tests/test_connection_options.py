import unittest
from rxpymqtt import ConnectionOptions, ConnectionCredentials

class TestConnectionOptions(unittest.TestCase):
  
  def test_constructable(self):
    options = ConnectionOptions('localhost', 1883)
    self.assertIsInstance(options, object)
  
  def test_stores_attributes(self):
    options = ConnectionOptions('localhost', 41883)
    self.assertEqual(options.host, 'localhost')
    self.assertEqual(options.port, 41883)
  
  def test_constructable_with_creds(self):
    credentials = ConnectionCredentials('username', 'password')
    options = ConnectionOptions('localhost', credentials=credentials)
    self.assertIsInstance(options, object)
  
  def test_stores_creds(self):
    credentials = ConnectionCredentials('username', 'password')
    options = ConnectionOptions('localhost', credentials=credentials)
    self.assertEqual(options.credentials, credentials)
