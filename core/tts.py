"""Text-to-speech for DJ Catto's spoken lines.

Default voice is edge-tts (free, no key). If OPENAI_API_KEY is set, the cheapest
realistic OpenAI voice (gpt-4o-mini-tts) is used under a monthly spend cap; when
the cap is hit it falls back to the free voice and DMs the owner once.
"""

import contextlib
import datetime
import logging
import os
import tempfile

import aiohttp

from core import db

log = logging.getLogger("catto")

EDGE_VOICE = "en-US-EricNeural"  # calm, laid-back
OPENAI_MODEL = "gpt-4o-mini-tts"
OPENAI_VOICE = "ash"
OPENAI_INSTRUCTIONS = "Speak like a chill, laid-back late-night radio DJ: warm, relaxed, unhurried."
USD_PER_CHAR = 0.00002  # conservative estimate for gpt-4o-mini-tts
MONTHLY_CAP_USD = 2.00
ALERT_USER_ID = 1331907055635796022


class TTSEngine:
    def __init__(self, bot):
        self.bot = bot

    @property
    def openai_key(self) -> str | None:
        return os.getenv("OPENAI_API_KEY")

    @staticmethod
    def _period() -> str:
        return datetime.datetime.now(datetime.UTC).strftime("%Y-%m")

    async def synth(self, text: str) -> str | None:
        """Return a path to an mp3 of `text`, or None on failure. Caller deletes it."""
        text = (text or "").strip()
        if not text:
            return None
        fd, path = tempfile.mkstemp(prefix="catto_tts_", suffix=".mp3")
        os.close(fd)
        if self.openai_key:
            if await self._within_budget(len(text)):
                if await self._openai(text, path):
                    await db.tts_spend_add(self._period(), len(text) * USD_PER_CHAR)
                    return path
            else:
                await self._alert_cap()
        if await self._edge(text, path):
            return path
        with contextlib.suppress(Exception):
            os.remove(path)
        return None

    async def _within_budget(self, nchars: int) -> bool:
        spent, _ = await db.tts_spend_get(self._period())
        return spent + nchars * USD_PER_CHAR <= MONTHLY_CAP_USD

    async def _openai(self, text: str, path: str) -> bool:
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.post(
                    "https://api.openai.com/v1/audio/speech",
                    headers={"Authorization": f"Bearer {self.openai_key}"},
                    json={
                        "model": OPENAI_MODEL,
                        "voice": OPENAI_VOICE,
                        "input": text,
                        "instructions": OPENAI_INSTRUCTIONS,
                        "response_format": "mp3",
                    },
                    timeout=aiohttp.ClientTimeout(total=20),
                ) as resp,
            ):
                if resp.status != 200:
                    log.warning("OpenAI TTS failed: HTTP %s", resp.status)
                    return False
                data = await resp.read()
            with open(path, "wb") as fh:
                fh.write(data)
            return os.path.getsize(path) > 0
        except Exception:
            log.exception("OpenAI TTS error")
            return False

    async def _edge(self, text: str, path: str) -> bool:
        try:
            import edge_tts

            await edge_tts.Communicate(text, EDGE_VOICE).save(path)
            return os.path.getsize(path) > 0
        except Exception:
            log.exception("edge-tts error")
            return False

    async def _alert_cap(self) -> None:
        period = self._period()
        _, alerted = await db.tts_spend_get(period)
        if alerted:
            return
        await db.tts_set_alerted(period)
        with contextlib.suppress(Exception):
            user = self.bot.get_user(ALERT_USER_ID) or await self.bot.fetch_user(ALERT_USER_ID)
            if user is not None:
                await user.send(
                    f"Heads up: the DJ voice hit its ${MONTHLY_CAP_USD:.0f} cap for {period}. "
                    "Switched to the free voice for the rest of the month."
                )
