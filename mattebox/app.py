import requests
import json
import m3u8
from urllib3.exceptions import HTTPError
from typing import List
from .auth import login
from .consts import API
from .helpers import now_timestamp
from .types import Program
from .exceptions import RecordingException


class MatteBOX:
    def __init__(
        self, username: str, password: str, device_id: str, subscription_code: str
    ) -> None:
        self.subscription_code = subscription_code
        self.cookies = {
            "access_token": login(username, password),
            "deviceId": device_id,
        }

    def __get(self, endpoint: str, params: dict) -> dict:
        res = requests.get(API + endpoint, params=params, cookies=self.cookies)
        if res.status_code >= 400:
            raise requests.exceptions.BaseHTTPError(res.text)
        return json.loads(res.text)

    @property
    def channels(self) -> list:
        res = self.__get(
            "/sws/subscription/settings/subscription-channels.json",
            params={"deviceType": "STB"},
        )
        return list(res.keys())

    def get_programs(self, channel: str) -> List[Program]:
        ts_now = now_timestamp()
        res = self.__get(
            "/sws/server/tv/channel-programs.json",
            params={
                "channelKey": channel,
                "fromTimestamp": ts_now - 172800000,  # 48h ago
                "toTimestamp": ts_now,
                "language": "eng",
            },
        )
        programs = [Program.from_channel_program(r) for r in res[::-1]]
        return programs

    @property
    def recordings(self) -> List[Program]:
        res = self.__get(
            "/sws/subscription/vod/pvr-programs.json",
            params={"entityCount": 0, "firstEntityOffset": 0, "language": "eng"},
        )
        recordings = [Program.from_recording(r) for r in res["entities"]]
        return recordings

    def add_recording(self, program: Program) -> None:
        try:
            self.__get(
                "/sws/subscription/vod/pvr-add-program.json",
                params={"epgId": program.epg_id},
            )
        except HTTPError as e:
            raise RecordingException(e) from None

    def remove_recording(self, program: Program) -> None:
        try:
            self.__get(
                "/sws/subscription/vod/pvr-remove-program.json",
                params={"pvrProgramId": program.content_id},
            )
        except HTTPError as e:
            raise RecordingException(e) from None

    def get_stream(self, program: Program, end: bool = True) -> str:
        service_type = "TIMESHIFT_TV" if program.type == "program" else "NPVR"
        if end:
            ts_end = program.ts_stop
        else:
            ts_end = now_timestamp() - 60000 * 3  # 3 minutes ago

        params = {
            "channelKey": program.channel,
            "contentId": program.content_id,
            "serviceType": service_type,
            "subscriptionCode": self.subscription_code,
            "deviceType": "STB",
            "fromTimestamp": program.ts_start,
            "toTimestamp": ts_end,
        }

        res = self.__get("/sws/server/streaming/uris.json", params=params)

        main_playlist_uri = res["uris"][0]["uri"]
        variants = m3u8.load(main_playlist_uri)
        playlist = variants.playlists[0]
        return playlist.uri
