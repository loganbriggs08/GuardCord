from win10toast import ToastNotifier

toast_notifier_client: object = ToastNotifier()

class Notifications:
    def send(post_title: str, post_body: str, duration: int) -> bool:
        toast_notifier_client.show_toast(post_title, post_body, duration=duration)