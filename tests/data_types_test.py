from modules.data_types import MockDataType


def test_mock_data_type():
    # Arrange
    mock_id = "test-id"
    mock_name = "Test Name"

    # Act
    mock_data = MockDataType(id=mock_id, name=mock_name)

    # Assert
    assert mock_data.id == mock_id
    assert mock_data.name == mock_name
