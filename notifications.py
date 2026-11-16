from winotify import Notification


def notify(icon_path, notifications):
    if notifications:
        notification = Notification(
            app_id="Monitor do Genshin",
            title="Monitor do Genshin",
            msg="O Genshin impact foi encerrado automaticamente.",
            icon=icon_path
        )
        notification.show()
