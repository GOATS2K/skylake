# pyright: reportPrivateImportUsage=false
from hcloud import Client
from hcloud.servers.client import BoundServer
from hcloud.actions.client import BoundAction
from hcloud.servers.domain import CreateServerResponse
from hcloud.server_types.domain import ServerType
from hcloud.images.client import BoundImage
from hcloud.datacenters.client import BoundDatacenter


class HetznerClient:
    def __init__(self, client: Client, server_name: str) -> None:
        self.client = client
        self.server_name = server_name

    def create_snapshot(self, server_id: int) -> None:
        pass

    def remove_snapshot(self, snapshot: str) -> None:
        pass

    def get_server(self) -> BoundServer | None:
        return self.client.servers.get_by_name(self.server_name)

    def _get_datacenter(self, datacenter_name: str) -> BoundDatacenter:
        datacenter_list = self.client.datacenters.get_all()
        datacenter = next(
            (dc for dc in datacenter_list if dc.name == datacenter_name), None
        )
        if not datacenter:
            raise ValueError("Invalid datacenter name.")

        return datacenter

    def _get_image(
        self, image_name: str, image_is_snapshot: bool = False
    ) -> BoundImage:
        types = ["system"]
        if image_is_snapshot:
            types = ["snapshot"]

        # Source servers only run on x86 as far as I am aware.
        image_list = self.client.images.get_list(architecture=["x86"], type=types)
        image = next(
            (
                image
                for image in image_list.images
                if image.name == image_name or image.description == image_name
            ),
            None,
        )
        if not image:
            raise ValueError("Invalid image name.")
        return image

    def _get_server_type(self, sku: str) -> ServerType:
        types = self.client.server_types.get_all()
        requested_type = next(
            (server_type for server_type in types if server_type.name == sku), None
        )
        if not requested_type:
            raise ValueError("Invalid SKU.")
        return requested_type

    def create_server(
        self,
        datacenter_name: str,
        sku: str = "cpx31",
        image_name: str = "debian-11",
        image_is_snapshot: bool = False,
    ) -> CreateServerResponse:
        server_type = self._get_server_type(sku)
        image = self._get_image(image_name, image_is_snapshot=image_is_snapshot)
        datacenter = self._get_datacenter(datacenter_name)

        server_response = self.client.servers.create(
            self.server_name,
            server_type=server_type,
            image=image,
            datacenter=datacenter,
        )
        return server_response

    def teardown_server(self) -> BoundAction:
        server = self.get_server()
        if not server:
            raise ValueError("Cannot find server.")
        return self.client.servers.delete(server)
