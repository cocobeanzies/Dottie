import contextlib, concurrent.futures

GLOBALS = globals()


PREFIX = ["d.", "D."]

INVITE = "https://discord.com/api/oauth2/authorize?client_id=737992099449929728&permissions=804645958&scope=bot"

OWNERS = [530781444742578188, 201548633244565504]

def is_owner(ctx):
  return ctx.message.author.id in OWNERS


try:
    with open("database/terminal_channels.txt", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
TERMINALS = {int(i) for i in s.splitlines() if i}

try:
    with open("database/DM_channels.txt", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
DM_CHANNEL = {int(i) for i in s.splitlines() if i}

try:
    with open("database/log_channels.txt", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
LOG_CHANNELS = {int(i) for i in s.splitlines() if i}

try:
    with open("database/topicloop_channels.txt", "r") as f:
        s = f.read()
except FileNotFoundError:
    s = ""
TOPICLOOP_CHANNELS = {int(i) for i in s.splitlines() if i}


required_emojis = {
    881133619983302718: "<:cheesecake:881133619983302718>", 
    881205443320479754: "<:kitten:881205443320479754>",
    881202126070624286: "<:puppy:881202126070624286>",
    797359273914138625: "<a:_:797359273914138625>",
    797359354314620939: "<a:_:797359354314620939>",
    797359351509549056: "<a:_:797359351509549056>",
    797359341157482496: "<a:_:797359341157482496>",
    722354192995450912: "<:_:722354192995450912>",
    833117645863780402: "<:colondead:833117645863780402>",
    760062353063936000: "<:empty:760062353063936000>",
    818530242971959337: "<a:cries_gif:818530242971959337>",
    818530180431741009: "<a:dummy_gif:818530180431741009>",
    712902348984549437: "<:smudgedead:712902348984549437>",
    712902347512217610: "<:txindead:712902347512217610>",
    867008087889805332: "<:LMOR_Lore:867008087889805332>",
    867008777327476756: "<:LMOR_Speedpaint:867008777327476756>",
    867008362436886558: "<:LMOR_Iss1:867008362436886558>",
    788165800448098324: "<:miza_dottie_hug:788165800448098324>",
    516974531852632066: "<a:RainbowCritterTransparent:516974531852632066>",
    776855303282229278: "<a:Smudge_FaceSprites:776855303282229278>",
    799211332632969256: "<:Txin_Smudge_Hug:799211332632969256>",
    751543624268775526: "<:Smudge:751543624268775526>",
    748840270069760072: "<a:curiouseal:748840270069760072>",
    670143859149242369: "<:seal_ball:670143859149242369>",
    762367799150510164: "<:sleepy_fox:762367799150510164>"
}


class MultiThreadedImporter(contextlib.AbstractContextManager, contextlib.ContextDecorator):

    def __init__(self, glob=None):
        self.glob = glob
        self.exc = concurrent.futures.ThreadPoolExecutor(max_workers=12)
        self.out = {}

    def __enter__(self):
        return self

    def __import__(self, *modules):
        for module in modules:
            self.out[module] = self.exc.submit(__import__, module)

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        if exc_type and exc_value:
            raise exc_value

    def close(self):
        for k in tuple(self.out):
            self.out[k] = self.out[k].result()
        glob = self.glob if self.glob is not None else globals()
        glob.update(self.out)
        self.exc.shutdown(True)


with MultiThreadedImporter() as importer:
    importer.__import__(
        "subprocess",
        "inspect",
        "time",
        "datetime",
        "random",
        "copy",
        "requests",
        "asyncio",
        "os",
        "psutil",
        "traceback",
        "math",
        "discord",
        "discord.ext",
        "json",
        "threading",
        "sys",
        "inspirobot",
        "re",
        "io",
        "PIL",
        "aiohttp",
        "urllib",
        "collections",
        "contextlib",
        "inspect",
    )

from PIL import Image, ImageDraw, ImageChops
from math import *
from discord.ext import tasks, commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord import utils
from collections import deque
sys.path.insert(1, "misc"); from alist import *


eloop = asyncio.get_event_loop()
def __setloop__(): return asyncio.set_event_loop(eloop)


athreads = concurrent.futures.ThreadPoolExecutor(
    max_workers=64,
    initializer=__setloop__,)
__setloop__()


def get_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return eloop

def wrap_future(fut, loop=None):
    if loop is None:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = eloop
    new_fut = loop.create_future()

    def on_done(*void):
        try:
            result = fut.result()
        except Exception as ex:
            loop.call_soon_threadsafe(new_fut.set_exception, ex)
        else:
            loop.call_soon_threadsafe(new_fut.set_result, result)

    fut.add_done_callback(on_done)
    return new_fut


def awaitable(obj): return hasattr(obj, "__await__") or issubclass(type(obj), asyncio.Future) or issubclass(type(obj), asyncio.Task) or inspect.isawaitable(obj)


def create_future_ex(func, *args, timeout=None, **kwargs):
    try:
        kwargs["timeout"] = kwargs.pop("_timeout_")
    except KeyError:
        pass
    fut = athreads.submit(func, *args, **kwargs)
    if timeout is not None:
        fut = athreads.submit(fut.result, timeout=timeout)
    return fut


async def _create_future(obj, *args, loop, timeout, **kwargs):
    if asyncio.iscoroutinefunction(obj):
        obj = obj(*args, **kwargs)
    elif callable(obj):
        if asyncio.iscoroutinefunction(obj.__call__) or not is_main_thread():
            obj = obj.__call__(*args, **kwargs)
        else:
            obj = await wrap_future(create_future_ex(obj, *args, timeout=timeout, **kwargs), loop=loop)
    while awaitable(obj):
        if timeout is not None:
            obj = await asyncio.wait_for(obj, timeout=timeout)
        else:
            obj = await obj
    return obj


def create_future(obj, *args, loop=None, timeout=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    fut = _create_future(obj, *args, loop=loop, timeout=timeout, **kwargs)
    if not isinstance(fut, asyncio.Task):
        fut = create_task(fut, loop=loop)
    return fut


def create_task(fut, *args, loop=None, **kwargs):
    if loop is None:
        loop = get_event_loop()
    return asyncio.ensure_future(fut, *args, loop=loop, **kwargs)

is_main_thread = lambda: threading.current_thread() is threading.main_thread()


pink_embed = 15277667

rainbow_embeds = [
    16711680,
    16738304,
    16773888,
    2948864,
    61951,
    6655,
    8323327,
    16711861
]


def create_progress_bar(length, ratio):
	start_bar = [
		"<:_:777028747383013376>",
		"<a:_:777028749970636833>",
		"<a:_:777028752660103179>",
		"<a:_:777028754983485462>",
		"<a:_:777028758895853589>",
	]
	mid_bar = [
		"<:_:777028760477892668>",
		"<a:_:777028763149271061>",
		"<a:_:777028767125995520>",
		"<a:_:777028769839054878>",
		"<a:_:777028773320589375>",
	]
	end_bar = [
		"<:_:777028775451820032>",
		"<a:_:777028777909551144>",
		"<a:_:777028780640305202>",
		"<a:_:777028782766555137>",
		"<a:_:777028787971424288>",
	]
	high = length * 4
	position = min(high, round(ratio * high))
	items = []
	new = min(4, position)
	items.append(start_bar[new])
	position -= new
	for i in range(length - 1):
		new = min(4, position)
		if i >= length - 2:
			bar = end_bar
		else:
			bar = mid_bar
		items.append(bar[new])
		position -= new
	return "".join(items)


def get_random_emoji():
    d = [chr(c) for c in range(128512, 128568)]
    d.extend(chr(c) for c in range(128577, 128580))
    d.extend(chr(c) for c in range(129296, 129302))
    d.extend(chr(c) for c in range(129312, 129318))
    d.extend(chr(c) for c in range(129319, 129328))
    d.extend(chr(c) for c in range(129392, 129399))
    d.extend(chr(c) for c in (129303, 129400, 129402))
    return random.choice(d)


if not os.path.exists("database"):
    try:
        print("Checking for database files, folder will be created if missing...")
        os.mkdir("database")
    except Exception as e:
        print()

if not os.path.exists("config.json") or not os.path.getsize("config.json"):
    print("No token found, generating config.json file... Please include Discord token when complete.\n\n")
    with open("config.json", "w") as f:
        template = {
            "token": ""
        }
        json.dump(template, f, indent=4)
        raise SystemExit


def start_miza():
    try:
        if "MIZA" in GLOBALS:
            stop_miza()
        GLOBALS["MIZA"] = psutil.Popen(["python", "bot.py"], cwd=os.getcwd() + "/Miza-VOICE", stdout=subprocess.DEVNULL)
    except:
        print("Directory \"MIZA-VOICE\" not found.\n")

def stop_miza():
    try:
        p = GLOBALS["MIZA"]
        for c in p.children(recursive=True):
            c.kill()
        p.kill()
    except psutil.NoSuchProcess:
        pass
        

start_miza()
if not os.path.exists("Miza-VOICE/auth.json") or not os.path.getsize("Miza-VOICE/auth.json"):
    try:
        print("Voice command's subprocess has incomplete configuration, generating auth.json file located under Miza-VOICE... Please include available data if desired.\n(Note that information such as the token and the prefix should be the same as the main bot process'.)\n\n")
        with open("Miza-VOICE/auth.json", "w") as f:
            template = {
                "prefix": "",
                "webserver_port": "",
                "encryption_key": "",
                "python_path":"",
                "discord_token": "",
                "google_api_key": "",
                "genius_key": ""
            }
            json.dump(template, f, indent=4)
    except Exception as e:
        print()
        GLOBALS.pop("MIZA", None)

with open("MIZA-VOICE/auth.json", "r") as f:
    data = json.load(f)
    miza_token = data["discord_token"]
    if miza_token == "":
        print("Discord token under MIZA-VOICE \"auth.json\" not found. To configure voice commands, please add the Discord token.\n(Note that information such as the token and the prefix should be the same as the main bot process'.)\n\n")
        GLOBALS.pop("MIZA", None)


emptyfut = fut_nop = asyncio.Future()
fut_nop.set_result(None)
newfut = concurrent.futures.Future()
newfut.set_result(None)


globals().update(discord.ext.commands.view.__dict__)

def get_quoted_word(self):
    current = self.current
    if current is None:
        return

    close_quote = _quotes.get(current)
    is_quoted = bool(close_quote)
    if is_quoted:
        result = []
        _escaped_quotes = (current, close_quote)
    else:
        result = [current]
        _escaped_quotes = _all_quotes

    while not self.eof:
        current = self.get()
        if not current:
            return ''.join(result)

        if current == '\\':
            next_char = self.get()
            if not next_char:
                return ''.join(result)

            if next_char in _escaped_quotes:
                result.append(next_char)
            else:
                self.undo()
                result.append(current)
            continue

        if is_quoted and current == close_quote:
            next_char = self.get()
            valid_eof = not next_char or next_char.isspace()
            return ''.join(result)

        if current.isspace() and not is_quoted:
            return ''.join(result)

        result.append(current)


discord.ext.commands.view.StringView.get_quoted_word = lambda self: get_quoted_word(self)