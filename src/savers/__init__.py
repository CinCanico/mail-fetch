from src.enums import Saver
from src.savers.base import SaverBase
from src.savers.eml import EmlSaver
from src.savers.mbox import MboxSaver


def get_saver(saver_type: Saver, username: str, mailbox_name: str, max_size: int = 128 * 1024 * 1024) -> SaverBase:
    if saver_type == Saver.MBOX:
        return MboxSaver(username, mailbox_name, max_size)
    else:
        return EmlSaver(username, mailbox_name)
