from pathlib import Path
from typing import Dict, Final

from _manifest_dto import ManifestDTO, get_correct_manifest
from _services_dto import create_yaml

CONFIG_FILES: Final[Dict[str, str]] = {
    "manifest.json": get_correct_manifest(ManifestDTO()),
    "services.yaml": create_yaml()
}

def __create_file(file: Path, content: str) -> None:
    with open(file, "w") as out_file:
        out_file.write(content)
    
    assert file.exists()

def _create_config_files(dist_folder: Path):
    print("[*] Create config files in dist folder")

    for config_file_name, config_file_content in CONFIG_FILES.items():
        print(f"[*] Creating {config_file_name}: ", end = "")

        dist_config_file_path = dist_folder.joinpath(config_file_name)
        __create_file(dist_config_file_path, config_file_content)

        print("OK")

def generate() -> None:
    dist_folder = Path("./")

    _create_config_files(dist_folder)
    

if __name__ == "__main__":
    generate()
