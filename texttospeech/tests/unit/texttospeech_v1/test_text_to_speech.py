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

from unittest import mock

import grpc

import pytest

from google import auth
from google.api_core import client_options
from google.auth import credentials
from google.cloud.texttospeech_v1 import enums
from google.cloud.texttospeech_v1.services.text_to_speech import TextToSpeechClient
from google.cloud.texttospeech_v1.services.text_to_speech import transports
from google.cloud.texttospeech_v1.types import cloud_tts
from google.oauth2 import service_account


def test_text_to_speech_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = TextToSpeechClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = TextToSpeechClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "texttospeech.googleapis.com"


def test_text_to_speech_client_client_options():
    # Check the default options have their expected values.
    assert (
        TextToSpeechClient.DEFAULT_OPTIONS.api_endpoint == "texttospeech.googleapis.com"
    )

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.texttospeech_v1.services.text_to_speech.TextToSpeechClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = TextToSpeechClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_text_to_speech_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.texttospeech_v1.services.text_to_speech.TextToSpeechClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = TextToSpeechClient(client_options={"api_endpoint": "squid.clam.whelk"})
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_list_voices(transport: str = "grpc"):
    client = TextToSpeechClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_tts.ListVoicesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_voices), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tts.ListVoicesResponse()
        response = client.list_voices(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_tts.ListVoicesResponse)


def test_list_voices_flattened():
    client = TextToSpeechClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_voices), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tts.ListVoicesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_voices(language_code="language_code_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].language_code == "language_code_value"


def test_list_voices_flattened_error():
    client = TextToSpeechClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_voices(
            cloud_tts.ListVoicesRequest(), language_code="language_code_value"
        )


def test_synthesize_speech(transport: str = "grpc"):
    client = TextToSpeechClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_tts.SynthesizeSpeechRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.synthesize_speech), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tts.SynthesizeSpeechResponse(
            audio_content=b"audio_content_blob"
        )
        response = client.synthesize_speech(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_tts.SynthesizeSpeechResponse)
    assert response.audio_content == b"audio_content_blob"


def test_synthesize_speech_flattened():
    client = TextToSpeechClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.synthesize_speech), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tts.SynthesizeSpeechResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.synthesize_speech(
            input=cloud_tts.SynthesisInput(text="text_value"),
            voice=cloud_tts.VoiceSelectionParams(language_code="language_code_value"),
            audio_config=cloud_tts.AudioConfig(
                audio_encoding=cloud_tts.AudioEncoding.LINEAR16
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].input == cloud_tts.SynthesisInput(text="text_value")
        assert args[0].voice == cloud_tts.VoiceSelectionParams(
            language_code="language_code_value"
        )
        assert args[0].audio_config == cloud_tts.AudioConfig(
            audio_encoding=cloud_tts.AudioEncoding.LINEAR16
        )


def test_synthesize_speech_flattened_error():
    client = TextToSpeechClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.synthesize_speech(
            cloud_tts.SynthesizeSpeechRequest(),
            input=cloud_tts.SynthesisInput(text="text_value"),
            voice=cloud_tts.VoiceSelectionParams(language_code="language_code_value"),
            audio_config=cloud_tts.AudioConfig(
                audio_encoding=cloud_tts.AudioEncoding.LINEAR16
            ),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.TextToSpeechGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = TextToSpeechClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TextToSpeechGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = TextToSpeechClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = TextToSpeechClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.TextToSpeechGrpcTransport)


def test_text_to_speech_base_transport():
    # Instantiate the base transport.
    transport = transports.TextToSpeechTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = ("list_voices", "synthesize_speech")
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_text_to_speech_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        client = TextToSpeechClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_text_to_speech_host_no_port():
    client = TextToSpeechClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="texttospeech.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "texttospeech.googleapis.com:443"


def test_text_to_speech_host_with_port():
    client = TextToSpeechClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="texttospeech.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "texttospeech.googleapis.com:8000"


def test_text_to_speech_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.TextToSpeechGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel


def test_enum_path():
    assert enums.SsmlVoiceGender == cloud_tts.SsmlVoiceGender


def test_enum_path():
    assert enums.SsmlVoiceGender == cloud_tts.SsmlVoiceGender
    assert enums.AudioEncoding == cloud_tts.AudioEncoding
