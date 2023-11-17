class ILogger:
    def log(self, level, msg):
        raise NotImplementedError

    def info(self, msg):
        raise NotImplementedError

    def warning(self, msg):
        raise NotImplementedError

    def error(self, msg):
        raise NotImplementedError
