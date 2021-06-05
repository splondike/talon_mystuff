from talon import Module, actions

mod = Module()


@mod.action_class
class EditingActions:
    def repeat_text(text: str, times: int):
        """
        Returns the given pace of text repeated `times` times
        """
        return text * times
