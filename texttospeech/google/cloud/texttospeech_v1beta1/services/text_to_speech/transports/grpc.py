# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Callable, Dict

from google.api_core import grpc_helpers  # type: ignore
from google.auth import credentials  # type: ignore

import grpc  # type: ignore

from google.cloud.texttospeech_v1beta1.types import cloud_tts

from .base import TextToSpeechTransport


class TextToSpeechGrpcTransport(TextToSpeechTransport):
    """gRPC backend transport for TextToSpeech.

    Service that implements Google Cloud Text-to-Speech API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "texttospeech.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
        """
        # Sanity check: Ensure that channel and credentials are not both
        # provided.
        if channel:
            credentials = False

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

        # If a channel was explicitly provided, set it.
        if channel:
            self._grpc_channel = channel

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = grpc_helpers.create_channel(
                self._host, credentials=self._credentials, scopes=self.AUTH_SCOPES
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def list_voices(
        self
    ) -> Callable[[cloud_tts.ListVoicesRequest], cloud_tts.ListVoicesResponse]:
        r"""Return a callable for the list voices method over gRPC.

        Returns a list of Voice supported for synthesis.

        Returns:
            Callable[[~.ListVoicesRequest],
                    ~.ListVoicesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_voices" not in self._stubs:
            self._stubs["list_voices"] = self.grpc_channel.unary_unary(
                "/google.cloud.texttospeech.v1beta1.TextToSpeech/ListVoices",
                request_serializer=cloud_tts.ListVoicesRequest.serialize,
                response_deserializer=cloud_tts.ListVoicesResponse.deserialize,
            )
        return self._stubs["list_voices"]

    @property
    def synthesize_speech(
        self
    ) -> Callable[
        [cloud_tts.SynthesizeSpeechRequest], cloud_tts.SynthesizeSpeechResponse
    ]:
        r"""Return a callable for the synthesize speech method over gRPC.

        Synthesizes speech synchronously: receive results
        after all text input has been processed.

        Returns:
            Callable[[~.SynthesizeSpeechRequest],
                    ~.SynthesizeSpeechResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "synthesize_speech" not in self._stubs:
            self._stubs["synthesize_speech"] = self.grpc_channel.unary_unary(
                "/google.cloud.texttospeech.v1beta1.TextToSpeech/SynthesizeSpeech",
                request_serializer=cloud_tts.SynthesizeSpeechRequest.serialize,
                response_deserializer=cloud_tts.SynthesizeSpeechResponse.deserialize,
            )
        return self._stubs["synthesize_speech"]


__all__ = ("TextToSpeechGrpcTransport",)
