
class FormMixin:
    def get_error_data(self):
        """
        提取form.errors中每个字段的message信息，返回一个字典，格式如下：
        {
        "telephone": ["Ensure this value has at most 11 characters (it has 12)." ],
        "password": ["This field is required."]
        }
        """
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            error_info = {}
            for field, error_list in errors.items():
                new_list = []
                for error_dict in error_list:
                    new_list.append(error_dict['message'])
                error_info[field] = new_list
            return error_info
