import argparse
from argparse import Namespace
from unittest.mock import patch

import pytest

from database_tools_script import main, run_parser


@pytest.mark.parametrize('param, expected_result',
                         [(argparse.Namespace(init_db=True, pop_db=None), Namespace(init_db=True, pop_db=None)),
                          (argparse.Namespace(init_db=None, pop_db=True), Namespace(init_db=None, pop_db=True))])
def test_run_parser(param, expected_result):
    with patch('argparse.ArgumentParser.parse_args', return_value=param):
        assert run_parser() == expected_result


@patch('database_tools_script.argparse.ArgumentParser.parse_args', return_value=Namespace(init_db=None, pop_db=None))
def test_run_parser_empty(mock_run_parser):
    with pytest.raises(ValueError):
        assert ValueError('Please select --init_db, --pop_db') == run_parser()
    mock_run_parser.assert_called_once()


@pytest.mark.parametrize('param, expected_result',
                         [(Namespace(init_db=True, pop_db=None), 'create_tables'),
                          (Namespace(init_db=None, pop_db=True), 'populate')])
@patch('database_tools_script.PopulateDB')
@patch('database_tools_script.DataGenerator')
def test_main(mock_data_generator, mock_populate_db, capsys, param, expected_result):
    mock_data_generator.groups.return_value = 'Fake_group'
    mock_data_generator.students.return_value = 'Fake_Student'
    mock_populate_db.create_tables.return_value = 'Fake_table'
    mock_populate_db.pop_groups.return_value = ['py', 'fl']
    mock_populate_db.pop_students.return_value = 99
    with patch('database_tools_script.run_parser', return_value=param):
        main()
        if expected_result == 'create_tables':
            mock_populate_db.create_tables.assert_called()
        if expected_result == 'populate':
            mock_populate_db.pop_groups.assert_called()
            mock_populate_db.pop_students.assert_called()
            mock_data_generator.groups.assert_called()
            mock_data_generator.students.assert_called()
