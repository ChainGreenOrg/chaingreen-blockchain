from typing import Callable, Optional

from chaingreen.introducer.introducer import Introducer
from chaingreen.protocols.introducer_protocol import RequestPeersIntroducer, RespondPeersIntroducer
from chaingreen.protocols.protocol_message_types import ProtocolMessageTypes
from chaingreen.server.outbound_message import Message, make_msg
from chaingreen.server.ws_connection import WSChaingreenConnection
from chaingreen.types.peer_info import TimestampedPeerInfo
from chaingreen.util.api_decorators import api_request, peer_required
from chaingreen.util.ints import uint64, uint16


class IntroducerAPI:
    introducer: Introducer

    def __init__(self, introducer) -> None:
        self.introducer = introducer

    def _set_state_changed_callback(self, callback: Callable):
        pass

    @peer_required
    @api_request
    async def request_peers_introducer(
        self,
        request: RequestPeersIntroducer,
        peer: WSChaingreenConnection,
    ) -> Optional[Message]:
        max_peers = self.introducer.max_peers_to_send
        if self.introducer.server is None or self.introducer.server.introducer_peers is None:
            return None
        rawpeers = self.introducer.server.introducer_peers.get_peers(
            max_peers * 5, True, self.introducer.recent_peer_threshold
        )

        peers = []
        peers.append(
            TimestampedPeerInfo(
                "eu1.node.chaingreen.org",
                uint16(8744),
                uint64(0),
            )
        )

        peers.append(
            TimestampedPeerInfo(
                "eu2.node.chaingreen.org",
                uint16(8744),
                uint64(0),
            )
        )

        peers.append(
            TimestampedPeerInfo(
                "eu3.node.chaingreen.org",
                uint16(8744),
                uint64(0),
            )
        )

        peers.append(
            TimestampedPeerInfo(
                "us1.node.chaingreen.org",
                uint16(8744),
                uint64(0),
            )
        )

        for r_peer in rawpeers:
            if r_peer.vetted <= 0:
                continue

            if r_peer.host == peer.peer_host and r_peer.port == peer.peer_server_port:
                continue

            if r_peer.port == 8444:
                continue

            peer_without_timestamp = TimestampedPeerInfo(
                r_peer.host,
                r_peer.port,
                uint64(0),
            )
            peers.append(peer_without_timestamp)

            if len(peers) >= max_peers:
                break

        if peer.port == 8444:
            peers = []
            self.introducer.log.info("Sending empty peers to a Chia node")
        else:
            self.introducer.log.info(f"Sending vetted {peers}")

        msg = make_msg(ProtocolMessageTypes.respond_peers_introducer, RespondPeersIntroducer(peers))
        return msg
