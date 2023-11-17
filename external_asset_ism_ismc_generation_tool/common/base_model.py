class BaseModel:
    def model_name(self) -> str:
        return type(self).__name__

    def __str__(self):
        return self._nice_formatted()

    def _nice_formatted(self, tabs_count: int = 1):
        result = f"{self.model_name()}:\n"
        for attribute, value in self.__dict__.items():
            formatted_value = BaseModel._nice_formatted(value, tabs_count + 1) if issubclass(type(value), BaseModel) else str(value)
            result += '\t'*tabs_count + f"{attribute}: {formatted_value}\n"

        return result
