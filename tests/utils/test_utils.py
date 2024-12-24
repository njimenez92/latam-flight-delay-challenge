import unittest
import pandas as pd
from utils.utils import get_period_day, is_high_season, get_min_diff, delay


class TestUtils(unittest.TestCase):

    def test_get_period_day_valid(self):
        """Test get_period_day with valid inputs."""
        self.assertEqual(get_period_day('2024-06-01 06:30:00'), 'mañana')
        self.assertEqual(get_period_day('2024-06-01 13:30:00'), 'tarde')
        self.assertEqual(get_period_day('2024-06-01 20:30:00'), 'noche')
        self.assertEqual(get_period_day('2024-06-01 03:30:00'), 'noche')
    
    def test_get_period_day_invalid(self):
        """Test get_period_day with invalid inputs."""
        self.assertEqual(get_period_day('invalid-date'), 'error')
        self.assertEqual(get_period_day('2024-06-01'), 'error')
    
    def test_get_period_day_with_timestamp(self):
        """Test get_period_day with pandas Timestamp."""
        timestamp = pd.Timestamp('2024-06-01 07:30:00')
        self.assertEqual(get_period_day(timestamp), 'mañana')

    def test_is_high_season_valid(self):
        """Test is_high_season with valid dates."""
        self.assertEqual(is_high_season('2024-12-20 00:00:00'), 1)  # High season
        self.assertEqual(is_high_season('2024-01-15 00:00:00'), 1)  # High season
        self.assertEqual(is_high_season('2024-06-15 00:00:00'), 0)  # Not high season
    
    def test_is_high_season_invalid(self):
        """Test is_high_season with invalid dates."""
        self.assertEqual(is_high_season('invalid-date'), 0)
        self.assertEqual(is_high_season('2024-06-01'), 0)

    def test_get_min_diff_valid(self):
        """Test get_min_diff with valid datetime strings."""
        row = pd.Series({
            'Fecha-O': '2024-06-01 14:30:00',
            'Fecha-I': '2024-06-01 14:00:00'
        })
        self.assertEqual(get_min_diff(row), 30.0)

    def test_get_min_diff_invalid_format(self):
        """Test get_min_diff with invalid datetime strings."""
        row = pd.Series({
            'Fecha-O': 'invalid-date',
            'Fecha-I': '2024-06-01 14:00:00'
        })
        self.assertEqual(get_min_diff(row), 0.0)

    def test_get_min_diff_missing_column(self):
        """Test get_min_diff with missing columns."""
        row = pd.Series({
            'Fecha-O': '2024-06-01 14:30:00'
        })
        self.assertEqual(get_min_diff(row), 0.0)

    def test_delay_valid(self):
        """Test delay with valid inputs."""
        self.assertEqual(delay(20, threshold=15), 1)
        self.assertEqual(delay(10, threshold=15), 0)

    def test_delay_edge_cases(self):
        """Test delay with edge case inputs."""
        self.assertEqual(delay(15, threshold=15), 0)
        self.assertEqual(delay(-5, threshold=15), 0)
        self.assertEqual(delay(0, threshold=15), 0)

    def test_delay_invalid_inputs(self):
        """Test delay with invalid inputs."""
        self.assertEqual(delay('invalid', threshold=15), 0)
        self.assertEqual(delay(None, threshold=15), 0)


if __name__ == '__main__':
    unittest.main()
