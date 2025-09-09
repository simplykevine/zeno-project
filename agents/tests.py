from django.test import TestCase
from django.db import IntegrityError, transaction
from .models import Agent, Tool

class AgentModelTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(
            agent_name="Test Agent",
            description="A test agent for unit testing."
        )

    def test_agent_creation(self):
        self.assertEqual(self.agent.agent_name, "Test Agent")
        self.assertEqual(self.agent.description, "A test agent for unit testing.")
        self.assertIsInstance(self.agent, Agent)

    def test_agent_str_representation(self):
        self.assertEqual(str(self.agent), "Test Agent")

    def test_agent_id_auto_increment(self):
        another_agent = Agent.objects.create(
            agent_name="Second Agent",
            description="Another test agent."
        )
        self.assertNotEqual(self.agent.agent_id, another_agent.agent_id)
        self.assertTrue(another_agent.agent_id > self.agent.agent_id)

    def test_agent_name_uniqueness(self):
        """Test that agent_name must be unique."""
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Agent.objects.create(
                    agent_name="Test Agent", 
                    description="Should fail"
                )

class ToolModelTest(TestCase):

    def setUp(self):
        self.var_tool_data = {
            'tool_name': 'VAR the Economic Model',
            'tool_description': (
                'A Vector Autoregression (VAR) model used for forecasting '
                'interdependent economic time series such as GDP, inflation, and unemployment.'
            ),
            'meta_data': {
                'parameters': {
                    'lags': 4,
                    'variables': ['GDP', 'Inflation', 'UnemploymentRate'],
                    'frequency': 'quarterly',
                    'estimation_method': 'OLS'
                },
                'required_data': {
                    'source': 'FRED',
                    'min_observations': 40
                },
                'output': {
                    'forecast_periods': 8,
                    'confidence_interval': 0.95
                }
            }
        }
        self.var_tool = Tool.objects.create(**self.var_tool_data)

    def test_var_tool_creation(self):
        """Test that the VAR economic model tool is created correctly."""
        tool = self.var_tool
        self.assertIsInstance(tool, Tool)
        self.assertEqual(tool.tool_name, 'VAR the Economic Model')
        self.assertIn('Vector Autoregression', tool.tool_description)
        self.assertEqual(tool.meta_data['parameters']['lags'], 4)
        self.assertIn('GDP', tool.meta_data['parameters']['variables'])
        self.assertEqual(tool.meta_data['output']['confidence_interval'], 0.95)

    def test_var_tool_str_method(self):
        """Test that __str__ returns the tool name."""
        self.assertEqual(str(self.var_tool), 'VAR the Economic Model')

    def test_tool_id_autoincrements(self):
        """Test that tool_id is assigned automatically and increments."""
        second_tool = Tool.objects.create(
            tool_name='ARIMA Forecast',
            tool_description='Forecasts single time series using ARIMA.',
            meta_data={'order': [1, 1, 1]}
        )
        self.assertEqual(second_tool.tool_id, self.var_tool.tool_id + 1)

    def test_meta_data_json_structure(self):
        """Test that meta_data retains its full nested JSON structure."""
        saved_tool = Tool.objects.get(tool_id=self.var_tool.tool_id)
        self.assertEqual(saved_tool.meta_data, self.var_tool_data['meta_data'])
        self.assertIsInstance(saved_tool.meta_data, dict)
        self.assertIsInstance(saved_tool.meta_data['parameters'], dict)

