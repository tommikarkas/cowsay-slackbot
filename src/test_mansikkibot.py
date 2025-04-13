"""Test module for mansikkibot.py"""

import unittest
from unittest.mock import MagicMock, patch

from src.mansikkibot import MansikkiBot


class TestMansikkibot(unittest.TestCase):
    """Test cases for Mansikkibot class"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        cls.bot_name = "test_bot"
        cls.bot_token = "test_token"
        cls.bot_id = "mansikkibot"
        
        # Create the bot and mock its ID
        cls.bot = MansikkiBot(cls.bot_name, cls.bot_token)
        cls.bot.bot_id = cls.bot_id
        cls.bot.say = MagicMock()  # Mock the say method

    def setUp(self):
        """Reset the say mock before each test"""
        self.bot.say.reset_mock()

    def test_handle_message_direct_message(self):
        """Test handling direct messages"""
        # Create a mock message
        message = MagicMock()
        message.text = "!cowsay Hello World"
        message.is_direct.return_value = True
        message.sent_at.return_value = False
        message.channel = "test_channel"

        # Test cowsay command
        self.bot.handle_message(message)
        self.bot.say.assert_called_once()
        self.assertTrue("Hello World" in self.bot.say.call_args[0][1])

    def test_handle_message_mention(self):
        """Test handling @mentions"""
        # Create a mock message
        message = MagicMock()
        message.text = f"<@{self.bot.bot_id}> !cowsay Hello World"
        message.is_direct.return_value = False
        message.sent_at.return_value = True
        message.channel = "test_channel"

        # Test cowsay command with mention
        self.bot.handle_message(message)
        self.bot.say.assert_called_once()
        self.assertTrue("Hello World" in self.bot.say.call_args[0][1])

    def test_handle_message_fortune(self):
        """Test fortune command"""
        message = MagicMock()
        message.text = "!cowsay !fortune"  # Both !cowsay and !fortune are needed
        message.is_direct.return_value = True
        message.sent_at.return_value = False
        message.channel = "test_channel"

        # Mock the fortune function at the correct import path
        with patch("src.fortune_action.fortune") as mock_fortune:
            mock_fortune.return_value = "Test fortune message"
            self.bot.handle_message(message)
            self.bot.say.assert_called_once()
            
            self.assertTrue("Test fortune message" in self.bot.say.call_args[0][1])

    def test_handle_message_routahe(self):
        """Test routahe command"""
        message = MagicMock()
        message.text = '!cowsay !routahe "From Address" "To Address"'  # Both !cowsay and !routahe are needed
        message.is_direct.return_value = True
        message.sent_at.return_value = False
        message.channel = "test_channel"

        # Mock the routahe function at the correct import path
        with patch("src.routahe_action.routahe") as mock_routahe:
            mock_routahe.return_value = "Test route"
            self.bot.handle_message(message)
            self.bot.say.assert_called_once()
            self.assertTrue("Test route" in self.bot.say.call_args[0][1])

    def test_handle_message_invalid_command(self):
        """Test handling invalid commands"""
        message = MagicMock()
        message.text = "!invalidcommand"
        message.is_direct.return_value = True
        message.sent_at.return_value = False
        message.channel = "test_channel"

        # Should not raise an exception
        self.bot.handle_message(message)
        self.bot.say.assert_not_called()

    def test_handle_message_empty(self):
        """Test handling empty messages"""
        message = MagicMock()
        message.text = ""
        message.is_direct.return_value = True
        message.sent_at.return_value = False
        message.channel = "test_channel"

        # Should not raise an exception
        self.bot.handle_message(message)
        self.bot.say.assert_not_called()


if __name__ == "__main__":
    unittest.main() 