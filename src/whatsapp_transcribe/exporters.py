from dataclasses import dataclass
from typing import TypedDict


@dataclass()
class ExtismManifest(TypedDict):
    url: str
    hash: str


@dataclass()
class ExporterPlugin:
    extism_manifest: ExtismManifest
    url: str


class PluginRegistry:
    def __init__(self):
        self.plugins = {}

    def register(self, plugin: ExporterPlugin):
        self.plugins[plugin.url] = plugin
