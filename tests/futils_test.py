import unittest
from unittest import TestCase
from unittest.mock import Mock
from futils import FileManager

class TestFileManager(TestCase):
    def setUp(self):
        self.file_manager = FileManager(sel=Mock(), fs=Mock(), ui=Mock())
        self.file_manager.sel.get_and_reset.return_value = ["file1", "file2"]

    def test_copy_files_success(self):
        self.file_manager.fs.copy.side_effect = [None, None]
        result = self.file_manager.copy_files("destination")
        self.assertEqual(result, 2)
        self.file_manager.fs.copy.assert_any_call("file1", "destination")
        self.file_manager.fs.copy.assert_any_call("file2", "destination")

    def test_copy_files_partial_failure(self):
        self.file_manager.fs.copy.side_effect = [None, Exception("Error")]
        result = self.file_manager.copy_files("destination")
        self.assertEqual(result, 0)
        self.file_manager.fs.copy.assert_any_call("file1", "destination")
        self.file_manager.fs.copy.assert_any_call("file2", "destination")
        self.file_manager.ui.error.assert_called_once_with("Copy: Error")

    def test_copy_files_no_files_selected(self):
        self.file_manager.sel.get_and_reset.return_value = []
        result = self.file_manager.copy_files("destination")
        self.assertEqual(result, 0)
        self.file_manager.fs.copy.assert_not_called()
        self.file_manager.ui.error.assert_not_called()
        
    def test_move_files_success(self):
        self.file_manager.fs.move.side_effect = [None, None]
        result = self.file_manager.move_files("destination")
        self.assertEqual(result, 2)
        self.file_manager.fs.move.assert_any_call("file1", "destination")
        self.file_manager.fs.move.assert_any_call("file2", "destination")
        
    def test_move_files_partial_failure(self):
        self.file_manager.fs.move.side_effect = [None, Exception("Error")]
        result = self.file_manager.move_files("destination")
        self.assertEqual(result, 0)
        self.file_manager.fs.move.assert_any_call("file1", "destination")
        self.file_manager.fs.move.assert_any_call("file2", "destination")
        self.file_manager.ui.error.assert_called_once_with("Move: Error")
        
    def test_move_files_no_files_selected(self):
        self.file_manager.sel.get_and_reset.return_value = []
        result = self.file_manager.move_files("destination")
        self.assertEqual(result, 0)
        self.file_manager.fs.move.assert_not_called()
        self.file_manager.ui.error.assert_not_called()
        
    def test_delete_files_success(self):
        self.file_manager.fs.delete.side_effect = [None, None]
        result = self.file_manager.delete_files()
        self.assertEqual(result, 2)
        self.file_manager.fs.delete.assert_any_call("file1")
        self.file_manager.fs.delete.assert_any_call("file2")
        
    def test_delete_files_partial_failure(self):
        self.file_manager.fs.delete.side_effect = [None, Exception("Error")]
        result = self.file_manager.delete_files()
        self.assertEqual(result, 0)
        self.file_manager.fs.delete.assert_any_call("file1")
        self.file_manager.fs.delete.assert_any_call("file2")
        self.file_manager.ui.error.assert_called_once_with("Delete: Error")
        
    def test_delete_files_no_files_selected(self):
        self.file_manager.sel.get_and_reset.return_value = []
        result = self.file_manager.delete_files()
        self.assertEqual(result, 0)
        self.file_manager.fs.delete.assert_not_called()
        self.file_manager.ui.error.assert_not_called()

if __name__ == '__main__':
    unittest.main()
