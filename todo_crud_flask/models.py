
class Models():

    def __init__(self):
        self.name = 'Models'

    def get_note_model(self):
        return {
            "title": "",
            "user_id": "",
            "created_at": "",
            "updated_at": "",
            "type": ["TODO", "Reminder", "Misc"],
            "content": ""
        }