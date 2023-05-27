import os
import shutil
import uuid
import cv2
from pyrogram import Client, filters
from pyrogram.types import Message

from download import BunnyVideoDRM

BOT_TOKEN = ""

app = Client("bot", api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e", bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def __start(_, m: Message):
    await m.reply_text("Hi, send me a bunnyvideo link to download it!", quote=True)

def get_video_info(file_path):
    cap = cv2.VideoCapture(file_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count // fps

    # Calculate middle frame index
    middle_frame_index = frame_count // 2

    # Set frame position to the middle frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_index)

    # Read the middle frame
    ret, frame = cap.read()
    ss_path = f"./downloads/{uuid.uuid4().hex}.jpg"

    cap.release()

    if ret:
        # Save the middle frame as an image
        cv2.imwrite(ss_path, frame)
        print("Middle frame captured successfully!")
    else:
        print("Failed to capture middle frame.")

    ss_path = None if not ret else ss_path

    return width, height, int(duration), ss_path


@app.on_message(filters.text)
async def __download(_, m: Message):
    try:
        msg = await m.reply_text("Downloading...", quote=True)

        url = m.text.split("\n\n")[0]
        caption = m.text.split("\n\n")[1]

        v_name = uuid.uuid4().hex
        # v_name = "d253eff8dc2446e6b25e9e620bc3f973"

        video = BunnyVideoDRM(
            referer='https://iframe.mediadelivery.net/',
            embed_url=url,
            name=v_name,
            path="./downloads/"
        )
        video.download()

        v_path = f"./downloads/{v_name}.mp4"
        shutil.rmtree(f"./downloads/.{v_name}.mp4", ignore_errors=True)

        width, height, duration, ss_path = get_video_info(v_path)

        await msg.edit_text("Uploading...")
        await m.reply_video(v_path, quote=True, width=width, height=height, duration=duration, thumb=ss_path, caption=caption)

        await msg.delete()

        os.remove(v_path)
        os.remove(ss_path)
    except Exception as e:
        await m.reply_text(f"Error: {e}", quote=True)

print("Bot started!")
app.run()
