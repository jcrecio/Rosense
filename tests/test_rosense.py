import unittest
import rosense
from monitor import Monitor
from unittest.mock import patch


class RosenseTests(unittest.TestCase):
    mock_kilometer1_sensors_data = ['data1', 'data2']

    def __init__(self, *args, **kwargs):
        super(RosenseTests, self).__init__(*args, **kwargs)
        self.robot = rosense.Rosense()

    @staticmethod
    def mock_kilometer1_sensors():
        return RosenseTests.mock_kilometer1_sensors_data

    def test_get_latest_information_empty(self):
        sensors = self.robot.sensors()

        self.assertEqual(sensors, '{}')

    @patch.object(Monitor, 'get_sensors', mock_kilometer1_sensors)
    def test_get_latest_information_kilometer1_sensor(self):
        self.robot.monitors.append(Monitor(1))
        sensors = self.robot.sensors()

        self.assertEqual(sensors, '{"1": ["data1", "data2"]}')