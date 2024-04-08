from abc import ABC, abstractmethod


class ImageGenerator(ABC):
    @abstractmethod
    def get_image_url(self, prompt: str) -> str:
        pass

    @abstractmethod
    def download_image(self, image_url: str, path: str) -> None:
        pass
