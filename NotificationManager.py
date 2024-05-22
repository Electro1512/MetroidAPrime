import time


class NotificationManager:
    notification_queue = []
    time_since_last_message:int = 0
    last_message_time:int = 0
    message_duration:int = None
    send_notification_func = None

    def __init__(self, message_duration, send_notification_func):
        self.message_duration = message_duration
        self.send_notification_func = send_notification_func

    def queue_notification(self, message):
        self.notification_queue.append(message)

    def handle_notifications(self):
        self.time_since_last_message = time.time() - self.last_message_time
        if len(self.notification_queue) > 0 and self.time_since_last_message >= self.message_duration:
            notification = self.notification_queue[0]
            result = self.send_notification_func(notification)
            if(result):
              self.notification_queue.pop(0)
              self.last_message_time = time.time()
              self.time_since_last_message = 0
