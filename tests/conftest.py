import sys
import os


def pytest_configure():
    # Step up from test/ to my_project/, then into src/boilerplate_ms_python/proto_generated
    proto_generated_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",  # up one directory from test/ to my_project/
            "src",
            "boilerplate_ms_python",
            "proto_generated",
        )
    )
    if proto_generated_path not in sys.path:
        sys.path.insert(0, proto_generated_path)
