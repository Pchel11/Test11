from utils import normilize_path


def test_normilize_path():

    for i in range(4):
            t = test_data[i]
                e = expected_data[i]
                    g = normalize_path(t)
                        assert e == g, f"mismatch: for normalize_path ('{t}') expected '{e}', got '{g}'"
    for :
        got = normalize_path(path)
        assert got == expected, f"path '{path}' normalized to '{got}', while '{expected}' expected"
