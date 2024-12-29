from typing import Any
from urllib.parse import urlencode

import requests


class BrightDataClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def send_request(
        self, method: str, path: str, qs: dict[str, str] = None, payload=None
    ):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        query = "?" + urlencode(qs) if qs is not None else ""
        url = f"https://api.brightdata.com/{path}{query}"

        return requests.request(method, url, headers=headers, json=payload)

    def trigger_data_collection(
        self,
        dataset_id: str,
        limit_per_input: int,
        include_errors: bool,
        payload: Any,
        type: str = None,
        discover_by: str = None,
    ):
        params = {
            "dataset_id": dataset_id,
            "limit_per_input": limit_per_input,
            "include_errors": "true" if include_errors else "false",
        }

        if type is not None:
            params["type"] = type

        if discover_by is not None:
            params["discover_by"] = discover_by

        res = self.send_request("POST", "datasets/v3/trigger", params, payload)
        return res.json()

    def monitor_progress(self, snapshot_id: str):
        res = self.send_request("GET", f"datasets/v3/progress/{snapshot_id}")
        return res.json()

    def download(self, snapshot_id: str) -> str:
        params = {"format": "jsonl"}
        res = self.send_request("GET", f"datasets/v3/snapshot/{snapshot_id}", params)

        return res.text
