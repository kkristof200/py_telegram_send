# ------------------------------------------------------------ Imports ----------------------------------------------------------- #

# System
from typing import List, Optional
import json

# Pip
from kcu import request
from noraise import noraise

from ktg.models.message import Message

# Local
from .models import Message, ParseMode

# -------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------- class: Telegram ------------------------------------------------------- #

class Telegram:

    # --------------------------------------------------------- Init --------------------------------------------------------- #

    def __init__(
        self,
        token: str,
        chat_id: Optional[str] = None,
        debug: bool = False
    ):
        self.token = token
        self.chat_id = chat_id
        self.debug = debug


    # ---------------------------------------------------- Public methods ---------------------------------------------------- #

    def get_updates(
        self,
        allowed_updates: Optional[List[str]] = None
    ):
        return self._send_message(
            endpoint='sendMessage',
            chat_id=chat_id,
            text=message,
            parse_mode=(parse_mode or ParseMode.HTML).value,
            reply_markup=json.dumps(reply_markup) if reply_markup else None,
            **extra_params
        )

    def send(
        self,
        message: str,
        chat_id: Optional[str] = None,
        parse_mode: Optional[ParseMode] = None,
        reply_markup: Optional[dict] = None,
        **extra_params
    ) -> Optional[Message]:
        return self._send_message(
            endpoint='sendMessage',
            chat_id=chat_id,
            text=message,
            parse_mode=(parse_mode or ParseMode.HTML).value,
            reply_markup=json.dumps(reply_markup) if reply_markup else None,
            **extra_params
        )

    def send_poll(
        self,
        question: str,
        options: List[str],
        chat_id: Optional[str] = None,
        allows_multiple_answers: bool = False,
        open_period_seconds: Optional[int] = None,
        **extra_params
    ) -> Optional[Message]:
        return self._send_message(
            endpoint='sendPoll',
            chat_id=chat_id,
            question=question,
            options=json.dumps(options),
            allows_multiple_answers=allows_multiple_answers,
            open_period=open_period_seconds,
            **extra_params
        )

    def delete_message(
        self,
        message_id: str,
        chat_id: Optional[str] = None
    ) -> Optional[dict]:
        return self._send(
            endpoint='deleteMessage',
            chat_id=chat_id,
            message_id=message_id
        )

    @noraise()
    def _send_message(
        self,
        endpoint: str,
        chat_id: Optional[str] = None,
        **extra_params
    ) -> Optional[Message]:
        return Message.from_dict(
            self._send(
                endpoint=endpoint,
                chat_id=chat_id,
                **extra_params
            )['result']
        )

    @noraise()
    def _send(
        self,
        endpoint: str,
        chat_id: Optional[str] = None,
        **extra_params
    ) -> Optional[dict]:
        chat_id = chat_id or self.chat_id

        if not chat_id:
            if self.debug:
                print('ERROR: No chat id')

            return False

        params = {
            'chat_id': chat_id
        }

        if extra_params:
            params.update(extra_params)

        # _params = {}
        
        # for k, v in params.items():
        #     if v is None:
        #         continue

            

        #     _params[k] = v
        params = {k:v for k, v in params.items() if v is not None}

        print(params)

        res = request.get(
            f'https://api.telegram.org/bot{self.token}/{endpoint}',
            params=params
        )

        from kcu import kjson

        kjson.print(res.json())

        return res.json()

    @classmethod
    def send_cls(
        cls,
        token: str,
        message: str,
        chat_id: str,
        parse_mode: Optional[ParseMode] = None,
        debug: bool = False
    ) -> Optional[dict]:
        return cls(token, chat_id, debug).send(message, parse_mode=parse_mode)


# -------------------------------------------------------------------------------------------------------------------------------- #