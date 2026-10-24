"""Names a story gives to things that become files or directories (host
and file names, NPC and topic ids, the story id) must stay one path
segment, so a story can never write outside its sandbox."""

from pathlib import Path

import pytest
import yaml

from sidechannel.engine.dialogue import load_npcs
from sidechannel.engine.shell import Network, materialize_fs_node
from sidechannel.engine.story import Story, StoryLoadError

UNSAFE = ["../../../.bashrc", "a/b", "..", ".", "", "a\\b", "c:x", "nul\0"]


def _network(tmp_path: Path, hosts: dict) -> Network:
    path = tmp_path / "network.yaml"
    path.write_text(yaml.safe_dump({"hosts": hosts}))
    return Network.load(path)


@pytest.mark.parametrize("name", UNSAFE)
def test_unsafe_file_name_fails_to_load(tmp_path, name):
    with pytest.raises(StoryLoadError, match="invalid file name"):
        _network(tmp_path, {"box": {"filesystem": {"etc": {"entries": {name: {"type": "text"}}}}}})


@pytest.mark.parametrize("name", UNSAFE)
def test_unsafe_host_id_fails_to_load(tmp_path, name):
    with pytest.raises(StoryLoadError, match="invalid host id"):
        _network(tmp_path, {name: {}})


@pytest.mark.parametrize("field", ["npc", "topic"])
def test_unsafe_npc_and_topic_ids_fail_to_load(field):
    topic = {"id": "../x" if field == "topic" else "t", "prompt": "p", "response": "r"}
    npc = {"id": "../x" if field == "npc" else "n", "topics": [topic]}
    with pytest.raises(StoryLoadError, match=f"invalid {field} id"):
        load_npcs({"npcs": [npc]})


def test_unsafe_story_id_fails_to_load(tmp_path):
    (tmp_path / "manifest.yaml").write_text(yaml.safe_dump({"id": "../x", "start": "a:b", "chapters": []}))
    with pytest.raises(StoryLoadError, match="invalid story id"):
        Story.load(tmp_path)


def test_materialize_refuses_an_escaping_name_even_unchecked(tmp_path):
    with pytest.raises(StoryLoadError, match="Unsafe"):
        materialize_fs_node({"../escaped": {"type": "text", "content": "x"}}, tmp_path / "host")
    assert not (tmp_path / "escaped").exists()
