from unittest.mock import patch

from web_courses.utils import DataGenerator, NewStudent


@patch('web_courses.utils.random.choices', return_value=['Y', 'U'])
@patch('web_courses.utils.random.randint', return_value=18)
def test_group_generator(mock_randint, mock_choices):
    assert 'YU-18' in DataGenerator.groups()
    mock_choices.assert_called()
    mock_randint.assert_called()


@patch('web_courses.utils.get_first_name', return_value='First_Name')
@patch('web_courses.utils.get_last_name', return_value='Last_Name')
@patch('web_courses.utils.random.randint', return_value=18)
def test_stud_generator(mock_randint, mock_get_last_name, mock_get_first_name):
    assert NewStudent(name='First_Name',
                      last_name='Last_Name',
                      id_group=18,
                      course='Python') in DataGenerator.students()
    mock_get_last_name.assert_called()
    mock_get_first_name.assert_called()
    mock_randint.assert_called()
