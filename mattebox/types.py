from __future__ import annotations


class Program:
    name: str
    channel: str
    epg_id: str
    content_id: str
    description: str
    ts_start: int
    ts_stop: int = None
    type: str

    @classmethod
    def from_channel_program(cls, data: dict) -> Program:
        obj = cls()
        obj.__dict__ = {
            "name": data["name"],
            "channel": data["channelKey"],
            "epg_id": data["epgId"],
            "content_id": obj.epg_id,
            "description": data["shortDescription"],
            "ts_start": data["startTimestamp"],
            "ts_stop": data["endTimestamp"],
            "type": "program",
        }
        return obj

    @classmethod
    def from_recording(cls, data: dict) -> Program:
        obj = cls()
        obj.__dict__ = {
            "name": data["title"],
            "channel": data["channelKey"],
            "epg_id": data["epgId"],
            "content_id": data["pvrProgramId"],
            "description": data["longDescription"],
            "ts_start": data["startTime"],
            "type": "recording",
        }
        return obj

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
