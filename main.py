"""
Developed by Artёm Minin
Moscow 2022

The client app for Websocket Server
"""

import hmac
import hashlib
import asyncio
import logging
import time
from datetime import datetime, timedelta

import websockets

import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")


def strip_key(key_to_strip):
    """
    Обрезает ключ и возвращает его значение.
    :param key_to_strip: ex. b"Key: n5AUbpMiEGV1WvAcgvjFdm75vDqrvFlm884ZN9IEBjJshGgOouCuNx"
    :return: ex. b'n5AUbpMiEGV1WvAcgvjFdm75vDqrvFlm884ZN9IEBjJshGgOouCuNx'
    """
    key_stripped = key_to_strip.split()[1]
    logger.debug(f'stripped key: {key_stripped}, type: {type(key_stripped)}')
    return key_stripped


def convert_email(key: bytes, some_email: str):
    """
    Кодирует e-mail в HMAC-sha256, в соответствии с инструкцией, которая прилетает от сервера
    :param key: ключ, который прилетает с сервера после подключения. Важно, чтобы он был очищен!
    :param some_email: наш e-mail, который хранится в config
    :return: ex. b"\x01\xac$5\x19IQ'V\xf2\xd5\xc0\x00\xa5;\x85Cs\xf5 \xd1\xc7\xc7\xc7\x9c\xa1%\x1dU\x8d\xad\xc5
    """
    signature_hmac = hmac.new(key, some_email.encode(), hashlib.sha256)
    signature = signature_hmac.digest()
    logger.debug(f'{some_email} converted to {signature}')
    return signature


def compose_payload(email: str, signature: bytes):
    """
    Собираем сообщение для отправки
    :param email: наш e-mail из config
    :param signature: закодированный e-mail из функции convert_email()
    :return: ex. b"minin.kp11@gmail.com:\x01\xac$5\x19IQ'V\ ... \x8d\xad\xc5"
    """
    email_mod = email + ':'
    payload = email_mod.encode() + signature
    logger.debug(f'payload to send: {payload}')
    return payload


async def communicate(uri):
    """
    Основная функция, осуществляющее взаимодействие с websocket сервером
    :param uri: адрес сервера из config
    :return: принтит логи и сообщения сервера
    """
    async with websockets.connect(uri) as ws:
        try:
            # getting the Key from the server
            key_raw = await ws.recv()
            logger.debug(f'Raw key received: {key_raw}')
            key = strip_key(key_raw)
            logger.debug("key = " + key.decode('ascii'))

            # according to instruction from the server, encoding email
            signed_email = convert_email(key, config.email)
            payload = compose_payload(config.email, signed_email)
            time.sleep(1)

            # sending our message to the server
            msg = await ws.send(payload)  # Responding None
            logger.debug(f'payload sent. Response: {msg}')
            time.sleep(1)

            # printing responses
            start_time = datetime.utcnow()
            now = start_time
            while now < start_time + timedelta(seconds=10):
                now = datetime.utcnow()
                msg = await ws.recv()
                print(msg)
                time.sleep(0.1)

            ws.close()

        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(communicate(uri=config.url))

