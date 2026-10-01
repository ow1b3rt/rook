from rook.schemas import Evidence


def test_nepali_text_and_unknown_location_survive_roundtrip():
    record = Evidence(
        platform="manual",
        external_id="1",
        kind="post",
        url="https://example.com/post/1",
        text_original="मूल्य कति हो?",
        extractor="manual",
    )
    restored = Evidence.model_validate_json(record.model_dump_json())
    assert restored.text_original == "मूल्य कति हो?"
    assert restored.location is None
    assert restored.collected_at.tzinfo is not None
