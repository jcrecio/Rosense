import unittest
import rosense
from monitor import Monitor
from unittest.mock import patch, create_autospec, Mock


class RosenseTests(unittest.TestCase):
    mock_kilometer1_sensors_data = []

    def __init__(self, *args, **kwargs):
        super(RosenseTests, self).__init__(*args, **kwargs)

    @staticmethod
    def mock_kilometer1_sensors():
        return RosenseTests.mock_kilometer1_sensors_data

    def setUp(self):
        RosenseTests.mock_kilometer1_sensors_data = ['data1', 'data2']
        self.robot = rosense.Rosense()

    def service_called(sensors):
        None

    def test_get_latest_information_empty(self):
        sensors = self.robot.sensors()

        self.assertEqual(sensors, '{}')

    @patch.object(Monitor, 'get_sensors', mock_kilometer1_sensors)
    def test_get_latest_information_kilometer1_sensor(self):
        self.robot.monitors.append(Monitor(1))
        sensors = self.robot.sensors()

        self.assertEqual(sensors, '{"1": ["data1", "data2"]}')

    @patch.object(Monitor, 'sensors', mock_kilometer1_sensors)
    @patch.object(Monitor, 'connect', side_effect=service_called)
    def test_connect_monitors(self, service_called):
        kms = [1, 2, 3]
        self.robot.add_monitors(kms)

        self.robot.connect_monitors()

        self.assertEqual(service_called.called, True)



