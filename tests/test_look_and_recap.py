"""`look` shows the scene's text again; continuing a save starts with a
"Previously:" recap of the latest journal entries."""

import json
from pathlib import Path

import pytest

from sidechannel import web_bridge as bridge
from sidechannel.engine.journal import JournalEntry
from sidechannel.engine.session import GameSession
from sidechannel.engine.story import Story
from sidechannel.tui import GameApp

DEAD_DROP = Path(__file__).parent.parent / "sidechannel" / "stories" / "story_02_dead_drop"


def terminal_session(tmp_path: Path) -> GameSession:
    session = GameSession.open(Story.load(DEAD_DROP), DEAD_DROP, tmp_path / "save.json", fresh=True)
    session.choose(session.available_choices()[0])  # -> relay_shell, a terminal scene
    assert session.scene.type == "terminal"
    return session


def test_look_asks_the_frontend_to_show_the_scene_again(tmp_path):
    session = terminal_session(tmp_path)
    result = session.run_command("look")
    assert result.look and not result.advanced and result.output == ""
    assert not session.run_command("help").look  # only for `look`


def test_recap_only_for_a_continued_save_with_the_latest_entries(tmp_path):
    session = terminal_session(tmp_path)
    assert not session.continued
    for i in range(5):
        session.state.journal.add(JournalEntry(id=f"e{i}", category="note", text=f"entry {i}"))
    session.save()

    continued = GameSession.open(Story.load(DEAD_DROP), DEAD_DROP, session.slot_path, fresh=False)
    assert continued.continued
    assert continued.recap() == ["entry 2", "entry 3", "entry 4"]


@pytest.fixture
def web(tmp_path):
    bridge.init(str(tmp_path))
    yield
    bridge.init("/saves")


def test_bridge_look_and_recap(web):
    bridge.start("dead_drop", "web", True)
    bridge.choose(0)
    view = json.loads(bridge.command("look"))
    assert view["look"] and view["scene"]["html"]
    assert json.loads(bridge.start("dead_drop", "web", True))["recap"] == []
    bridge._require_session().state.journal.add(JournalEntry(id="x", category="lead", text="the relay"))
    bridge.save()
    assert json.loads(bridge.start("dead_drop", "web", False))["recap"] == ["the relay"]


@pytest.mark.asyncio
async def test_tui_shows_the_recap_and_look_writes_the_scene_again(tmp_path):
    session = terminal_session(tmp_path)
    session.state.journal.add(JournalEntry(id="x", category="lead", text="the relay [lead]"))
    session.save()
    app = GameApp(GameSession.open(Story.load(DEAD_DROP), DEAD_DROP, session.slot_path, fresh=False))
    texts: list[str] = []
    app.log_text = lambda text, style=None: texts.append(text)  # type: ignore[method-assign]
    async with app.run_test() as pilot:
        await pilot.pause()
        assert texts[0] == "Previously:\n- the relay \\[lead]"  # escaped for Rich markup
        app.show_result(app.session.run_command("look"))
        assert texts[-1] == app.session.scene.text
