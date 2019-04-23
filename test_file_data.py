import os
import pytest
import mock
import shutil

import file_data as store_ops

@pytest.mark.run(order=1)
def test_local_rename():
    old_file_path = os.path.abspath('test_file.txt')
    new_file_path = os.path.abspath('new_test_file.txt')
    with open(old_file_path, 'w') as fb:
        fb.write('test')
    test_result = store_ops.rename_doc('local', old_file_path, new_file_path)
    assert test_result == "file successfully renamed"
    os.remove(new_file_path)

@pytest.mark.run(order=2)
def test_delete_file_local():
    file_path = os.path.abspath('test_file.txt')
    with open(file_path, 'w') as fb:
        fb.write('test')
    test_result = store_ops.delete('local', file_path)
    assert test_result == "file successfully deleted"

@pytest.mark.run(order=3)
def test_delete_folder_local():
    folder_path = os.path.abspath('test_folder_test')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    test_result = store_ops.delete('local', folder_path)
    assert test_result == "folder successfully deleted"

@pytest.mark.run(order=4)
def test_file_attributes_local():
    file_path = os.path.abspath('test_file.txt')
    with open(file_path, 'w') as fb:
        fb.write('test')
    last_modified = os.path.getmtime(file_path)
    size = os.path.getsize(file_path)
    test_dict = store_ops.get_attributes('local', file_path)
    assert test_dict['last_modified'] == last_modified
    assert test_dict['size'] == size
    os.remove(file_path)

@pytest.mark.run(order=5)
@mock.patch('leucine_assign.file_data.getFolderSize')
def test_folder_attributes_local(mocked_folder_size):
    file_path = os.path.abspath('test_size_and_modified/test_file.txt')
    folder_path = os.path.abspath('test_size_and_modified')
    mocked_folder_size.return_value = 45
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(file_path, 'w') as fb:
        fb.write('test')
    last_modified = os.path.getmtime(folder_path)
    test_dict = store_ops.get_attributes('local', folder_path)
    assert test_dict['last_modified'] == last_modified
    assert test_dict['size'] == 45
    shutil.rmtree(folder_path)

@pytest.mark.run(order=6)
def test_folder_size():
    file_path = os.path.abspath('test_size_and_modified/test_file.txt')
    folder_path = os.path.abspath('test_size_and_modified')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(file_path, 'w') as fb:
        fb.write('test')
    folder_size = store_ops.getFolderSize(folder_path)
    assert folder_size > 0
    shutil.rmtree(folder_path)

@pytest.mark.run(order=7)
def test_get_doc_data():
    file_path = os.path.abspath('test_file.txt')
    with open(file_path, 'w') as fb:
        fb.write('test')
    test_data = store_ops.get_doc_data('local', file_path)
    assert test_data == 'test'
    os.remove(file_path)

