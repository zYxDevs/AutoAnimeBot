from config import INDEX_USERNAME, SCHEDULE_ID, STATUS_ID, UPLOADS_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="View Schedule",
                url=f"https://t.me/{UPLOADS_USERNAME}/{SCHEDULE_ID}",
            )
        ],
        [
            InlineKeyboardButton(
                text="Index Channel", url=f"https://t.me/{INDEX_USERNAME}"
            ),
            InlineKeyboardButton(
                text="Discussion Group", url="https://t.me/+Q0xUxmKd1bQyMWI9"
            ),
        ],
    ]
)


button2 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Check Queue", url= f"https://t.me/{UPLOADS_USERNAME}/{STATUS_ID}")
            ]
        ]
    )