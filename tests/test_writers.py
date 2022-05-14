from ingestion.writers import FileWriter, InvalidDataTypeForIngestionException
import pytest
from datetime import datetime
import json


@pytest.mark.parametrize("folder_name, expected",
                [( "api_folder_name", str('api_folder_name') + f'/{ datetime.strftime( datetime.now(), "%Y-%m-%d-%H_%M" ) }.json'),
                ("", f'/{ datetime.strftime( datetime.now(), "%Y-%m-%d-%H_%M" ) }.json')])
def test_build_address(folder_name, expected):
    writer = FileWriter(folder_name)
    actual = writer.address
    assert actual == expected



dummy_data = {f'dummy_key_{i}': f'dummy_item_{i}' for i in range(5)}

@pytest.mark.parametrize("data, expected",
                [( dummy_data, json.dumps({'data':[dummy_data]}, indent = 6, sort_keys = True)),
                ([dummy_data,dummy_data,dummy_data], json.dumps({'data':[dummy_data,dummy_data,dummy_data]}, indent = 6, sort_keys = True)) ,
                ])
def test_write_file(tmpdir, data, expected):
    file = tmpdir.mkdir("sub").join('textfile.txt')
    writer = FileWriter()
    writer.address = file.strpath
    writer.write_file(data)
    actual = file.read()
    assert actual == expected


def test_write_element():
    with pytest.raises(InvalidDataTypeForIngestionException):
        writer = FileWriter('folder_name')
        writer.write_file('Dtype string should cause an Exception')