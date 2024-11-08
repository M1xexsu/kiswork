from main import *
import unittest
from unittest.mock import MagicMock, patch
from io import StringIO


class TestSwitchCommand(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_ls(self, mock_stdout):
        vfs = MagicMock()
        vfs.listdir.return_value = ['file1.txt', 'file2.txt']

        switchcommand("ls", vfs, None, None)

        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "['file1.txt', 'file2.txt']")

    @patch('sys.stdout', new_callable=StringIO)
    def test_cd(self, mock_stdout):
        vfs = MagicMock()

        switchcommand("cd /home/user", vfs, None, None)
        vfs.jumpto.assert_called_once_with('/home/user')

        switchcommand("cd", vfs, None, None)
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "zsh: cd: missing argument")

    @patch('sys.stdout', new_callable=StringIO)
    def test_rmdir(self, mock_stdout):
        vfs = MagicMock()

        switchcommand("rmdir /home/user/dir", vfs, None, None)
        vfs.rmdir.assert_called_once_with('/home/user/dir')

        switchcommand("rmdir", vfs, None, None)
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "zsh: rmdir: missing argument")

    @patch('sys.stdout', new_callable=StringIO)
    def test_uname(self, mock_stdout):

        switchcommand("uname", None, None, None)
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Darwin")

    @patch('sys.stdout', new_callable=StringIO)
    def test_du(self, mock_stdout):

        vfs = MagicMock()
        tar = MagicMock()

        switchcommand("du", vfs, tar, None)
        vfs.du.assert_called_once_with(tar)

    @patch('sys.stdout', new_callable=StringIO)
    def test_exit(self, mock_stdout):
        user = "test_user"

        with self.assertRaises(SystemExit):
            switchcommand('exit', None, None, user)

        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, f"Connection to {user} closed.")

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_command(self, mock_stdout):
        vfs = MagicMock()
        switchcommand("unknowncommand", vfs, None, None)
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "zsh: command not found: unknowncommand")

    @patch('sys.stdout', new_callable=StringIO)
    def test_exception_handling(self, mock_stdout):
        vfs = MagicMock()
        vfs.listdir.side_effect = Exception("Test exception")

        switchcommand("ls", vfs, None, None)
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Ошибка выполнения команды: Test exception")


if __name__ == '__main__':
    unittest.main()
