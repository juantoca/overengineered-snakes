from dataclasses import dataclass
from pathlib import Path
from shutil import move
from subprocess import Popen
from typing import Any

root_path = Path(__file__).parent.parent
langs_path = root_path / "langs"

all_langs_path = langs_path.glob("*")


@dataclass
class LanguageArtifacts:
    identifier: str
    source: Path
    config: Path
    build: Path
    target: Path


artifacts = list(
    map(
        lambda path: LanguageArtifacts(
            path.parts[-1],
            path,
            path / "mkdocs.yml",
            path / "site",
            root_path / "site" / path.parts[-1]
            if path.parts[-1] != "en"
            else root_path / "site",
        ),
        all_langs_path,
    ),
)


def build_language(path: LanguageArtifacts) -> Popen[Any]:
    return Popen(["mkdocs", "build", "-f", path.config])


print("\n[Building static language sites]:")

build_processes = list(map(lambda artifact: build_language(artifact), artifacts))

for x in build_processes:
    x.wait()

for art in artifacts:
    move(art.build, art.target)
